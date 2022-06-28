from io import StringIO
import os

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import docx2txt
import re
#import win32com.client as win32
#from win32com.client import constants
import textract

from dotenv import load_dotenv

load_dotenv()
PATH = os.environ.get("TEMP_FOLDER")


def read_pdf_files(files):
    text_dict = {}
    for file in files:
        text = read_pdf(file)
        text_dict[file] = text
        print("done reading, returning string...")
    return text_dict


def read_pdf(filename):
    """
    Reads a PDF file
    :param filename: the name of a PDF file
    :param path: The path to the folder
    :return: the content of the PDF as a string
    """
    output_string = StringIO()
    with open(filename, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            try:
                interpreter.process_page(page)
            except Exception:
                pass
    print("done reading, returning string...")
    return output_string.getvalue()


"""def convert_doc_to_docx(filenames):
    for file in filenames:
        file_path = file
        print(file_path)
        save_as_docx(file_path)
        os.remove(file_path)
    print("done converting")"""


"""def save_as_docx(path):
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
    doc.Close(False)"""


def read_word_files(files):
    text_dict = {}
    for file in files:
        text = textract.process(file)
        text_dict[file] = text
        print("done reading, returning string...")
    return text_dict

