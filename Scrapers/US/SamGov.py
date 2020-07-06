from selenium.common.exceptions import NoSuchElementException

from ScrapingTools import read_write
from DataUploader import Sheet
from FileHandleler import HandleFiles
import time
import re
import winsound
from selenium import webdriver
import logging

from Scrapers.base_scraper import BaseScraper

class SamGov(BaseScraper):
    def __init__(self, end_opp, end_page):
        super(SamGov, self).__init__(
            link="https://beta.sam.gov/search?index=opp&sort=-relevance&page=1&keywords=%22all-in-one%22%20laptop%20laptops%20computer%20workstation%20hp%20philips%20dell%20lenovo%20desktop%20display&inactive_filter_values=false&naics=334&notice_type=k&opp_inactive_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_publish_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%222020-06-11%22,%22endDate%22:%222020-06-18%22%7D%7D&opp_modified_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_response_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&date_filter_index=0",
            folder_id="1bupED_ONXjdQ7yhb_Q9denAHVVk3KCQh",
            sheet_folder_id="155JpRxPZv25UHq7gG-o3kOzDsy7VbS0u",
            project="SamGov",
            header=["Link", "Published", "Type", "Title", "Notice ID", "Agency", "NAICS", "PSC", "Description",
              "Postal Address", "Contact Person", "Phone number", "Email address", "TCO mentioned",
              "EPEAT mentioned", "Interesting words", "Link to documents"],
            end_opp=end_opp,
            end_page=end_page)

    def pagination(self, driver):
        nav = self.driver.find_element_by_class_name("page-next")
        nav.click()
        time.sleep(10)

    def go_to_start_page(self):
        time.sleep(30)
        while self.start_page > self.at_page:
            pagination(driver)
            self.at_page += 1

    def get_table(self):
        result = self.driver.find_element_by_id("search-results")
        return result.find_elements_by_class_name("opportunity-title")

    def go_back(self):
        driver.execute_script("window.history.go(-1)")

    def click_links(self):
        opps = self.get_table()
        opps[self.at_opp].find_element_by_tag_name("a").click()
        time.sleep(10)
        info = extract_sam_info()
        self.go_back()
        return info

    def extract_sam_info(self):
        title = self.try_extraction(self.driver.find_element_by_xpath('//h1[@class="\'sam-ui-header"]'))
        reference_id = self.try_extraction(self.try_by_id("header-solicitation-number")
                                      .find_element_by_class_name("description"))
        try:
            description = self.try_extraction(
                self.try_by_id("description").find_element_by_class_name("ng-star-inserted"))
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            description = None
        published = self.split_text(self.try_extraction(self.try_by_id("general-original-published-date")))
        gen_type = self.split_text(self.try_extraction(self.try_by_id("general-type")))
        naics = self.split_text(self.try_extraction(self.try_by_id("classification-naics-code")))
        pcs = self.split_text(self.try_extraction(self.try_by_id("classification-classification-code")))
        name = self.try_by_id("contact-primary-poc-full-name")
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

        if description is not None:
            find_tco = self.find_text(description.strip(), r'((Tco|TCO|tco).\w+|(\w+).(Tco|TCO|tco))')
            find_epeat = self.find_text(description.strip(), r'((Epeat|EPEAT|epeat).\w+|(\w+).(Epeat|EPEAT|epeat))')
            if len(description) > 40000:
                description = description[:40000]
        else:
            find_tco = None
            find_epeat = None

        info = [self.driver.current_url,
                published,
                gen_type,
                title,
                reference_id,
                try_extraction(self.driver.find_element_by_xpath(
                    "//*[text()=' Department/Ind. Agency ']/following-sibling::div")),
                naics,
                pcs,
                description,
                contractor,
                name,
                phone,
                self.try_extraction(self.try_by_id("contact-primary-poc-email")),
                find_tco,
                find_epeat
                ]

        for height in range(10):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/{});".format(height))
            time.sleep(5)

        try:
            self.driver.find_element_by_xpath("//*[@class='fa fa-cloud-download']").click()
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)
            pass

        time.sleep(60)
        if reference_id is not None:
            folder_name = reference_id
        else:
            folder_name = title
        file_operator = HandleFiles(folder_name, folder_id)
        file_operator.extract_files(["zip"])
        time.sleep(10)
        file_operator.read_pdfs()
        words = file_operator.read_docx()
        time.sleep(20)
        drive_link = file_operator.upload_files()
        time.sleep(20)
        file_operator.delete_all_files()

        info.append(words)
        info.append(drive_link)

        return info

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




