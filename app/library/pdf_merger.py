import sys
from typing import List
import logging.config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def merge(input_filenames: List[str], combined_filename: str):
    logger.debug(f"Merging {len(input_filenames)} PDFs into '{combined_filename}'...")
    await merge_via_pypdf2(combined_filename, input_filenames)


async def merge_via_pypdf2(combined_filename, input_filenames):
    logger.debug(
        f"Merging {len(input_filenames)} PDFs into '{combined_filename}' via PyPDF2..."
    )
    from PyPDF2 import PdfFileReader, PdfFileWriter

    input_streams = []
    output_stream = open(combined_filename, "wb")
    try:
        # open input files for reading
        for input_filename in input_filenames:
            input_streams.append(open(input_filename, "rb"))

        pdf_file_writer = PdfFileWriter()

        for pdf_file_reader in map(PdfFileReader, input_streams):
            logger.debug(f"Reading PDF...")
            for page_number in range(pdf_file_reader.getNumPages()):
                logger.debug(f"Reading PDF page {page_number+1}...")
                pdf_input_page = pdf_file_reader.getPage(page_number)
                pdf_file_writer.addPage(pdf_input_page)

        logger.debug("Writing PDF...")
        pdf_file_writer.write(output_stream)

    finally:
        logger.debug("Closing streams...")

        # close input streams
        for input_stream in input_streams:
            input_stream.close()

        # close output stream
        output_stream.close()
