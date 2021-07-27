#!/bin/usr/python3
import asyncio
import logging.config
import threading
import uuid
from pprint import pprint
from typing import Optional, List, Union

from fastapi import FastAPI, File, Form, UploadFile, Depends
from fastapi import Header, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import app.library.person
import app.library.templates
from app.library import health, exporter, doorplates, pdf_merger, templates, configuration
from app.library.doorplates import Doorplate
from app.rest.doorplate import DoorplateRequest, DoorplateResponse, DoorplatesResponse
from app.rest import doorplate

fastapi = FastAPI()

fastapi.mount("/static", StaticFiles(directory="app/static"), name="static")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@fastapi.get("/health")
def get_health():
    logger.debug("Received GET request on /health")
    return health.get_health()


@fastapi.get("/health_async")
async def get_health_async():
    logger.debug("Received GET request on /health_async")
    return await health.get_health_async()


@fastapi.get("/configuration")
async def get_configuration(config: configuration.Configuration = Depends(configuration.get_configuration)):
    return {
        "inkscape_url": config.inkscape_url,
    }


@fastapi.get("/templates/")
async def get_templates():
    logger.debug("Received GET request on /templates")
    return await app.library.templates.get_all_filenames()


@fastapi.post("/templates/")
async def post_file(template_file: UploadFile = File(...), filename: str = Form(...)):
    logger.debug("Received POST request in /templates")
    template_data = await template_file.read()
    await templates.add(filename, template_data)


@fastapi.post("/doorplates/", response_model=Union[DoorplateResponse, DoorplatesResponse])
async def route_doorplate_request(
        request: Request, content_type: Optional[str] = Header(None)
) -> Union[DoorplateResponse, DoorplatesResponse]:
    logger.debug(
        f"Received POST request on /doorplates/. Routing depending on Content-Type ({content_type})..."
    )
    if content_type == "application/json":
        logger.debug("Routing to JSON handler...")
        doorplate_data = await request.json()
        doorplate_in = DoorplateRequest(**doorplate_data)
        doorplate_out = await post_doorplate_json(doorplate_in)
        logger.debug(f"Returning {doorplate_out}...")
        return doorplate_out
    elif content_type.startswith("text/csv"):
        logger.debug("Routing to CSV handler...")
        doorplates_csv = (await request.body()).decode("UTF-8")
        doorplate_out = await post_doorplate_csv(doorplates_csv)
        logger.debug(f"Returning {doorplate_out}...")
        return doorplate_out
    else:
        logger.error("Not routed to anything!")
        # TODO: some exception
        pass


async def post_doorplate_json(doorplate_request: DoorplateRequest) -> DoorplateResponse:
    doorplate_ = await doorplate.to_doorplate(doorplate_request)
    doorplate_.id = str(uuid.uuid4())
    logger.debug(f"Running doorplate generation id={doorplate_.id} in coroutine...")
    asyncio.create_task(generate_doorplate(doorplate_, doorplate_.id))

    doorplate_response = await doorplate.to_doorplate_response(doorplate_)
    return doorplate_response


async def post_doorplate_csv(doorplates_csv) -> DoorplatesResponse:
    doorplates_ = await doorplates.from_csv_lines(doorplates_csv.splitlines())
    for doorplate_ in doorplates_:
        # TODO: questionable if really the rest package should generate the id or better the library
        doorplate_.id = str(uuid.uuid4())

    doorplate_generation_threads: List[threading.Thread] = []

    for doorplate_ in doorplates_:
        logger.debug(f"Starting doorplate generation id={doorplate_.id} in thread...")
        doorplate_generation_thread = threading.Thread(
            target=asyncio.run, args=(generate_doorplate(doorplate_, doorplate_.id),)
        )
        doorplate_generation_threads.append(doorplate_generation_thread)
        doorplate_generation_thread.start()
        logger.debug(f"Started doorplate generation id={doorplate_.id} in thread")

    for doorplate_generation_thread in doorplate_generation_threads:
        logger.debug(f"Starting generation thread {doorplate_generation_thread}...")
        doorplate_generation_thread.join()
        logger.debug(f"Started generation thread {doorplate_generation_thread}")

    doorplates_filepaths = [
        exporter.get_filename_from_id(doorplate_.id) for doorplate_ in doorplates_
    ]

    combined_doorplates_id = str(uuid.uuid4())
    combined_doorplates_filepath = exporter.get_filename_from_id(combined_doorplates_id)
    await pdf_merger.merge(doorplates_filepaths, combined_doorplates_filepath)

    return DoorplatesResponse(
        id=combined_doorplates_id,
        doorplates=[await doorplate.to_doorplate_response(doorplate_) for doorplate_ in doorplates_],
    )


async def generate_doorplate(doorplate_: Doorplate, doorplate_id: str):
    logger.debug(f"Generating doorplate {doorplate_} with id={doorplate_id}")
    svg_data = await app.library.templates.generate(
        doorplate_.roomnumber,
        doorplate_.description,
        doorplate_.personname,
        doorplate_.template,
    )
    await exporter.export_to_pdf(svg_data, doorplate_id)


@fastapi.get("/doorplates/{doorplate_id}")
async def download_doorplate(doorplate_id: str):
    logger.debug(f"Received GET request on /doorplates/{doorplate_id}")

    pdf_filename = exporter.get_filename_from_id(doorplate_id)
    logger.debug(f"Sending PDF file '{pdf_filename}'...")
    return FileResponse(
        pdf_filename,
        filename=f"doorplate_{doorplate_id}.pdf",
        media_type="application/pdf",
    )

# @fastapi.post("/persons/", response_model=PersonOut)
# async def post_person(input_person: PersonIn):
#     person: app.library.person.Person = await app.library.person.create_person(input_person.name)
#     return PersonOut(name=person.name, created_on=person.created_on)
#
# @fastapi.get("/persons/{name}", response_model=PersonOut)
# async def get_person(name: str):
#     person: app.library.person.Person = await app.library.person.get_person(name)
#     return PersonOut(name=person.name, created_on=person.created_on)
