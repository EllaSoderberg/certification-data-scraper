from ScrapingTools import read_write
from FileHandleler import HandleFiles
from DataUploader import Sheet
import time
from bs4 import BeautifulSoup
import winsound

import logging


class BaseScraper:
    def __init__(self, link, folder_id, project, header, end_opp, end_page, username="", password=""):
        self.link = link
        self.doc_folder_id = folder_id
        self.project = project
        self.header = header
        self.end_opp = end_opp
        self.end_page = end_page
        self.username = username
        self.password = password

        self.data_list = []
        self.first_run = True
        self.table_len = 10
        self.at_opp = 0
        self.start_page = 1
        self.at_page = self.start_page
        self.first_page = True

        self.retries = 0

        self.driver = webdriver.Chrome(executable_path='C:/Users/Movie Computer/Desktop/drivers/chromedriver.exe')
        self.today = date.today()

    def run(self):
        logging.info("Running {}....".format(self.project))
        # Start the scraper and run until 5 fails
        while self.retries < 5:
            try:
                self.driver.get(self.link)
                logging.info("Starting at:", self.link)

                self.login(self.username, self.password)

                self.opp_page()

                # While there are still pages to go trough
                while self.end_page >= self.at_page:
                    self.table_len = len(self.get_table)
                    run_range = self.calc_range()
                    # Go trough all the opportunities in the page
                    for tender_no in run_range:
                        # A function to click each element in the list
                        self.at_opp = tender_no

                        self.data_list.append(self.click_links())
                        self.go_back()

                        logging.info("Number of datapoints:", len(self.data_list))
                        logging.info("Currently at", tender_no + 1, "of", self.table_len)
                        read_write.save_pickle(self.data_list, "{}.pickle".format(self.project))

                self.first_page = False
                self.at_page += 1
                self.at_opp = 0
                self.pagination()

            except Exception as e:
                logging.error("Exception occurred", exc_info=True)
                print("Stopped at page {} and on opportunity {}".format(self.at_page, self.at_opp + 1))
                self.retries += 1
                logging.warning("Retry no. {}".format(self.retries))

        if self.retries == 5:
            logging.warning("Maximum retries exceeded, quitting program and saving logs.")
            read_write.save_pickle(self, "self.p")
            quit(1)

        read_write.save_pickle(self.data_list, "{}.pickle".format(self.project))
        driver.close()
        self.upload()
        logging.info("Done with {}!".format(self.project))

    def login(self, username, password):
        pass

    def opp_page(self):
        pass

    def get_table(self):
        return []

    def go_back(self):
        return

    def pagination(self):
        pass

    def click_links(self):
        pass

    def get_data(self):
        pass

    def download(self):
        pass

    def upload(self):
        sheet = Sheet(self.doc_folder_id, self.project, self.today)
        sheet.init_sheet(self.header)
        logging.info("Time to upload...")
        sheet.append_row(self.data_list)
        pass

    def calc_range(self):
        if self.at_page == self.end_page:
            run_range = range(self.at_opp - 1, self.end_opp - 1)
        else:
            run_range = range(self.at_opp - 1, self.table_len)
        return run_range

    @staticmethod
    def warning_sound():
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)