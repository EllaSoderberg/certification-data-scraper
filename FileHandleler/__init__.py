import glob
import os

from FileHandleler import extractor, readPDF, analysePDF, drive_upload, read_doc
import patoolib

downloads_path = "C:\\Users\\Movie Computer\\Downloads"


class HandleFiles:
    def __init__(self, project_name, dest_folder, path=downloads_path):
        self.path = path
        self.project_name = project_name
        self.dest_folder = dest_folder
        self.ext_files = []
        self.file_list = []
        self.folder_list = []
        self.found_words = []
        self.folder_link = ""

    def get_files(self, file_format):
        """
        Gets the name of all files in a certain directory. Default downloads.
        :param file_format: A string specifying file type, eg. "pdf", "rar", "zip"
        :param path: The path to the folder
        :return: A list with the full names of the files
        """
        files = []
        os.chdir(self.path)
        for file in glob.glob("*." + file_format):
            files.append(file)
        return files

    def delete_files(self, files):
        """
        Deletes the specified files
        :param files: A list with the full names of the files to be removed
        """
        os.chdir(self.path)
        for file in files:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass

    def extract_files(self, filetypes):
        """
        Extracts the files of specified type
        :param filetypes: a list of filetypes to extract
        """
        for f_type in filetypes:
            print("time to extract", f_type)
            self.ext_files += self.get_files(f_type)
            print("gonna extract", self.ext_files)
            for file in self.ext_files:
                patoolib.extract_archive(self.path + "\\" + file, outdir=self.path)
                print("extracted", file)

    def get_folder_files(self, file_format):
        files = []
        os.chdir(self.path)

        for folder in glob.glob('*\\'):
            if folder[:-1] not in self.folder_list:
                self.folder_list.append(folder[:-1])
            os.chdir(self.path + "\\" + folder)
            for file in glob.glob("*." + file_format):
                files.append(folder + file)
        return files

    def read_pdfs(self):
        """
        Reads the PDF files in the selected folder
        :return: Returns the found words as a list
        """
        print("Reading PDFs....")
        pdf_list = self.get_files("pdf")
        pdf_list = pdf_list + self.get_folder_files("pdf")
        self.file_list = self.file_list + pdf_list
        for file in pdf_list:
            text = readPDF.read_pdf(file, self.path)
            words = analysePDF.find_search_words(text)
            print(words)
            if words is not None:
                if len(words) != 0:
                    self.found_words += words
        return str(self.found_words)

    def read_docx(self):
        #read_doc.convert_doc_to_docx()
        doc_list = self.get_files("docx")
        doc_list = doc_list + self.get_folder_files("docx")
        self.file_list = self.file_list + doc_list
        for file in doc_list:
            text = read_doc.read_docx_files(file, self.path)
            words = analysePDF.find_search_words(text)
            print(words)
            if words is not None:
                if len(words) != 0:
                    self.found_words += words
        return str(self.found_words)

    def upload_files(self):
        """
        Uploads all files to drive.
        :return: returns link to drive
        """
        self.folder_link = drive_upload.upload_to_drive(self.project_name, self.dest_folder, self.file_list, self.path)
        return self.folder_link

    def delete_all_files(self):
        """
        Deletes all files that has been used
        """
        print("gonna delete", self.ext_files, self.file_list)
        print("and", self.folder_list)

        self.delete_files(self.ext_files)
        self.delete_files(self.file_list)
        self.delete_files(self.get_files("zip"))
        print("files", glob.glob('*\\'))
        for folder in self.folder_list:
            print(self.path + "\\" + folder)
            os.chdir(self.path + "\\" + folder)
            for file in glob.glob("*.*"):
                os.remove(file)
            os.chdir(self.path)
            #for folder in self.folder_list:
                #os.rmdir(self.path + "\\" + folder)
            os.rmdir(self.path + "\\" + folder)

        self.file_list = []
        self.ext_files = []
        self.folder_list = []

