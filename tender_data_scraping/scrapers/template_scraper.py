from selenium.webdriver.common.by import By
from datetime import datetime
import time
from scraping_operations.scraping_machine import ScrapingMachine

class Template(ScrapingMachine):
    def __init__(self):
        super(Template, self).__init__(
            link="https://www.example.com",
            doc_folder_id="1ckD74zWxLjDJSpNuJYu1MAQT1KtwlPrG",
            sheet_folder_id="1_3CkwtS6EMUdD3WRUQ7B3jhgUn3T1v-y",
            project="Template",
            data={"Title": None, "Reference": None, "Published": None, "TCOC mentioned": "", "EPEAT mentioned": "",
                  "Keywords in description": "", "Keywords in documents": "", "Link to documents": None},
            username="user",
            password="pass",
        )

    def login(self):
        """
        Function to use the driver to log in to the database
        """
        pass

    def go_to_database(self):
        """
        Function to go to the page where the database is found
        """
        pass

    def navigate_to_current_page(self):
        """
        If the script has previously restarted, this function will go to the correct page.
        """
        pass

    def find_final_page(self):
        """
        Function to find where the final page is.
        :return: final page as an int
        """
        return

    def get_table(self):
        """
        Function to retrieve the table and return its elements
        :return: The elements of the table as a webdriver object
        """
        return

    def go_to_tender(self, tender):
        """
        :return: dictionary with all the data with at least the values:
        {
        title:,
        date_published:,
        }
        """
        return self.data, ""

    def documents_exist(self):
        """
        Check if there are any documents to download
        :return: True or False
        """
        return False

    def download_documents(self):
        """
        Download documents
        :return:
        """
        pass

    def go_back(self):
        """
        Go back to database page
        """
        pass

    def pagination(self):
        """
        Paginate trough the pages
        """
        pass

