from typing import List
import csv

from app.rest.doorplate import DoorplateIn
import logging.config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# async def convert_line_to_json(line: str) -> DoorplateIn:
#     pass

async def convert_lines_to_doorplate(lines: List[str]) -> List[DoorplateIn]:
    doorplates = []

    csv_reader = csv.reader(lines, delimiter=';')
    for row in csv_reader:
        logger.debug(f"Parsing row {csv_reader.line_num} in CSV file...")

        doorplates.append(await convert_row_to_doorplate(row))

    return doorplates

    # # TODO: maybe uns csvreader which would then just parse the whole thing
    # return [ await convert_line_to_json(line) for line in lines.splitlines() ]


async def convert_row_to_doorplate(row):
    try:
        roomnumber = row[0]
    except:
        roomnumber = ''
    try:
        description = row[1]
    except:
        description = ''
    try:
        personname = row[2]
    except:
        personname = ''
    try:
        template = row[3]
    except:
        template = ''

    return DoorplateIn(roomnumber=roomnumber, description=description, personname=personname, template=template)
