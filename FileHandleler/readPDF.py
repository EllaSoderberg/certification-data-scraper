from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def read_pdf(filename, path="C:\\Users\\Ella\\Downloads"):
    """
    Reads a PDF file
    :param filename: the name of a PDF file
    :param path: The path to the folder
    :return: the content of the PDF as a string
    """
    output_string = StringIO()
    with open(path + "\\" + filename, 'rb') as in_file:
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

