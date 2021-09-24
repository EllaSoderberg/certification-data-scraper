import time
import logging
from datetime import datetime

from scraping_operations.scraping_machine import ScrapingMachine


class Gebiz(ScrapingMachine):
    def __init__(self):
        super(Gebiz, self).__init__(
            link="https://www.gebiz.gov.sg/ptn/loginGeBIZID.xhtml",
            doc_folder_id="1ckD74zWxLjDJSpNuJYu1MAQT1KtwlPrG",
            sheet_folder_id="1_3CkwtS6EMUdD3WRUQ7B3jhgUn3T1v-y",
            project="Gebiz",
            data={"Title": None, "Reference": None, "Reference number": None, "Agency": None,
                  "Published": None, "Procurement type": None, "Category": None, "Contact person": None, "Email": None,
                  "Mobile phone number": None, "Address": None, "TCOC mentioned": "", "EPEAT mentioned": "",
                  "Keywords in description": "", "Keywords in documents": "", "Link to documents": None},
            username="301776080",
            password="TcoDevelopment2021",
        )
        self.start_page = 0

    def login(self):
        time.sleep(5)
        user_box = self.driver.find_element_by_xpath("//*[@name='contentForm:j_idt145_inputText']")
        user_box.send_keys(self.username)
        password_box = self.driver.find_element_by_id('contentForm:password_inputText')
        password_box.send_keys(self.password)
        time.sleep(5)
        self.driver.find_element_by_id("contentForm:buttonSubmit").click()
        time.sleep(10)

    def go_to_database(self):
        self.driver.find_element_by_id("contentForm:j_id58").click()
        time.sleep(5)

    def navigate_to_current_page(self):
        """
        If the script has previously failed, this function will go to the correct page.
        """
        while self.start_page < self.at_page:
            self.pagination()
            self.start_page += 1

    def find_final_page(self):
        """
        Function to find where the final page is.
        :return: final page as an int
        """
        # Since for Gebiz we will be looking for a final tender instead of a page, we return None
        return None

    def get_table(self):
        return self.driver.find_elements_by_class_name("commandLink_TITLE-BLUE")

    def go_to_tender(self, tender):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.data["Title"] = tender.text
        tender.click()
        time.sleep(10)
        self.extract_gebiz_info()
        time.sleep(10)
        return self.data, ""

    def pagination(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        nav = self.driver.find_element_by_class_name("formRepeatPagination2_NAVIGATION-BUTTONS-DIV")
        nav.find_element_by_xpath("//*[@value='Next']").click()
        time.sleep(20)

    def try_extraction(self, xpath):
        try:
            extraction = self.driver.find_element_by_xpath(xpath).find_element_by_class_name(
                "formOutputText_VALUE-DIV ").text
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            extraction = None
        return extraction

    def extract_gebiz_info(self):

        self.data["Reference"] = self.try_extraction("//span[text()='Quotation No.']/../../../../..")
        self.data["Reference number"] = self.try_extraction("//span[text()='Reference No.']/../../../../..")
        self.data["Agency"] = self.try_extraction("//span[text()='Agency']/../../../../..")
        self.data["Published"] = datetime.strptime(self.try_extraction("//span[text()='Published']/../../../../.."),
                                                   '%d %b %Y %I:%M%p').strftime("%Y-%m-%d")
        self.data["Procurement type"] = self.try_extraction("//span[text()='Procurement Type']/../../../../..")
        self.data["Category"] = self.try_extraction("//span[text()='Procurement Category']/../../../../..")

        contact_info = self.driver.find_element_by_xpath(
            "//*[text()='WHO TO CONTACT']/../../../../../../following-sibling::div").text.split("\n")
        i = 0
        if "PRIMARY" in contact_info[0]:
            i = 1

        self.data["Contact person"] = contact_info[i]
        self.data["Email"] = contact_info[i + 1]
        self.data["Mobile phone number"] = contact_info[i + 2]
        self.data["Address"] = contact_info[-1]

    def documents_exist(self):
        """
        Check if there are any documents to download
        """
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.find_element_by_class_name("formAttachmentsList_DOWNLOAD-BUTTON")
            return True
        except Exception as e:
            print(e)
            return False

    def download_documents(self):
        """
        Download documents
        """
        files = self.driver.find_elements_by_class_name("formAttachmentsList_DOCUMENT-LINK")
        for file in files:
            file.click()
        print("just clicked download")
        time.sleep(10)

    def go_back(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element_by_xpath("//input[@value='Back to Search Results']").click()
