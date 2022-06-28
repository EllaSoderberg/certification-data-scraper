import patoolib
from dotenv import load_dotenv
import os

load_dotenv()
PATH = os.environ.get("TEMP_FOLDER")


def extract_files(files):
    """
    Function to extract files of almost any file format.
    :param files: A list of files that can be extracted
    :param path: The path to the folder
    """

    print("Function starting using files", files)
    for file in files:
        print("Extracting....")
        patoolib.extract_archive(file, outdir=PATH)
        print(file, " extracted")


