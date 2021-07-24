import sys
from typing import List
from PyPDF2 import PdfFileReader, PdfFileWriter

# def pdf_cat(input_filenames, output_stream):
#     input_streams = []
#
#     try:
#         for input_filename in input_filenames:
#             input_streams.append(open(input_filename, 'rb'))
#
#         writer = PdfFileWriter()
#         for reader in map(PdfFileReader, input_streams):
#             for n in range(reader.getNumPages()):
#                 writer.addPage(reader.getPage(n))
#         writer.write(output_stream)
#     finally:
#         for f in input_streams:
#             f.close()
#         output_stream.close()
#
# if __name__ == '__main__':
#     if sys.platform == "win32":
#         import os, msvcrt
#         msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
#     pdf_cat(sys.argv[1:], sys.stdout)


async def merge(input_filenames: List[str], combined_filename: str):
    input_streams = []
    output_stream = open(combined_filename, 'wb')

    try:
        # open input files for reading
        for input_filename in input_filenames:
            input_streams.append(open(input_filename, 'rb'))

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