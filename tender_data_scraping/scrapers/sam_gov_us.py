from selenium.common.exceptions import NoSuchElementException

import time
import re
import logging
from datetime import datetime

from scraping_operations.scraping_machine import ScrapingMachine


class SamGov(ScrapingMachine):
    def __init__(self):
        super(SamGov, self).__init__(
            link="https://sam.gov/search/?index=opp&page=1&sort=-relevance&sfm%5Bstatus%5D%5Bis_active%5D=true&sfm%5Bkeywords%5D%5B0%5D%5Bkey%5D=%22All-in-one%22&sfm%5Bkeywords%5D%5B0%5D%5Bvalue%5D=%22All-in-one%22&sfm%5Bkeywords%5D%5B1%5D%5Bkey%5D=laptop&sfm%5Bkeywords%5D%5B1%5D%5Bvalue%5D=laptop&sfm%5Bkeywords%5D%5B2%5D%5Bkey%5D=laptops&sfm%5Bkeywords%5D%5B2%5D%5Bvalue%5D=laptops&sfm%5Bkeywords%5D%5B3%5D%5Bkey%5D=hp&sfm%5Bkeywords%5D%5B3%5D%5Bvalue%5D=hp&sfm%5Bkeywords%5D%5B4%5D%5Bkey%5D=lenovo&sfm%5Bkeywords%5D%5B4%5D%5Bvalue%5D=lenovo&sfm%5Bkeywords%5D%5B5%5D%5Bkey%5D=acer&sfm%5Bkeywords%5D%5B5%5D%5Bvalue%5D=acer&sfm%5Bkeywords%5D%5B6%5D%5Bkey%5D=asus&sfm%5Bkeywords%5D%5B6%5D%5Bvalue%5D=asus&sfm%5Bkeywords%5D%5B7%5D%5Bkey%5D=epeat&sfm%5Bkeywords%5D%5B7%5D%5Bvalue%5D=epeat&sfm%5Bkeywords%5D%5B8%5D%5Bkey%5D=notebook&sfm%5Bkeywords%5D%5B8%5D%5Bvalue%5D=notebook&sfm%5Bkeywords%5D%5B9%5D%5Bkey%5D=aoc&sfm%5Bkeywords%5D%5B9%5D%5Bvalue%5D=aoc&sfm%5Bkeywords%5D%5B10%5D%5Bkey%5D=dell&sfm%5Bkeywords%5D%5B10%5D%5Bvalue%5D=dell&sfm%5Bkeywords%5D%5B11%5D%5Bkey%5D=casio&sfm%5Bkeywords%5D%5B11%5D%5Bvalue%5D=casio&sfm%5Bkeywords%5D%5B12%5D%5Bkey%5D=epson&sfm%5Bkeywords%5D%5B12%5D%5Bvalue%5D=epson&sfm%5Bkeywords%5D%5B13%5D%5Bkey%5D=headset&sfm%5Bkeywords%5D%5B13%5D%5Bvalue%5D=headset&sfm%5Bkeywords%5D%5B14%5D%5Bkey%5D=projectors&sfm%5Bkeywords%5D%5B14%5D%5Bvalue%5D=projectors&sfm%5Bkeywords%5D%5B15%5D%5Bkey%5D=notebooks&sfm%5Bkeywords%5D%5B15%5D%5Bvalue%5D=notebooks&sfm%5Bdates%5D%5BpublishedDate%5D%5BpublishedDateSelect%5D=pastWeek",
            doc_folder_id="1bupED_ONXjdQ7yhb_Q9denAHVVk3KCQh",
            sheet_folder_id="155JpRxPZv25UHq7gG-o3kOzDsy7VbS0u",
            project="SamGov",
            data={"Link": None, "Published": None, "Type": None, "Title": None, "Reference": None, "Agency": None,
                  "NAICS": None, "PSC": None, "Description": "", "Postal Address": None, "Contact Person": None,
                  "Phone number": None, "Email address": None, "TCOC mentioned": "", "EPEAT mentioned": "",
                  "Keywords in description": "", "Keywords in documents": "", "Link to documents": None}
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
        time.sleep(10)
        self.driver.find_element_by_xpath("//button[@aria-label='Close Modal']").click()
        time.sleep(10)

    def navigate_to_current_page(self):
        """
        If the script has previously restarted, this function will go to the correct page.
        """
        self.pagination()

    def find_final_page(self):
        """
        Function to find where the final page is.
        :return: final page as an int
        """
        page_count = self.driver.find_element_by_id("bottomPagination-currentPage")
        max_page = int(page_count.get_attribute("max"))
        return max_page

    def get_table(self):
        """
        Function to retrieve the table and return its elements
        :return: The elements of the table as a webdriver object
        """
        time.sleep(5)
        result = self.driver.find_element_by_tag_name("search-list-layout")
        return result.find_elements_by_tag_name("app-opportunity-result")

    def go_back(self):
        self.driver.get(self.current_link)
        time.sleep(15)

    def go_to_tender(self, tender):
        """
        :return: dictionary with all the data with at least the values:
        {
        title:,
        date_published:,
        }
        """
        self.driver.get(tender.find_element_by_tag_name("a").get_attribute("href"))
        time.sleep(10)
        info = self.extract_sam_info()
        return self.data, info

    def extract_sam_info(self):
        title = self.try_extraction(self.driver.find_element_by_xpath('//h1[@class="\'sam-ui-header"]'))
        reference_id = self.try_extraction(self.try_by_id("header-solicitation-number")
                                      .find_element_by_class_name("description"))
        try:
            description = self.try_extraction(
                self.try_by_id("description").find_element_by_class_name("ng-star-inserted"))
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            description = ""

        published = datetime.strptime(self.split_text(self.try_extraction(
            self.try_by_id("general-original-published-date"))), ' %b %d, %Y %H').strftime("%Y-%m-%d")
        gen_type = self.split_text(self.try_extraction(self.try_by_id("general-type")))
        agency = self.try_extraction(self.driver.find_element_by_xpath(
            "//*[text()=' Department/Ind. Agency ']/following-sibling::div"))
        naics = self.split_text(self.try_extraction(self.try_by_id("classification-naics-code")))
        pcs = self.split_text(self.try_extraction(self.try_by_id("classification-classification-code")))
        name = self.try_by_id("contact-primary-poc-full-name")
        email = self.try_extraction(self.try_by_id("contact-primary-poc-email"))

        if name is not None:
            name = name.text
        else:
            name = None
        phone = self.try_extraction(self.try_by_id("contact-primary-poc-phone"))
        contractor = self.try_by_id("-contracting-office")
        if contractor is not None:
            contractor = contractor.find_element_by_class_name("ng-star-inserted").text
        else:
            contractor = None

        self.data.update({"Link": self.driver.current_url, "Published": published, "Type": gen_type, "Title": title,
                          "Reference": reference_id, "Agency": agency, "NAICS": naics, "PSC": pcs,
                          "Description": description, "Postal Address": contractor, "Contact Person": name,
                          "Phone number": phone, "Email address": email})

        return description

    def try_by_id(self, id):
        try:
            result = self.driver.find_element_by_id(id)
        except NoSuchElementException:
            logging.error("Exception occurred", exc_info=True)
            result = None
        return result

    def try_extraction(self, query):
        try:
            extraction = query.text
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            extraction = None
        return extraction

    def split_text(self, ext):
        if ext is not None:
            result = ext.split(":")[1]
        return result

    def find_text(self, soup, regex):
        matchobj = re.search(regex, soup)
        if matchobj:
            item = matchobj.group()
        else:
            item = None
        return item

    def documents_exist(self):
        """
        Check if there are any documents to download
        :return: True or False
        """
        for height in range(10):
            print("scrolled")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/10*{});".format(height))
            time.sleep(2)
        try:
            self.driver.find_element_by_xpath("//a[@class='file-link ng-star-inserted']")
        except Exception:
            return False
        return True

    def download_documents(self):
        """
        Download documents
        :return:
        """
        file_links = self.driver.find_elements_by_xpath("//a[@class='file-link ng-star-inserted']")
        for file in file_links:
            file.click()

    def go_back(self):
        """
        Go back to database page
        """
        self.driver.get(self.get_current_link())
        self.driver.get(self.get_current_link())
        time.sleep(10)

    def pagination(self):
        """
        Paginate trough the pages
        """
        self.driver.get(self.get_current_link())
        time.sleep(10)

    def get_current_link(self):
        return "https://sam.gov/search/?index=opp&page={}&sort=-relevance&sfm%5Bstatus%5D%5Bis_active%5D=true&sfm%5Bkeywords%5D%5B0%5D%5Bkey%5D=%22All-in-one%22&sfm%5Bkeywords%5D%5B0%5D%5Bvalue%5D=%22All-in-one%22&sfm%5Bkeywords%5D%5B1%5D%5Bkey%5D=laptop&sfm%5Bkeywords%5D%5B1%5D%5Bvalue%5D=laptop&sfm%5Bkeywords%5D%5B2%5D%5Bkey%5D=laptops&sfm%5Bkeywords%5D%5B2%5D%5Bvalue%5D=laptops&sfm%5Bkeywords%5D%5B3%5D%5Bkey%5D=hp&sfm%5Bkeywords%5D%5B3%5D%5Bvalue%5D=hp&sfm%5Bkeywords%5D%5B4%5D%5Bkey%5D=lenovo&sfm%5Bkeywords%5D%5B4%5D%5Bvalue%5D=lenovo&sfm%5Bkeywords%5D%5B5%5D%5Bkey%5D=acer&sfm%5Bkeywords%5D%5B5%5D%5Bvalue%5D=acer&sfm%5Bkeywords%5D%5B6%5D%5Bkey%5D=asus&sfm%5Bkeywords%5D%5B6%5D%5Bvalue%5D=asus&sfm%5Bkeywords%5D%5B7%5D%5Bkey%5D=epeat&sfm%5Bkeywords%5D%5B7%5D%5Bvalue%5D=epeat&sfm%5Bkeywords%5D%5B8%5D%5Bkey%5D=notebook&sfm%5Bkeywords%5D%5B8%5D%5Bvalue%5D=notebook&sfm%5Bkeywords%5D%5B9%5D%5Bkey%5D=aoc&sfm%5Bkeywords%5D%5B9%5D%5Bvalue%5D=aoc&sfm%5Bkeywords%5D%5B10%5D%5Bkey%5D=dell&sfm%5Bkeywords%5D%5B10%5D%5Bvalue%5D=dell&sfm%5Bkeywords%5D%5B11%5D%5Bkey%5D=casio&sfm%5Bkeywords%5D%5B11%5D%5Bvalue%5D=casio&sfm%5Bkeywords%5D%5B12%5D%5Bkey%5D=epson&sfm%5Bkeywords%5D%5B12%5D%5Bvalue%5D=epson&sfm%5Bkeywords%5D%5B13%5D%5Bkey%5D=headset&sfm%5Bkeywords%5D%5B13%5D%5Bvalue%5D=headset&sfm%5Bkeywords%5D%5B14%5D%5Bkey%5D=projectors&sfm%5Bkeywords%5D%5B14%5D%5Bvalue%5D=projectors&sfm%5Bkeywords%5D%5B15%5D%5Bkey%5D=notebooks&sfm%5Bkeywords%5D%5B15%5D%5Bvalue%5D=notebooks&sfm%5Bdates%5D%5BpublishedDate%5D%5BpublishedDateSelect%5D=pastWeek".format(str(self.at_page + 1))

