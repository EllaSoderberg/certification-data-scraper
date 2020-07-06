from FileHandleler import HandleFiles
from DataUploader import Sheet
from ScrapingTools import read_write
import time
import winsound
import logging

from Scrapers.base_scraper import BaseScraper


class Gebiz(BaseScraper):
    def __init__(self, end_opp, end_page):
        super(Gebiz, self).__init__(
            link="https://www.gebiz.gov.sg/ptn/loginGeBIZID.xhtml",
            folder_id="1ckD74zWxLjDJSpNuJYu1MAQT1KtwlPrG",
            sheet_folder_id="1_3CkwtS6EMUdD3WRUQ7B3jhgUn3T1v-y",
            project="Gebiz",
            header=["Title", "Reference", "Reference number", "Agency", "Published", "Procurement type", "Category",
                    "Contact person", "Email", "Mobile phone number", "Address", "Found words", "Link to files"],
            end_opp=end_opp,
            end_page=end_page,
            username="301776080",
            password="TcoDevelopment"
        )

    def pagination(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        nav = self.driver.find_element_by_class_name("formRepeatPagination2_NAVIGATION-BUTTONS-DIV")
        nav.find_element_by_xpath("//*[@value='Next']").click()
        time.sleep(20)

    def login(self):
        time.sleep(5)
        user_box = self.driver.find_element_by_xpath("//*[@name='contentForm:j_idt140_inputText']")
        user_box.send_keys(self.username)
        password_box = self.driver.find_element_by_id('contentForm:password_inputText')
        password_box.send_keys(self.password)
        time.sleep(5)
        self.driver.find_element_by_id("contentForm:buttonSubmit").click()
        time.sleep(10)

    def opp_page(self):
        self.driver.find_element_by_id("contentForm:j_id56").click()
        time.sleep(5)

    def go_to_start_page(self):
        while self.start_page > self.at_page:
            self.pagination()
            self.at_page += 1

    def get_table(self):
        return self.driver.find_elements_by_class_name("commandLink_TITLE-BLUE")

    def click_links(self):
        tenders = self.get_table()
        reference = self.driver.find_elements_by_class_name("formSectionHeader6_TEXT")[self.at_opp].text
        title = tenders[self.at_opp].text
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        tenders[self.at_opp].click()
        time.sleep(10)
        data = self.extract_gebiz_info(title, reference)
        time.sleep(10)
        return data

    def try_extraction(self, xpath):
        try:
            extraction = self.driver.find_element_by_xpath(xpath).find_element_by_class_name(
                "formOutputText_VALUE-DIV ").text
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            extraction = None
        return extraction

    def extract_gebiz_info(self, title, reference):
        info_list = [title, reference, try_extraction(self.driver, "//span[text()='Reference No.']/../../../../.."),
                     try_extraction(self.driver, "//span[text()='Agency']/../../../../.."),
                     try_extraction(self.driver, "//span[text()='Published']/../../../../.."),
                     try_extraction(self.driver, "//span[text()='Procurement Type']/../../../../.."),
                     try_extraction(self.driver, "//span[text()='Procurement Category']/../../../../..")]

        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.find_element_by_class_name("formAttachmentsList_DOWNLOAD-BUTTON").click()
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)
            pass

        time.sleep(60)

        file_operator = HandleFiles(reference, doc_folder_id)
        file_operator.extract_files(["zip"])
        time.sleep(10)
        file_operator.read_pdfs()
        words = file_operator.read_docx()
        time.sleep(20)
        drive_link = file_operator.upload_files()
        time.sleep(20)
        file_operator.delete_all_files()
        contact_info = driver.find_element_by_xpath(
            "//*[text()='WHO TO CONTACT']/../../../../../../following-sibling::div").text.split("\n")
        i = 0
        if "PRIMARY" in contact_info[0]:
            i = 1

        info_list.append(contact_info[i])
        info_list.append(contact_info[i + 1])
        info_list.append(contact_info[i + 2])
        info_list.append(contact_info[-1])

        info_list.append(words)
        info_list.append(drive_link)

        return info_list

    def go_back(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element_by_xpath("//input[@value='Back to Search Results']").click()
