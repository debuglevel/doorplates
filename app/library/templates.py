import logging.config
import os
from typing import Union

import aiofiles

from app.library import configuration

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_templates_directory():
    return configuration.get_configuration().templates_directory


async def add(filename: str, data: Union[bytes, str]):
    logger.debug(f"Adding template {filename} ({len(data)} bytes)...")
    filepath = get_filepath(filename)
    async with aiofiles.open(filepath, "wb") as file:
        await file.write(data)


async def get_all_filenames():
    logger.debug("Getting templates...")
    return [filename for filename in os.listdir(get_templates_directory())]


def get_filepath(filename: str) -> str:
    logger.debug(f"Getting template filepath for {filename}...")
    filepath = f"{get_templates_directory()}/{filename}"
    return filepath


async def get_data(filename: str) -> bytes:
    logger.debug(f"Getting template {filename}...")
    filepath = get_filepath(filename)
    async with aiofiles.open(filepath, "rb") as file:
        data = await file.read()
    return data


async def generate(
    room_number: str, description: str, person_name: str, template_filename: str
) -> bytes:
    logger.debug(f"Generating template file for room number '{room_number}'...")

    data = await get_data(template_filename)
    data = await replace_placeholders(data, description, person_name, room_number)

    return data


async def replace_placeholders(
    data: bytes, description: str, person_name: str, room_number: str
):
    logger.debug(f"Replacing placeholders in template file...")

    data = data.replace(b"$roomNumber$", bytes(room_number, "UTF-8"))
    data = data.replace(b"$roomDescription$", bytes(description, "UTF-8"))
    data = data.replace(b"$roomPerson$", bytes(person_name, "UTF-8"))

    return data
