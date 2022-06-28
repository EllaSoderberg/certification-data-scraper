import re
import time
from datetime import datetime
from scraping_operations.scraping_machine import ScrapingMachine


class Tendium(ScrapingMachine):
    def __init__(self):
        super(Tendium, self).__init__(
            link="https://app.tendeye.com/auth/sign-in",
            doc_folder_id="1kaLIvIfHqnxWzWmaz-TOZnhQ7EmwvvlG",
            sheet_folder_id="1ykLGk7wWPNm9Pm03F68Ht_rpTOdB5zdS",
            project="Tendium",
            data={"Title": None, "Reference": None, "Published": None, "Description": None,
                  "Agency": None, "CPV": None, "TCO Certified mentioned": None},
            username="ella.soderberg@tcodevelopment.com",
            password="6ehqzQhXByvVyQh",
        )
        self.url = ""

    def login(self):
        """
        Function to use the driver to log in to the database
        """
        self.driver.find_element_by_id("email").send_keys(self.username)
        self.driver.find_element_by_id("password").send_keys(self.password)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()

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
        return self.driver.find_elements_by_class_name("ant-table-row")

    def go_to_tender(self, tender):
        """
        :return: dictionary with all the data with at least the values:
        {
        title:,
        date_published:,
        }
        """
        tender = self.get_table()[0]
        title = tender.find_elements_by_class_name("ant-table-cell")[4]
        self.data["Title"] = title.text
        title.click()
        time.sleep(2)
        self.driver.find_element_by_class_name("ProcurementPreview_reportButton__3RnZ0").click()
        time.sleep(5)
        reference = self.get_sibling_text("Reference-ID")
        published_text = self.get_sibling_text("Published")
        date = re.search(r"\d{1,2} \w+ \d{4}", published_text).group()
        published = datetime.strptime(date, '%d %B %Y').strftime("%Y-%m-%d")
        agency = self.get_sibling_text("Procuring agency")
        description = self.get_sibling_text("Short description")
        #cpv = self.get_sibling_text("Published")
        self.data.update({"Reference": reference, "Published": published, "Description": description,
                "Agency": agency})# "CPV": cpv})
        print(reference)
        self.url = self.driver.current_url
        print(self.url)
        self.driver.get(self.url + "&activeCategory=documentsSearch")
        time.sleep(10)
        occurances_str = self.driver.find_element_by_class_name("styles_occurrences__h5UNU").text
        occurances_int = int(''.join(x for x in occurances_str if x.isdigit()))
        print(occurances_int)
        if occurances_int != 0:
            self.data["TCO Certified mentioned"] = True
        else:
            self.data["TCO Certified mentioned"] = False

        self.driver.get(self.url + "&activeCategory=description")
        time.sleep(3)

        self.driver.find_element_by_class_name("WorkspaceSelect_wsActionButton__3x5_M").click()
        if self.data["TCO Certified mentioned"]:
            self.driver.find_element_by_xpath("//div[@label='Mentions TCO Certified']").click()
        else:
            self.driver.find_element_by_xpath("//div[@label='No mention TCO Certified']").click()
        time.sleep(2)
        return self.data, ""

    def get_sibling_text(self, title):
        text = ""
        try:
            text = self.driver.find_element_by_xpath("//*[contains(text(), '{}')]/../following-sibling::div".format(title)).text
        except Exception:
            pass
        return text

    def documents_exist(self):
        """
        Check if there are any documents to download
        :return: True or False
        """
        self.driver.get(self.url + "&activeCategory=documents")
        time.sleep(5)
        try:
            self.driver.find_elements_by_class_name("ProcurementFiles_button__2g29R")
            return True
        except Exception:
            return False

    def download_documents(self):
        """
        Download documents
        :return:
        """
        time.sleep(20)
        self.driver.find_element_by_xpath("//span[contains(text(), 'Download all documents')]").click()
        time.sleep(5)
        pass

    def go_back(self):
        """
        Go back to database page
        """
        self.driver.find_element_by_class_name("anticon-left-circle").click()
        time.sleep(20)
        pass

    def pagination(self):
        """
        Paginate trough the pages
        """
        pass

