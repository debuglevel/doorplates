import sys
from typing import List


async def merge(input_filenames: List[str], combined_filename: str):
    await merge_via_pypdf2(combined_filename, input_filenames)


async def merge_via_pypdf2(combined_filename, input_filenames):
    from PyPDF2 import PdfFileReader, PdfFileWriter

    input_streams = []
    output_stream = open(combined_filename, "wb")
    try:
        # open input files for reading
        for input_filename in input_filenames:
            input_streams.append(open(input_filename, "rb"))

        pdf_file_writer = PdfFileWriter()

        for pdf_file_reader in map(PdfFileReader, input_streams):
            for page_number in range(pdf_file_reader.getNumPages()):
                pdf_input_page = pdf_file_reader.getPage(page_number)
                pdf_file_writer.addPage(pdf_input_page)

        pdf_file_writer.write(output_stream)

    finally:
        # close input streams
        for input_stream in input_streams:
            input_stream.close()

        # close output stream
        output_stream.close()
