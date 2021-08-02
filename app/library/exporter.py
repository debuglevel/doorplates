#!/usr/bin/python3
import asyncio
import base64
import io
import logging.config
import tempfile
from pathlib import Path

import aiofiles

from app.library import inkscape_converter_client, configuration
from app.library.inkscape_converter_client.api import default_api
from app.library.inkscape_converter_client.model.conversion_request import ConversionRequest
from app.library.inkscape_converter_client.model.conversion_response import ConversionResponse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_doorplates_directory():
    return configuration.get_configuration().doorplates_directory


def get_rendering_backend():
    rendering_backend = configuration.get_configuration().rendering_backend
    logger.debug(f"Using {rendering_backend} as rendering backend.")

    if rendering_backend == "svglib":
        logger.warning(
            "Using svglib as rendering backend. This may produce poor results. Please consider switching to inkscape-microservice."
        )
    elif rendering_backend == "cairosvg":
        logger.warning(
            "Using CairoSVG as rendering backend. This may produce unexpected results with Inkscape SVGs. Please consider switching to inkscape-microservice."
        )

    return rendering_backend


async def export_to_pdf(image_data: bytes, doorplate_id: str):
    logger.debug(
        f"Exporting image ({len(image_data)} bytes) to PDF with id={doorplate_id}..."
    )

    pdf_filename = get_filename_from_id(doorplate_id)

    rendering_backend = get_rendering_backend()
    if rendering_backend == "inkscape-microservice":
        await export_to_pdf_via_inkscape_microservice(image_data, pdf_filename)
    elif rendering_backend == "inkscape":
        await export_to_pdf_via_inkscape(image_data, pdf_filename)
    elif rendering_backend == "svglib":
        await export_to_pdf_via_svglib(image_data, pdf_filename)
    elif rendering_backend == "cairosvg":
        await export_to_pdf_via_cairosvg(image_data, pdf_filename)
    else:
        logger.error(f"Unknown rending backend '{rendering_backend}'!")

    pdf_file = Path(pdf_filename)
    if pdf_file.is_file():
        size = pdf_file.stat().st_size
        if size > 0:
            logger.debug(f"Output file '{pdf_file}' has {size} bytes.")
        else:
            raise FileNotFoundError(
                f"Output file '{pdf_file}' has 0 bytes after rendering."
            )
    else:
        raise FileNotFoundError(
            f"Output file '{pdf_file}' does not exist after rendering."
        )


async def export_to_pdf_via_svglib(image_data: bytes, pdf_filename: str):
    logger.debug(
        f"Exporting image ({len(image_data)} bytes) to '{pdf_filename}' via svglib..."
    )
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF

    file_like_image_data = io.BytesIO(image_data)

    logger.debug("Loading SVG data...")
    drawing = svg2rlg(file_like_image_data)

    logger.debug("Rendering SVG to PDF...")
    renderPDF.drawToFile(drawing, pdf_filename)


async def export_to_pdf_via_cairosvg(image_data: bytes, pdf_filename: str):
    logger.debug(
        f"Exporting image ({len(image_data)} bytes) to '{pdf_filename}' via CairoSVG..."
    )
    import cairosvg

    file_like_image_data = io.BytesIO(image_data)

    logger.debug("Rendering SVG to PDF...")
    cairosvg.svg2pdf(file_obj=file_like_image_data, write_to=pdf_filename)


async def export_to_pdf_via_inkscape(image_data: bytes, pdf_filename: str):
    logger.debug(
        f"Exporting image ({len(image_data)} bytes) to '{pdf_filename}' via Inkscape..."
    )
    from subprocess import call

    with tempfile.NamedTemporaryFile() as input_file:
        logger.debug(f"Writing temporary file to '{input_file.name}'...")
        input_file.write(image_data)
        input_file.flush()

        process_arguments = [
            "inkscape",
            f"{input_file.name}",
            f"--export-filename={pdf_filename}",
        ]

        logger.debug(f"Calling inkscape: {process_arguments}")
        call(process_arguments)
        logger.debug(f"Called inkscape")


async def export_to_pdf_via_inkscape_microservice(image_data: bytes, pdf_filename: str):
    logger.debug(
        f"Exporting image ({len(image_data)} bytes) to '{pdf_filename}' via Inkscape microservice..."
    )

    logger.debug("Encoding image data to Base64...")
    image_base64_bytes = base64.b64encode(image_data)
    image_base64_string = image_base64_bytes.decode("UTF-8")
    logger.debug(
        f"Encoded SVG data ({len(image_data)} bytes) to Base64 ({len(image_base64_string)} bytes)..."
    )

    api_configuration = inkscape_converter_client.Configuration(
        host=configuration.get_configuration().inkscape_url
    )
    with inkscape_converter_client.ApiClient(api_configuration) as inkscape_client:
        inkscape_instance = default_api.DefaultApi(inkscape_client)

        conversion_request = ConversionRequest(
            base64=image_base64_string,
            input_format="svg",  # TODO should not assume file to be SVG
            output_format="pdf",
        )

        try:
            logger.debug(f"Sending POST /images/ request to Inkscape microservice ({api_configuration.host})...")
            # returns an application/octet-stream which results in a BufferedReader here
            # TODO: it would probably be nice if this is async/await,
            #  but OpenAPI generator does not seem to support that.
            #  async_req would at least create a thread; but this does not seem
            #  to be very helpful at this place (maybe in post_doorplate_csv instead of the async?).
            conversion_response: ConversionResponse = inkscape_instance.post_image_images_post(conversion_request)
            logger.debug(f"Received response from Inkscape microservice: {conversion_response}")

        except inkscape_converter_client.ApiException as e:
            logger.error(f"Exception when calling DefaultApi->post_image_images_post: {e}")

        await wait_for_conversion_done(api_configuration, inkscape_instance, conversion_response.id)

        try:
            logger.debug(f"Sending GET /images/{conversion_response.id}/download request to Inkscape microservice ({api_configuration.host})...")

            # returns an application/octet-stream which results in a BufferedReader here
            pdf_buffered_reader = inkscape_instance.download_image_images_image_id_download_get(conversion_response.id)

            async with aiofiles.open(pdf_filename, "wb") as pdf_file:
                logger.debug(f"Writing PDF to {pdf_filename}...")
                await pdf_file.write(pdf_buffered_reader.read())

        except inkscape_converter_client.ApiException as e:
            logger.error(f"Exception when calling DefaultApi->download_image_images_image_id_download_get: {e}")

        # TODO: DELETE image afterwards


async def wait_for_conversion_done(api_configuration, inkscape_instance, conversion_id: str):
    while True:
        logger.debug("Checking if conversion is done...")
        try:
            logger.debug(
                f"Sending GET /images/{conversion_id} request to Inkscape microservice ({api_configuration.host})...")
            conversion_response: ConversionResponse = inkscape_instance.get_image_images_image_id_get(conversion_id)
            if conversion_response.status == "enqueued":
                logger.debug("Conversion is still enqueued. Sleeping and retrying...")
                await asyncio.sleep(1)
                continue
            elif conversion_response.status == "done":
                logger.debug("Conversion is done.")
                break
            else:
                logger.error(f"Conversion has unknown status '{conversion_response.status}'")
        except inkscape_converter_client.ApiException as e:
            logger.error(f"Exception when calling DefaultApi->get_image_images_image_id_get: {e}")
    return conversion_response


def get_filename_from_id(doorplate_id: str) -> str:
    logger.debug(f"Getting PDF filename for doorplate id={doorplate_id}...")
    return f"{get_doorplates_directory()}/{doorplate_id}.pdf"
