import time
from datetime import datetime

from scraping_operations.scraping_machine import ScrapingMachine


class Merx(ScrapingMachine):
    def __init__(self):
        super(Merx, self).__init__(
            link="https://merx.com",
            doc_folder_id="18StvdkIgclwHxIA79tJvNsNaUnXa917f",
            sheet_folder_id="1rfGa51k5md7Zcupar7rtzQPju11w64nk",
            project="Merx",
            data={"Link": None, "Title": None, "Reference": None, "Published": None, "Due date": None, "Agency": None,
                  "Location": None, "Contact information": None, "TCOC mentioned": "", "EPEAT mentioned": "",
                  "Keywords in description": "", "Keywords in documents": "", "Link to documents": None},
            username="chobby1",
            password="tcodmerx",
        )
        self.start_page = 0

    def login(self):
        """
        Function to use the driver to log in to the database
        """
        self.driver.find_element_by_id("menu_mobileAvatarToggle").click()
        time.sleep(2)
        self.driver.find_element_by_id("mainHeader_btnLogin_mobile").click()
        time.sleep(10)
        user_box = self.driver.find_element_by_id('j_username')
        user_box.send_keys(self.username)
        password_box = self.driver.find_element_by_id('j_password')
        password_box.send_keys(self.password)
        time.sleep(5)
        self.driver.find_element_by_id('loginButton').click()
        time.sleep(10)
        #self.driver.find_element_by_name("ContinueButton").click()
        #time.sleep(10)

    def go_to_database(self):
        """
        Function to go to the page where the database is found
        """
        pass

    def navigate_to_current_page(self):
        """
        If the script has previously restarted, this function will go to the correct page.
        """
        while self.start_page < self.at_page:
            self.pagination()
            self.start_page += 1

    def find_final_page(self):
        """
        Function to find where the final page is.
        :return: final page as an int
        """
        return int(self.driver.find_element_by_xpath("//a[@class='last mets-pagination-page-icon']")
                   .get_attribute("data-page-number"))

    def get_table(self):
        """
        Function to retrieve the table and return its elements
        :return: The elements of the table as a webdriver object
        """
        table = self.driver.find_element_by_id("solicitationsTable")
        return table.find_elements_by_tag_name("tr")

    def go_to_tender(self, tender):
        """
        :return: dictionary with all the data with at least the values:
        {
        title:,
        date_published:,
        }
        """
        title = tender.find_element_by_class_name("solicitationTitle").text
        organisation = tender.find_element_by_class_name("buyerIdentification").text
        closing_date = tender.find_element_by_class_name("dateValue").text
        pub_date = datetime.strptime(tender.find_element_by_class_name("publicationDate").text.split(" ")[-1],
                                     '%Y/%m/%d').strftime("%Y-%m-%d")
        location = tender.find_element_by_class_name("regionValue").text

        print("clicking tender!!")
        tender.find_element_by_class_name("solicitationTitle").click()
        time.sleep(10)

        link = self.driver.current_url
        try:
            reference = self.driver.find_element_by_xpath(
                '//span[contains(string(), "Reference")]/following-sibling::div').text
            contact = self.driver.find_element_by_xpath('//h3[contains(string(), "Contact")]/following-sibling::div').text

            try:
                self.driver.find_element_by_id("descriptionTextReadMore").click()
            except Exception:
                pass

            description = self.driver.find_element_by_id("descriptionText").text
        except Exception:
            time.sleep(60)

        self.data.update({"Link": link, "Title": title, "Reference": reference, "Published": pub_date,
                          "Due date": closing_date, "Agency": organisation, "Location": location,
                          "Contact information": contact})

        return self.data, description

    def documents_exist(self):
        """
        Check if there are any documents to download
        :return: True or False
        """
        try:
            self.driver.find_element_by_xpath("//a[@title='Documents']").click()
            time.sleep(5)
            document_table = self.driver.find_element_by_class_name("solicitationDocumentsTable")
            document_table.find_elements_by_tag_name("a")
        except Exception:
            return False
        return True

    def download_documents(self):
        """
        Download documents
        :return:
        """
        document_table = self.driver.find_element_by_class_name("solicitationDocumentsTable")
        for doc in document_table.find_elements_by_tag_name("a"):
            doc.click()

    def go_back(self):
        """
        Go back to database page
        """
        self.driver.get("https://www.merx.com/private/supplier/solicitations/search")
        time.sleep(20)

    def pagination(self):
        """
        Paginate trough the pages
        """
        self.driver.find_element_by_xpath('//a[@class ="next mets-pagination-page-icon"]').click()
