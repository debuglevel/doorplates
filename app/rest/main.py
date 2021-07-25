#!/bin/usr/python3
import asyncio
import logging.config
import uuid
from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile
from fastapi import Header, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import app.library.person
import app.library.templates
from app.library import health, exporter, doorplates, pdf_merger, templates
from app.rest.doorplate import DoorplateIn, DoorplateOut

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


@fastapi.get("/templates/")
async def get_templates():
    logger.debug("Received GET request on /templates")
    return await app.library.templates.get_all_filenames()


@fastapi.post("/templates/")
async def post_file(
    template_file: UploadFile = File(...), filename: str = Form(...)
):
    logger.debug("Received POST request in /templates")
    template_data = await template_file.read()
    await templates.add(filename, template_data)


@fastapi.post("/doorplates/", response_model=DoorplateOut)
async def route_doorplate_request(
    request: Request, content_type: Optional[str] = Header(None)
) -> DoorplateOut:
    logger.debug(
        f"Received POST request on /doorplates/. Routing depending on Content-Type ({content_type})..."
    )
    if content_type == "application/json":
        logger.debug("Routing to JSON handler...")
        doorplate_data = await request.json()
        doorplate_in = DoorplateIn(**doorplate_data)
        doorplate_out = await post_doorplate(doorplate_in)
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


async def post_doorplate(doorplate: DoorplateIn) -> DoorplateOut:
    doorplate_id = str(uuid.uuid4())

    logger.debug(f"Running doorplate generation id={doorplate_id} in coroutine...")
    asyncio.create_task(generate_doorplate(doorplate, doorplate_id))

    doorplate_out = DoorplateOut(id=doorplate_id)
    return doorplate_out


async def post_doorplate_csv(doorplates_csv) -> DoorplateOut:
    doorplates_ = await doorplates.from_csv_lines(doorplates_csv.splitlines())

    doorplates_ids = []
    doorplate_generation_tasks = []

    for doorplate in doorplates_:
        doorplate_id = str(uuid.uuid4())
        doorplates_ids.append(doorplate_id)

        # logger.debug(f"X Running doorplate generation id={doorplate_id} in coroutine...")
        # TODO: this seems at least not to run in parallel
        doorplate_generation_tasks.append(
            asyncio.create_task(generate_doorplate(doorplate, doorplate_id))
        )
        # logger.debug(f"X Ran doorplate generation id={doorplate_id} in coroutine")

    for doorplate_generation_task in doorplate_generation_tasks:
        # logger.debug(f"Y Awaiting generation task {doorplate_generation_task}...")
        await doorplate_generation_task
        # logger.debug(f"Y Awaited generation task {doorplate_generation_task}")

    doorplates_filepaths = [
        exporter.get_filename_from_id(doorplate_id) for doorplate_id in doorplates_ids
    ]

    combined_doorplates_id = str(uuid.uuid4())
    combined_doorplates_filepath = exporter.get_filename_from_id(combined_doorplates_id)
    await pdf_merger.merge(doorplates_filepaths, combined_doorplates_filepath)

    return DoorplateOut(id=combined_doorplates_id)


async def generate_doorplate(doorplate: DoorplateIn, doorplate_id: str):
    logger.debug(f"Generating doorplate {doorplate} with id={doorplate_id}")
    svg_data = await app.library.templates.generate(
        doorplate.roomnumber,
        doorplate.description,
        doorplate.personname,
        doorplate.template,
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
