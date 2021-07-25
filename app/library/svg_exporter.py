#!/usr/bin/python3
import base64
import logging.config

from app.library import inkscape_converter_client
from app.library.inkscape_converter_client.api import default_api
from app.library.inkscape_converter_client.model.conversion_in import ConversionIn

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

data_directory = "data/doorplates/"


async def export_to_pdf(svg_data: str, doorplate_id: str):
    logger.debug(
        f"Exporting SVG data ({len(svg_data)} bytes) to PDF with id={doorplate_id}..."
    )
    await export_to_pdf_via_inkscape_microservice(svg_data, doorplate_id)


async def export_to_pdf_via_inkscape_microservice(svg_data: str, doorplate_id: str):
    logger.debug(
        f"Exporting SVG data ({len(svg_data)} bytes) to PDF with id={doorplate_id} via Inkscape microservice..."
    )

    logger.debug("Encoding SVG data to Base64...")
    # TODO: UTF-8 instead? test if it works
    svg_bytes = svg_data.encode("ascii")
    svg_base64_bytes = base64.b64encode(svg_bytes)
    svg_base64 = svg_base64_bytes.decode("ascii")
    logger.debug(
        f"Encoded SVG data ({len(svg_data)} bytes) to Base64 ({len(svg_base64)} bytes)..."
    )

    # TODO: the host should be configurable, obviously.
    api_configuration = inkscape_converter_client.Configuration(
        host="http://localhost:8081"
    )
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
            pdf_buffered_reader = inkscape_instance.convert_image_images_post(
                conversion_in
            )
            logger.debug("Received response from Inkscape microservice")

            pdf_filename = get_filename_from_id(doorplate_id)
            with open(pdf_filename, "wb") as pdf_file:
                logger.debug(f"Writing PDF to {pdf_filename}...")
                pdf_file.write(pdf_buffered_reader.read())

        except inkscape_converter_client.ApiException as e:
            logger.error(
                f"Exception when calling DefaultApi->convert_image_images_post: {e}\n"
            )


def get_filename_from_id(doorplate_id: str) -> str:
    logger.debug(f"Getting filename for doorplate id={doorplate_id}...")
    return f"{data_directory}/{doorplate_id}.pdf"
