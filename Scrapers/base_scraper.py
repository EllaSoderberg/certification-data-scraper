from FileHandleler import HandleFiles
from ScrapingTools import read_write
from DataUploader import Sheet
import winsound
from selenium import webdriver
from datetime import date
import logging
import time

class BaseScraper:
    def __init__(self, link, doc_folder_id, sheet_folder_id, project, header, end_opp, end_page, sheet_id=None, username="", password=""):
        self.link = link
        self.doc_folder_id = doc_folder_id
        self.sheet_folder_id = sheet_folder_id
        self.sheet_id = sheet_id
        self.project = project
        self.header = header
        self.end_opp = end_opp
        self.end_page = end_page
        self.username = username
        self.password = password

        self._data_list = []
        self.first_run = True
        self.table_len = 10
        self.at_opp = 0
        self.start_page = 1
        self.at_page = self.start_page
        self.first_page = True

        self.retries = 0

        self.driver = webdriver.Chrome(executable_path='C:/Users/Ella_/Desktop/Drivers/chromedriver.exe')
        self.today = date.today()

    def run(self):
        logging.info("Running {}....".format(self.project))
        if not self.sheet_id:
            sheet = self.create_sheet()
        else:
            sheet = self.init_sheet()
        # Start the scraper and run until 5 fails
        while self.retries < 5 and self.end_page >= self.at_page:
            try:
                self.driver.get(self.link)
                logging.info("Starting at: {}".format(self.link))

                if self.retries == 0:
                    self.login()

                self.opp_page()

                self.go_to_start_page()

                # While there are still pages to go trough
                while self.end_page >= self.at_page:
                    self.table_len = len(self.get_table())
                    run_range = self.calc_range()
                    # Go trough all the opportunities in the page
                    for tender_no in run_range:
                        print(run_range)
                        # A function to click each element in the list
                        self.at_opp = tender_no
                        data = self.click_links()
                        if data is not None:
                            print("this i will upload", data)
                            self._data_list.append(data)
                            self.go_back()

                            logging.info("Number of datapoints: {}".format(len(self._data_list)))
                            logging.info("Currently at {} of {}".format(tender_no+1, self.table_len))
                            self.upload(sheet, [data])
                            #read_write.save_pickle(self._data_list, "{}.p".format(self.project))
                        self.at_opp += 1


                    self.first_page = False
                    self.at_page += 1
                    self.pagination()
                    self.at_opp = 0

            except Exception:
                self.warning_sound(1500)
                time.sleep(5)
                logging.error("Exception occurred", exc_info=True)
                logging.info("Stopped at page {} and on opportunity {}".format(self.at_page, self.at_opp + 1))
                logging.info("Sheet ID is {}".format(sheet.sheet_id))
                #read_write.save_pickle(self._data_list, "{}.p".format(self.project))
                self.retries += 1
                self.purge()
                self.start_page = self.at_page
                logging.warning("Retry no. {}".format(self.retries))

        if self.retries == 5:
            logging.warning("Maximum retries exceeded, quitting program and saving logs.")
            #read_write.save_pickle([self.at_opp, self.at_page], "stop.p")
            self.purge()
            quit(1)

        #read_write.save_pickle(self._data_list, "{}.p".format(self.project))
        #self.driver.close()
        self.close_files()
        logging.info("Done with {}!".format(self.project))
        self.purge()

    def login(self):
        pass

    def opp_page(self):
        pass

    def get_table(self):
        return []

    def go_back(self):
        return

    def pagination(self):
        pass

    def go_to_start_page(self):
        pass

    def click_links(self):
        pass

    def get_data(self):
        pass

    def download(self, link_text):
        pass

    def purge(self):
        file_deleter = HandleFiles(self.project, self.doc_folder_id)
        file_deleter.delete_files(file_deleter.get_files("docx"))
        file_deleter.delete_files(file_deleter.get_files("pdf"))
        file_deleter.delete_files(file_deleter.get_files("zip"))
        file_deleter.delete_files(file_deleter.get_files("doc"))
        file_deleter.delete_files(file_deleter.get_files("xlsx"))
        file_deleter.delete_files(file_deleter.get_files("txt"))

    def init_sheet(self):
        sheet = Sheet(self.sheet_folder_id, self.project, self.today, sheet_id=self.sheet_id)
        return sheet

    def create_sheet(self):
        sheet = Sheet(self.sheet_folder_id, self.project, self.today)
        sheet.init_sheet(self.header)
        return sheet

    def close_files(self):
        pass

    def upload(self, sheet, data):
        logging.info("Time to upload...")
        sheet.append_row(data)

    def calc_range(self):
        if self.at_page == self.end_page:
            run_range = range(self.at_opp, self.end_opp)
        else:
            run_range = range(self.at_opp, self.table_len)
        return run_range

    @staticmethod
    def warning_sound(freq=2500):
        frequency = freq  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)