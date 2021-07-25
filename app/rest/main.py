#!/bin/usr/python3
import logging.config
from pprint import pprint
from typing import Optional
from fastapi import FastAPI
import sys
import tempfile
import uuid
import os
import shutil
import app.library.person
from app.library import health, svg_exporter, svg_generator, csv_converter, pdf_merger
from app.rest.doorplate import DoorplateIn, DoorplateOut
from fastapi.responses import FileResponse
import asyncio
from fastapi import FastAPI, Header, Request

fastapi = FastAPI()

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
    return await svg_generator.get_templates()


# TODO POST / PUT templates


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
        return await post_doorplate(doorplate_in)
    elif content_type == "text/csv":
        logger.debug("Routing to CSV handler...")
        doorplates_csv = (await request.body()).decode("UTF-8")
        return await post_doorplate_csv(doorplates_csv)
    else:
        # TODO: some exception
        pass


async def post_doorplate(doorplate: DoorplateIn) -> DoorplateOut:
    doorplate_id = str(uuid.uuid4())

    logger.debug(f"Running doorplate generation id={doorplate_id} in coroutine...")
    asyncio.create_task(generate_doorplate(doorplate, doorplate_id))

    doorplate_out = DoorplateOut(id=doorplate_id)
    return doorplate_out


async def post_doorplate_csv(doorplates_csv) -> DoorplateOut:
    doorplates = await csv_converter.convert_lines_to_doorplate(
        doorplates_csv.splitlines()
    )

    doorplates_ids = []
    doorplate_generation_tasks = []

    for doorplate in doorplates:
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
        svg_exporter.get_filename_from_id(doorplate_id)
        for doorplate_id in doorplates_ids
    ]

    combined_doorplates_id = str(uuid.uuid4())
    combined_doorplates_filepath = svg_exporter.get_filename_from_id(
        combined_doorplates_id
    )
    await pdf_merger.merge(doorplates_filepaths, combined_doorplates_filepath)

    return DoorplateOut(id=combined_doorplates_id)


async def generate_doorplate(doorplate: DoorplateIn, doorplate_id: str):
    logger.debug(f"Generating doorplate {doorplate} with id={doorplate_id}")
    svg_data = await svg_generator.generate(
        doorplate.roomnumber,
        doorplate.description,
        doorplate.personname,
        doorplate.template,
    )
    await svg_exporter.export_to_pdf(svg_data, doorplate_id)


@fastapi.get("/doorplates/{id}")
async def download_doorplate(doorplate_id: str):
    logger.debug(f"Received GET request on /doorplates/{doorplate_id}")

    pdf_filename = svg_exporter.get_filename_from_id(doorplate_id)
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
