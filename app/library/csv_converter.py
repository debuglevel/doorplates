from typing import List
import csv

from app.rest.doorplate import DoorplateIn
import logging.config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def convert_lines_to_doorplate(lines: List[str]) -> List[DoorplateIn]:
    doorplates = []

    csv_reader = csv.reader(lines, delimiter=";")
    for row in csv_reader:
        logger.debug(f"Parsing row {csv_reader.line_num} in CSV file...")
        doorplates.append(await convert_row_to_doorplate(row))

    return doorplates


async def convert_row_to_doorplate(csv_row):
    room_number_column_index = 0
    description_column_index = 1
    person_name_column_index = 2
    template_column_index = 3

    try:
        room_number = csv_row[room_number_column_index]
    except:
        room_number = ""

    try:
        description = csv_row[description_column_index]
    except:
        description = ""

    try:
        person_name = csv_row[person_name_column_index]
    except:
        person_name = ""

    try:
        template = csv_row[template_column_index]
    except:
        template = ""

    return DoorplateIn(
        roomnumber=room_number,
        description=description,
        personname=person_name,
        template=template,
    )
