import logging.config
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

templates_directory = "data/templates/"


async def add(filename: str, data: str):
    logger.debug(f"Adding template {filename}...")
    filepath = get_filepath(filename)
    with open(filepath, "w") as file:
        file.write(data)


async def get_all_filenames():
    logger.debug("Getting templates...")
    return [filename for filename in os.listdir(templates_directory)]


def get_filepath(filename: str) -> str:
    logger.debug(f"Getting template filepath for {filename}...")
    filepath = f"{templates_directory}/{filename}"
    return filepath


async def get_data(filename: str) -> str:
    logger.debug(f"Getting template {filename}...")
    filepath = get_filepath(filename)
    with open(filepath, "r") as file:
        data = file.read()
    return data


async def generate(
    room_number: str, description: str, person_name: str, template_filename: str
) -> str:
    logger.debug(f"Generating template file for room number '{room_number}'...")

    data = await get_data(template_filename)
    data = await replace_placeholders(data, description, person_name, room_number)

    return data


async def replace_placeholders(data, description, person_name, room_number):
    logger.debug(f"Replacing placeholders in template file...")

    data = data.replace("$roomNumber$", room_number)
    data = data.replace("$roomDescription$", description)
    data = data.replace("$roomPerson$", person_name)

    return data
