import docx2txt

from glob import glob
import re
import os
import win32com.client as win32
from win32com.client import constants


def save_as_docx(path):
    # Opening MS Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(path)
    doc.Activate()

    # Rename path with .docx
    new_file_abs = os.path.abspath(path)
    new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

    # Save and Close
    word.ActiveDocument.SaveAs(
        new_file_abs, FileFormat=constants.wdFormatXMLDocument
    )
    doc.Close(False)


def convert_doc_to_docx():
    paths = glob('C:\\Users\\Ella_\\Downloads\\**\\*.doc', recursive=True)
    for file in paths:
        print(file)
        save_as_docx(file)
        os.remove(file)
    print("done converting")


def read_docx_files(filename, path="C:\\Users\\Ella_\\Downloads"):
    text = docx2txt.process(path + "\\" + filename)
    print("done reading, returning string...")
    return text