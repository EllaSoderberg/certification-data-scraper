import os
from dotenv import load_dotenv
import glob

load_dotenv()
PATH = os.environ.get("TEMP_FOLDER")


def delete_files(path=PATH):
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    if len(subfolders) != 0:
        for folder in subfolders:
            delete_files(folder)
            os.rmdir(folder)
    files = glob.glob(path + "/*")
    for f in files:
        os.remove(f)