#!/usr/bin/python3
from subprocess import call
from os import remove
import csv
import tempfile
import os
import logging.config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

templates_directory = "data/templates/"


async def generate(
    room_number: str, description: str, person_name: str, template_filename: str
) -> str:
    logger.debug(f"Generating SVG file for room number '{room_number}'...")

    svg_template_filename = f"{templates_directory}/{template_filename}"
    logger.debug(f"Reading SVG template '{svg_template_filename}'...")
    with open(svg_template_filename, "r") as template_svg_file:
        svg_data = template_svg_file.read()

    logger.debug(f"Replacing place holders in SVG file...")
    svg_data = svg_data.replace("$roomNumber$", room_number)
    svg_data = svg_data.replace("$roomDescription$", description)
    svg_data = svg_data.replace("$roomPerson$", person_name)

    return svg_data


async def get_templates():
    return [filename for filename in os.listdir(templates_directory)]
