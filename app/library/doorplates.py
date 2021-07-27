from typing import List, Optional
import csv

from pydantic import BaseModel

import logging.config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Doorplate(BaseModel):
    id: Optional[str]
    roomnumber: str
    description: str
    personname: str
    template: str


async def from_csv_lines(lines: List[str]) -> List[Doorplate]:
    logger.debug("Building Doorplates from CSV lines...")

    doorplates: List[Doorplate] = []

    csv_reader = csv.reader(lines, delimiter=";")
    for row in csv_reader:
        logger.debug(f"Parsing row {csv_reader.line_num} in CSV file...")
        doorplates.append(await from_csv_row(row))

    return doorplates


async def from_csv_row(csv_row: List[str]) -> Doorplate:
    logger.debug("Building Doorplate from CSV line...")

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

    return Doorplate(
        roomnumber=room_number,
        description=description,
        personname=person_name,
        template=template,
    )
