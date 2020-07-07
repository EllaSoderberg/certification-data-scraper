from FileHandleler import HandleFiles
from ScrapingTools import read_write
from DataUploader import Sheet
import winsound
from selenium import webdriver
from datetime import date
import logging


class BaseScraper:
    def __init__(self, link, doc_folder_id, sheet_folder_id, project, header, end_opp, end_page, username="", password=""):
        self.link = link
        self.doc_folder_id = doc_folder_id
        self.sheet_folder_id = sheet_folder_id
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
        while self.retries < 5 and self.end_page >= self.at_page:
            try:
                self.driver.get(self.link)
                logging.info("Starting at:", self.link)

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
                        self.data_list.append(self.click_links())
                        self.go_back()
                        self.at_opp += 1

                        logging.info("Number of datapoints:", len(self.data_list))
                        logging.info("Currently at", tender_no + 1, "of", self.table_len)
                        read_write.save_pickle(self.data_list, "{}.pickle".format(self.project))
                        print(self.at_opp)
                        print(self.at_page)

                    self.first_page = False
                    self.at_page += 1
                    self.pagination()
                    print(self.at_page)
                    self.at_opp = 0

            except Exception:
                logging.error("Exception occurred", exc_info=True)
                logging.info("Stopped at page {} and on opportunity {}".format(self.at_page, self.at_opp + 1))
                self.retries += 1
                self.purge()
                self.start_page = self.at_page
                logging.warning("Retry no. {}".format(self.retries))

        if self.retries == 5:
            logging.warning("Maximum retries exceeded, quitting program and saving logs.")
            read_write.save_pickle([self.at_opp, self.at_page], "stop.p")
            self.purge()
            quit(1)

        read_write.save_pickle(self.data_list, "{}.pickle".format(self.project))
        print("closing driver")
        self.driver.close()
        print("uploading files")
        print(self.data_list)
        self.upload()
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

    def upload(self):
        sheet = Sheet(self.sheet_folder_id, self.project, self.today)
        sheet.init_sheet(self.header)
        logging.info("Time to upload...")
        sheet.append_row(self.data_list)
        pass

    def calc_range(self):
        if self.at_page == self.end_page:
            run_range = range(self.at_opp, self.end_opp)
        else:
            run_range = range(self.at_opp, self.table_len)
        return run_range

    @staticmethod
    def warning_sound():
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)