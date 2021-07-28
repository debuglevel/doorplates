#!/usr/bin/python3
import base64
import logging.config

import aiofiles

from app.library import inkscape_converter_client, configuration
from app.library.inkscape_converter_client.api import default_api
from app.library.inkscape_converter_client.model.conversion_in import ConversionIn

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

data_directory = "data/doorplates/"


async def export_to_pdf(image_data: str, doorplate_id: str):
    logger.debug(
        f"Exporting image ({len(image_data)} bytes) to PDF with id={doorplate_id}..."
    )
    await export_to_pdf_via_inkscape_microservice(image_data, doorplate_id)


async def export_to_pdf_via_inkscape_microservice(image_data: str, doorplate_id: str):
    logger.debug(
        f"Exporting image ({len(image_data)} bytes) to PDF with id={doorplate_id} via Inkscape microservice..."
    )

    logger.debug("Encoding image data to Base64...")
    image_bytes = image_data.encode("UTF-8")
    image_base64_bytes = base64.b64encode(image_bytes)
    image_base64 = image_base64_bytes.decode("UTF-8")
    logger.debug(
        f"Encoded SVG data ({len(image_data)} bytes) to Base64 ({len(image_base64)} bytes)..."
    )

    api_configuration = inkscape_converter_client.Configuration(
        host=configuration.get_configuration().inkscape_url
    )
    with inkscape_converter_client.ApiClient(api_configuration) as inkscape_client:
        inkscape_instance = default_api.DefaultApi(inkscape_client)

        conversion_in = ConversionIn(
            base64=image_base64,
            inputformat="svg",  # TODO should not only be svg
            outputformat="pdf",
        )

        try:
            logger.debug(f"Sending request to Inkscape microservice ({api_configuration.host})...")
            # returns an application/octet-stream which results in a BufferedReader here
            # TODO: it would probably be nice if this is async/await,
            #  but OpenAPI generator does not seem to support that.
            #  async_req would at least create a thread; but this does not seem
            #  to be very helpful at this place (maybe in post_doorplate_csv instead of the async?).
            pdf_buffered_reader = inkscape_instance.convert_image_images_post(
                conversion_in
            )
            logger.debug("Received response from Inkscape microservice")

            pdf_filename = get_filename_from_id(doorplate_id)
            async with aiofiles.open(pdf_filename, "wb") as pdf_file:
                logger.debug(f"Writing PDF to {pdf_filename}...")
                await pdf_file.write(pdf_buffered_reader.read())

        except inkscape_converter_client.ApiException as e:
            logger.error(
                f"Exception when calling DefaultApi->convert_image_images_post: {e}\n"
            )


def get_filename_from_id(doorplate_id: str) -> str:
    logger.debug(f"Getting PDF filename for doorplate id={doorplate_id}...")
    return f"{data_directory}/{doorplate_id}.pdf"
