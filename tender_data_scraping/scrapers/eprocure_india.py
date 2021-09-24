import logging
import time
from datetime import datetime

from bs4 import BeautifulSoup

from scraping_operations.scraping_machine import ScrapingMachine


class Eprocure(ScrapingMachine):
    def __init__(self):
        super(Eprocure, self).__init__(
            link="https://eprocure.gov.in/cppp/searchbyproduct/byUjI5dlpITT1BMTNoMVEyOXRjSFYwWlhJZ1NHRnlaSGRoY21VPUExM2gxY0hWaWJHbHphR1ZrWDJSaGRHVT1BMTNoMWMyRnNkQT09",
            doc_folder_id="1ZiyNH8ADT4rQsOv0qaX9IY_-LgtwucIU",
            sheet_folder_id="1Q9dT-AaNlExuFZMtkn2WPRFWzdye0KWy",
            project="Eprocure",
            data={"Published": None, "Organisation Name": None, "Title": None, "Reference": None,
                  "Product Category": None, "Product Sub-Category": None, "Description": None, "TCOC mentioned": "",
                  "EPEAT mentioned": "", "Keywords in description": "", "Keywords in documents": "",
                  "Link to documents": None}
        )
        self.start_page = 0
        self.new_link = self.link + "?page={}".format(self.at_page)

    def login(self):
        """
        Function to use the driver to log in to the database
        """
        pass

    def go_to_database(self):
        """
        Function to go to the page where the database is found
        """
        self.driver.get(self.new_link)

    def navigate_to_current_page(self):
        """
        If the script has previously restarted, this function will go to the correct page.
        """
        while self.start_page < self.at_page:
            self.pagination()
            self.start_page += 1
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
        table = self.driver.find_element_by_tag_name("tbody")
        t_rows = table.find_elements_by_tag_name("tr")
        return t_rows

    def go_to_tender(self, tender):
        """
        :return: dictionary with all the data with at least the values:
        {
        title:,
        date_published:,
        }
        """
        columns = tender.find_elements_by_tag_name("td")
        columns[4].find_element_by_tag_name("a").click()
        captcha = self.driver.find_element_by_xpath("//img[@title='Image CAPTCHA']").get_attribute("alt")
        self.driver.find_element_by_id("edit-captcha-response").send_keys(captcha)
        time.sleep(10)
        self.driver.find_element_by_id("edit-save").click()
        time.sleep(10)
        data = self.get_data()
        return data, ""

    def documents_exist(self):
        """
        Check if there are any documents to download
        :return: True or False
        """
        details = self.driver.find_elements_by_id("tenderDetailDivTd")
        for detail in details:
            try:
                doc_link = detail.find_element_by_tag_name("a").click()
            except Exception:
                pass

        time.sleep(20)

        try:
            self.driver.find_element_by_xpath("//*[contains(text(), 'Download as zip file')]")
            return True
        except Exception:
            return False

    def download_documents(self):
        """
        Download documents
        :return:
        """

        self.driver.find_element_by_xpath("//*[contains(text(), 'Download as zip file')]").click()

        try:
            self.driver.find_element_by_xpath("//button[@id='captcha']")
        except Exception:
            pass
        else:
            self.warning_sound()
            time.sleep(20)
            self.driver.find_element_by_xpath("//*[contains(text(), 'Download as zip file')]").click()

    def go_back(self):
        """
        Go back to database page
        """
        self.driver.get(self.new_link)

    def pagination(self):
        """
        Paginate trough the pages
        """
        self.new_link = self.link + "?page={}".format(self.at_page)
        self.driver.get(self.new_link)

    def get_data(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        published_date = datetime.strptime(soup.find('td', string="ePublished Date").find_next_siblings(width="20%")[0]
                                           .text.strip(), '%d-%b-%Y %I:%M %p').strftime("%Y-%m-%d")
        org_name = soup.find('td', string="Organisation Name").find_next_siblings(id="tenderDetailDivTd")[0].text.strip()
        title = soup.find('td', string="Tender Title").find_next_siblings(id="tenderDetailDivTd")[0].text.strip()
        reference_number = soup.find('td', string="Tender Reference Number").find_next_siblings(width="20%")[0].text.strip()
        product_category = soup.find('td', string="Product Category").find_next_siblings(width="20%")[0].text.strip()
        sub_category = soup.find('td', string="Product Sub-Category").find_next_siblings(width="20%")[0].text.strip()
        description = soup.find('td', string="Work Description").find_next_siblings(id="tenderDetailDivTd")[0].text.strip()

        self.data.update({"Published": published_date, "Organisation Name": org_name, "Title": title,
                          "Reference": reference_number, "Product Category": product_category,
                          "Product Sub-Category": sub_category, "Description": description})

        time.sleep(20)
        return self.data

