#!/usr/bin/python3
from subprocess import call
from os import remove
import csv
import tempfile
import os
import logging.config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

templates_directory = "templates/"


async def generate(room_number: str, description: str, person_name: str, template_filename: str) -> str:
    logger.debug(f"Generating SVG file for room number '{room_number}'...")

    svg_template_filename = f'{templates_directory}/{template_filename}'
    logger.debug(f"Reading SVG template '{svg_template_filename}'...")
    with open(svg_template_filename, 'r') as template_svg_file:
        svg_data = template_svg_file.read()

    logger.debug(f"Replacing place holders in SVG file...")
    svg_data = svg_data.replace("$roomNumber$", room_number)
    svg_data = svg_data.replace("$roomDescription$", description)
    svg_data = svg_data.replace("$roomPerson$", person_name)

    return svg_data


async def get_templates():
    return [filename for filename in os.listdir(templates_directory)]


# def batch_from_csv(type, csv_filename, output_directory):
#     logger.debug(f"Generating batch doorplates PDF from CSV file '{csv_filename}'...")
#
#     with open(csv_filename) as csv_file:
#         reader = csv.reader(csv_file, delimiter=';')
#         for row in reader:
#             line_number = str(reader.line_num).zfill(3)
#             logger.debug(f"Parsing row {line_number} in CSV file...")
#
#             try:
#                 roomnumber = row[0]
#             except:
#                 roomnumber = ''
#
#             try:
#                 description = row[1]
#             except:
#                 description = ''
#
#             try:
#                 personname = row[2]
#             except:
#                 personname = ''
#
#             pdf_filename = f"{output_directory}/{line_number}.pdf"
#             logger.debug(f"Using output PDF file '{pdf_filename}'")
#             generate(roomnumber, description, personname, pdf_filename)
#
#     # merge all generated room plates into a single PDF
#     num_files = len([f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))])
#     pdf_filename = f"{output_directory}/plates_combined.pdf"
#     logger.debug(f"Merging {num_files} PDF files in '{output_directory}' into '{pdf_filename}'...")
#     call(f"pdftk {output_directory}/*.pdf cat output {pdf_filename}", shell=True)
#     logger.debug(f"Merged {num_files} PDF files in '{output_directory}' into '{pdf_filename}'")
#
#     return pdf_filename