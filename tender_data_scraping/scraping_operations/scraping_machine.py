import os
import sys
import time
import traceback
#import Appkit

import drive_operations.google_sheets as sheets
from file_operations import delete_files, handle_files
from text_operations import analyze
from drive_operations import folder
from . import new_chrome_browser

from dotenv import load_dotenv
from datetime import date

from . import read_write_cache

load_dotenv()

class ScrapingMachine:

    def __init__(self, link, doc_folder_id, sheet_folder_id, project, data, username="", password=""):
        self.link = link
        self.doc_folder_id = doc_folder_id
        self.sheet_folder_id = sheet_folder_id
        self.sheet_id = None
        self.sheet = None
        self.project = project
        self.username = username
        self.password = password
        self.data = data

        self.at_page = 0
        self.at_opp = 0
        self.end_page = None
        self.end_opp = None
        self.last_tender_title = None
        self.last_tender_published = None
        self.first_tender_title = None
        self.first_tender_published = None
        self.last_run = date.today()


        self.driver = new_chrome_browser(executable_path=os.environ.get("DRIVER_PATH"),
                                         download_path=os.environ.get("TEMP_FOLDER"))
        self.today = date.today()
        self.success = False

        # Check the previous run to set variables from previous run
        self.read_cache()
        self.new_cache = {
            "last_run": self.last_run.strftime("%Y-%m-%d"),
            "run_successful": False,
            "sheet_id": self.sheet_id,
            "last_tender_title": self.last_tender_title,
            "last_tender_published": self.last_tender_published,
            "first_tender_title": self.first_tender_title,
            "first_tender_published": self.first_tender_published,
            "at_page": self.at_page,
            "at_opp": self.at_opp,
            }
        if self.last_tender_published is not None:
            self.new_cache["last_tender_published"] = self.last_tender_published.strftime("%Y-%m-%d")

    def read_cache(self):
        """
        Function to read cache from pickle with the same name as project.
        Sets variables depending on whether the last run was successful or exited with errors.
        """
        cache = read_write_cache.read_cache(self.project)

        if cache["run_successful"]:
            self.sheet = sheets.create_sheet(self.sheet_folder_id, self.project, self.today, list(self.data.keys()))
            self.sheet_id = self.sheet.sheet_id
        else:
            self.sheet_id = cache["sheet_id"]
            self.sheet = sheets.init_sheet_from_id(self.sheet_folder_id, self.project, self.today, self.sheet_id)

        self.last_run = date.fromisoformat(cache["last_run"])
        self.last_tender_title = cache["last_tender_title"]
        if cache["last_tender_published"] is not None:
            self.last_tender_published = date.fromisoformat(cache["last_tender_published"])
        self.first_tender_title = cache["first_tender_title"]
        self.first_tender_published = cache["first_tender_published"]
        self.at_page = cache["at_page"]
        self.at_opp = cache["at_opp"]

    def run(self):
        """
        Main function to run the scraping script
        :return:
        """
        # Get the link
        self.driver.get(self.link)
        time.sleep(2)

        # Log in
        self.login()

        # Navigate to opportunities page
        self.go_to_database()

        # Navigate to the correct page
        self.navigate_to_current_page()

        # Find what page the script should stop running on.
        self.end_page = self.find_final_page()

        # Here the scraping loop starts
        while True:
            try:
                # Get table
                table_lenght = len(self.get_table())
                # Go trough each element in the table
                for tender_no in range(self.at_opp, table_lenght):
                    self.data['Keywords in documents'] = ""
                    time.sleep(5)

                    tender = self.get_table()

                    # Get all the data, all values, text on the page etc. return as a dictionary.
                    print(tender[tender_no])
                    data, text_to_analyze = self.go_to_tender(tender[tender_no])

                    # If the first opportunity is scraped, save this to the cache.
                    if self.at_opp == 0 and self.at_page == 0:
                        self.new_cache["first_tender_title"] = self.data["Title"]
                        self.new_cache["first_tender_published"] = self.data["Published"]
                        self.first_tender_title = self.data["Title"]
                        self.first_tender_published = self.data["Published"]

                    # Check if it should be the last opportunity. If it is, skip everything else.
                    if self.end_page is None:
                        if self.last_tender_title is not None and self.data["Title"] == self.last_tender_title or \
                                self.last_tender_published is not None and date.fromisoformat(self.data["Published"]) \
                                < self.last_tender_published:
                            self.new_cache.update({
                                "last_run": self.today.strftime("%Y-%m-%d"),
                                "run_successful": True,
                                "sheet_id": None,
                                "last_tender_title": self.first_tender_title,
                                "last_tender_published": self.first_tender_published,
                                "first_tender_title": None,
                                "first_tender_published": None,
                                "at_page": 0,
                                "at_opp": 0
                            })
                            self.finish_scraping()
                            sys.exit("Finished successfully")

                    else:
                        if int(self.end_page) + 1 <= self.at_page:
                            self.new_cache.update({
                                "last_run": self.today.strftime("%Y-%m-%d"),
                                "run_successful": True,
                                "sheet_id": None,
                                "at_page": 0,
                                "at_opp": 0
                            })
                            self.finish_scraping()
                            sys.exit("Finished successfully")

                    # Analyze text
                    mention = analyze.analyze(text_to_analyze)
                    self.data["TCOC mentioned"] = mention["TCO"]
                    self.data["EPEAT mentioned"] = mention["EPEAT"]
                    self.data["Keywords in description"] = analyze.analysis(text_to_analyze)

                    # Download and check documents
                    if self.documents_exist():
                        self.download_documents()
                        time.sleep(10)

                        # Get the text from the documents and convert it to text trough the modules
                        text_dict = handle_files.handle_files()
                        time.sleep(20)
                        for key in text_dict.keys():
                            found_words = analyze.find_search_words(text_dict[key])
                            if found_words is not None:
                                self.data['Keywords in documents'] += "{}: {} ".format(key.split("\\")[-1], found_words)

                        # Upload documents to drive
                        folder_name = self.data["Reference"]
                        if folder_name is None:
                            folder_name = self.data["Title"]
                        self.data["Link to documents"] = folder.upload_to_drive(folder_name, self.doc_folder_id)
                        time.sleep(60)

                        # Finally delete all the files
                        delete_files.delete_files()

                    # Interpret all the text read and create a dictionary with the findings
                    # Send data and documents to google drive
                    self.sheet.append_row([list(self.data.values())])

                    # Save cache
                    read_write_cache.write_cache(self.project, self.new_cache)

                    # Move on to the next one
                    self.go_back()
                    self.at_opp += 1
                    time.sleep(5)

                # Go to the next page
                self.at_page += 1
                self.pagination()
                self.at_opp = 0

            except Exception:
                traceback.print_exc()
                self.new_cache.update({
                    "run_successful": False,
                    "sheet_id": self.sheet_id,
                    "at_page": self.at_page,
                    "at_opp": self.at_opp,
                })
                self.finish_scraping()
                sys.exit("Finished with an error")

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
        return {}

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

    def finish_scraping(self):
        """
        Function to close the script in a good way.
        """
        read_write_cache.write_cache(self.project, self.new_cache)
        delete_files.delete_files()
        self.driver.quit()

    @staticmethod
    def warning_sound(freq=2500):
        """
        Function that simply makes noise.
        :param freq: the frequency of the sound
        """
        frequency = freq  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        #winsound.Beep(frequency, duration)
        AppKit.NSBeep()
