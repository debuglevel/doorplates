#!/usr/bin/python3
from subprocess import call
from os import remove
import csv
import tempfile
import os
import logging.config
import uuid

#from app.library import inkscape_converter_client

import time
#import app.library.inkscape_converter_client
from pprint import pprint

from app.library import inkscape_converter_client
from app.library.inkscape_converter_client.api import default_api
from app.library.inkscape_converter_client.model.conversion_in import ConversionIn
from app.library.inkscape_converter_client.model.http_validation_error import HTTPValidationError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

data_directory = "data"

async def export_to_pdf(svg: str):
    logger.debug(f"Exporting PDF file for SVG...")
    return await export_to_pdf_microservice(svg)


async def export_to_pdf_microservice(svg: str) -> str:
    id = str(uuid.uuid4())

    # TODO: maybe better pass around a ByteStream or something different instead of a file? no idea.

    # # TODO: delete=False spams data directory
    # with tempfile.NamedTemporaryFile(mode='w', suffix='.pdf', delete=False) as pdf_file:
            # POST to microservice
            # GET form microservice
    #
    #     logger.debug("Sending PDF file...")
    #     return FileResponse(
    #         pdf_file.name, filename=f"doorplates_{doorplate.roomnumber}.pdf", media_type='application/pdf'
    #     )

    import base64

    svg_bytes = svg.encode('ascii')
    base64_svg_bytes = base64.b64encode(svg_bytes)
    base64_svg = base64_svg_bytes.decode('ascii')

    # Defining the host is optional and defaults to http://localhost
    # See configuration.py for a list of all supported configuration parameters.
    configuration = inkscape_converter_client.Configuration(
        host="http://localhost:8081"
    )

    # Enter a context with an instance of the API client
    with inkscape_converter_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)
        conversion_in = ConversionIn(
            base64=base64_svg,
            inputformat="svg",
            outputformat="pdf",
        )  # ConversionIn |

        try:
            # Convert Image
            api_response = api_instance.convert_image_images_post(conversion_in)
            pprint(api_response)
            buffered_reader = api_response
            # save to data directory
            open(get_filename_from_id(id), 'wb').write(buffered_reader.read())

        except inkscape_converter_client.ApiException as e:
            print("Exception when calling DefaultApi->convert_image_images_post: %s\n" % e)


    return str(id)

    pass


def get_filename_from_id(id: str) -> str:
    return f"{data_directory}/{id}.pdf"

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
