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


# TODO POST / PUT template


@fastapi.post('/doorplates/')
async def route_doorplate_request(request: Request, content_type: Optional[str] = Header(None)):
    logger.debug(f'Received POST request on /doorplates/. Routing depending on Content-Type ({content_type})...')
    if content_type == "application/json":
        logger.debug("Routing to JSON method...")
        doorplate_data = await request.json()
        doorplate_in = DoorplateIn(**doorplate_data)
        return await post_doorplate(doorplate_in)
    elif content_type == "text/csv":
        logger.debug("Routing to CSV method...")
        doorplates_csv = (await request.body()).decode('UTF-8')
        pprint(doorplates_csv)
        return await post_doorplate_csv(doorplates_csv)
    else:
        # TODO: some exception
        pass

# @fastapi.post('/doorplates/')
async def post_doorplate(doorplate: DoorplateIn):
    #logger.debug('Received POST request on /doorplates/')

    doorplate_id = str(uuid.uuid4())

    asyncio.create_task(generate_doorplate(doorplate, doorplate_id))

    doorplate_out = DoorplateOut(id=doorplate_id)
    return doorplate_out


async def generate_doorplate(doorplate: DoorplateIn, doorplate_id: str):
    svg_data = await svg_generator.generate(doorplate.roomnumber, doorplate.description, doorplate.personname,
                                            doorplate.template)
    await svg_exporter.export_to_pdf(svg_data, doorplate_id)


#@fastapi.post('/doorplates_csv/')
async def post_doorplate_csv(doorplates_csv: str):
    #logger.debug('Received POST request on /doorplates_csv/')

    #logger.debug("Received a CSV request")
    # print("Type of request.data: " + str(type(request.data)))
    #logger.debug(f"CSV data: {doorplates_csv}")


    doorplates = await csv_converter.convert_lines_to_doorplate(doorplates_csv.splitlines())

    doorplates_ids = []

    for doorplate in doorplates:
        doorplate_id = str(uuid.uuid4())
        doorplates_ids.append(doorplate_id)
        logger.debug(f"Generating doorplate with id={doorplate_id}")
        await generate_doorplate(doorplate, doorplate_id)  # TODO: async task and join them all

    # # merge all pdfs into one pdf
    # #                    output | var | input   | filter/predicate
    # even_ints_squared = [e * e for e in a_list if e % 2 == 0]

    doorplates_filepaths = [ svg_exporter.get_filename_from_id(doorplate_id) for doorplate_id in doorplates_ids ]

    #doorplates_filepaths = map(svg_exporter.get_filename_from_id, doorplates_ids)

    combined_id = str(uuid.uuid4())
    combined_filepath = svg_exporter.get_filename_from_id(combined_id)
    await pdf_merger.merge(doorplates_filepaths, combined_filepath)

    # send id
    return combined_id


    # with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv') as temp_csv_file:
    #     logger.debug(f"Writing CSV data to temporary file '{temp_csv_file.name}'...")
    #     temp_csv_file.write(request.data)
    #     temp_csv_file.flush()
    #
    #     with tempfile.TemporaryDirectory() as temp_output_directory:
    #         pdf_filename = export.batch_from_csv(None, temp_csv_file.name, temp_output_directory)
    #
    #         pdf_uuid = str(uuid.uuid4())
    #         stored_pdf_filename = f"{data_directory}/{pdf_uuid}.pdf"
    #         logger.debug(f"Moving PDF file '{pdf_filename}' into data directory '{stored_pdf_filename}'")
    #         shutil.copy2(pdf_filename, stored_pdf_filename)
    #
    #         logger.debug(f"Sending UUID '{pdf_uuid}'...")
    #         return pdf_uuid


@fastapi.get('/doorplates/{id}')
async def download_doorplate(id: str):
    logger.debug(f'Received GET request on /doorplates/{id}')

    pdf_filename = svg_exporter.get_filename_from_id(id)
    logger.debug(f"Sending PDF file '{pdf_filename}'...")
    return FileResponse(
        pdf_filename, filename=f"doorplates_{id}.pdf", media_type= 'application/pdf'
    )


# @fastapi.get("/")
# def read_root():
#     return {"Hello": "World"}
#
#
# @fastapi.get("/greetings/{greeting_id}")
# async def read_item(greeting_id: int, language: Optional[str] = None):
#     return {"greeting_id": greeting_id, "language": language, "greeting": f"Say Hello to ID {greeting_id} in {language}"}
#
# @fastapi.post("/persons/", response_model=PersonOut)
# async def post_person(input_person: PersonIn):
#     person: app.library.person.Person = await app.library.person.create_person(input_person.name)
#     return PersonOut(name=person.name, created_on=person.created_on)
#
# @fastapi.get("/persons/{name}", response_model=PersonOut)
# async def get_person(name: str):
#     person: app.library.person.Person = await app.library.person.get_person(name)
#     return PersonOut(name=person.name, created_on=person.created_on)
#
# # def main():
# #     logger.info("Starting...")
# #
# #     # sleeptime = int(os.environ['SLEEP_INTERVAL'])
# #
# #     parser = argparse.ArgumentParser()
# #     parser.add_argument("--some-host", help="some host", type=str, default="localhost")
# #     parser.add_argument("--some-port", help="some port", type=int, default=8080)
# #     args = parser.parse_args()
# #     # args.some_port
# #     # args.some_host
# #
# #     uvicorn.run(fastapi, host="0.0.0.0", port=8080)
# #
# #
# #
# # def main():
# #     import uvicorn
# #     import yaml
# #     logging.config.dictConfig(yaml.load(open("app/logging-config.yaml", 'r')))  # configured via cmdline
# #     logger.info("Starting via main()...")
# #     uvicorn.run(fastapi, host="0.0.0.0", port=8080)
# #
# # # This only runs if the script is called instead of uvicorn; should probably not be used.
# # if __name__ == "__main__":
# #     main()
