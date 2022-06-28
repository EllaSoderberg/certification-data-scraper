import os
import glob
import time

from . import delete_files, extract_zip, read_files
from dotenv import load_dotenv
from drive_operations import folder

load_dotenv()
PATH = os.environ.get("TEMP_FOLDER")

# Funktioner som
"""
1. Kollar vilken ändelse varje fil har 
2. Läser filerna och använder rätt metod för att göra det
3. Söker igenom texten och sparar orden tillsammans med filnamnet
4. Laddar upp alla filer
5. Tar bort alla filer
"""


def handle_files():
    print("time to handle!!")
    text_dict = {}
    compressed_types = ["zip", "rar", "7z", "gz", "sitx"]
    # Extract all archives
    for type in compressed_types:
        print("extracting" + type)
        extract_zip.extract_files(get_files(type))
    time.sleep(10)

    print("converting")
    read_files.convert_doc_to_docx(get_files("doc"))
    docx_files = get_files("docx")
    text_dict.update(read_files.read_docx_files(docx_files))
    time.sleep(10)

    pdf_files = get_files("pdf")
    print(pdf_files)
    text_dict.update(read_files.read_pdf_files(pdf_files))
    time.sleep(10)

    return text_dict


def get_files(file_format, path=PATH):
    """
    Gets the name of all files in a certain directory. Default downloads.
    :param file_format: A string specifying file type, eg. "pdf", "rar", "zip"
    :param path: The path to the folder
    :return: A list with the full names of the files
    """
    files = []
    for file in glob.glob(path + "\\*." + file_format):
        files.append(file)
    print("files", files)
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    if len(subfolders) != 0:
        print("subfolders",  subfolders)
        subfiles = []
        for folder in subfolders:
            subfiles += get_files(file_format, folder)
        print("subfiles", subfiles)
        files += subfiles
    print("final files", files)
    return files