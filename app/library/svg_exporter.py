#!/usr/bin/python3
from subprocess import call
from os import remove
import csv
import tempfile
import os
import logging.config
import uuid

# from app.library import inkscape_converter_client

import time
# import app.library.inkscape_converter_client
from pprint import pprint

from app.library import inkscape_converter_client
from app.library.inkscape_converter_client.api import default_api
from app.library.inkscape_converter_client.model.conversion_in import ConversionIn
from app.library.inkscape_converter_client.model.http_validation_error import HTTPValidationError
import base64

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

data_directory = "data"


async def export_to_pdf(svg_data: str, doorplate_id: str):
    logger.debug(f"Exporting SVG data ({len(svg_data)} bytes) to PDF with id={doorplate_id}...")
    return await export_to_pdf_via_inkscape_microservice(svg_data, doorplate_id)


async def export_to_pdf_via_inkscape_microservice(svg_data: str, doorplate_id: str):
    logger.debug(f"Exporting SVG data ({len(svg_data)} bytes) to PDF with id={doorplate_id} via Inkscape microservice...")

    logger.debug("Encoding SVG data to Base64...")
    svg_bytes = svg_data.encode('ascii')
    svg_base64_bytes = base64.b64encode(svg_bytes)
    svg_base64 = svg_base64_bytes.decode('ascii')
    logger.debug(f"Encoded SVG data ({len(svg_data)} bytes) to Base64 ({len(svg_base64)} bytes)...")

    # TODO: the host should be configurable, obviously.
    api_configuration = inkscape_converter_client.Configuration(host="http://localhost:8081")
    with inkscape_converter_client.ApiClient(api_configuration) as inkscape_client:
        inkscape_instance = default_api.DefaultApi(inkscape_client)

        conversion_in = ConversionIn(
            base64=svg_base64,
            inputformat="svg",
            outputformat="pdf",
        )

        try:
            logger.debug("Sending request to Inkscape microservice...")
            # returns an application/octet-stream which results in a BufferedReader here
            pdf_buffered_reader = inkscape_instance.convert_image_images_post(conversion_in)
            logger.debug("Received response from Inkscape microservice")

            pdf_filename = get_filename_from_id(doorplate_id)
            with open(pdf_filename, 'wb') as pdf_file:
                logger.debug(f"Writing PDF to {pdf_filename}...")
                pdf_file.write(pdf_buffered_reader.read())

        except inkscape_converter_client.ApiException as e:
            logger.error(f"Exception when calling DefaultApi->convert_image_images_post: {e}\n")


def get_filename_from_id(doorplate_id: str) -> str:
    logger.debug(f"Getting filename for doorplate id={doorplate_id}...")
    return f"{data_directory}/{doorplate_id}.pdf"

# def export_inkscape(svg: str):
#     logger.debug(f"Exporting PDF file for SVG...")
#
#     with tempfile.NamedTemporaryFile(mode='w', suffix='.svg') as temp_svg_file:
#         logger.debug(f"Writing SVG file '{temp_svg_file.name}'...")
#         temp_svg_file.write(data)
#
#         logger.debug(f"Exporting SVG '{temp_svg_file.name}' to PDF '{pdf_filename}'...")
#         call(["inkscape", f"{temp_svg_file.name}", f"--export-pdf={pdf_filename}"])
#         logger.debug(f"Exported SVG '{temp_svg_file.name}' to PDF '{pdf_filename}'")


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
#             generate_roomplate_13x13(roomnumber, description, personname, pdf_filename)
#
#     # merge all generated room plates into a single PDF
#     num_files = len([f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))])
#     pdf_filename = f"{output_directory}/plates_combined.pdf"
#     logger.debug(f"Merging {num_files} PDF files in '{output_directory}' into '{pdf_filename}'...")
#     call(f"pdftk {output_directory}/*.pdf cat output {pdf_filename}", shell=True)
#     logger.debug(f"Merged {num_files} PDF files in '{output_directory}' into '{pdf_filename}'")
#
#     return pdf_filename
