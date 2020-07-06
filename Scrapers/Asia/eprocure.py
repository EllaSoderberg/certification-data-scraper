import logging
import time

from FileHandleler import HandleFiles
from bs4 import BeautifulSoup

from Scrapers.base_scraper import BaseScraper


class Eprocure(BaseScraper):
    def __init__(self, end_opp, end_page):
        super(Eprocure, self).__init__(
            link="https://eprocure.gov.in/cppp/searchbyproduct/byUjI5dlpITT1BMTNoMVEyOXRjSFYwWlhJZ1NHRnlaSGRoY21VPUExM2"
                 "gxY0hWaWJHbHphR1ZrWDJSaGRHVT1BMTNoMWMyRnNkQT09",
            folder_id="1ZiyNH8ADT4rQsOv0qaX9IY_-LgtwucIU",
            sheet_folder_id="1Q9dT-AaNlExuFZMtkn2WPRFWzdye0KWy",
            project="Eprocure-India",
            header=["Date published", "Organisation Name", "Tender Title", "Reference Number", "Product Category",
                    "Product Sub-Category", "Description", "Keywords", "Found", "Link to folder"],
            end_opp=end_opp,
            end_page=end_page)
        self.new_link = self.link + "?page={}".format(self.at_page)

    def go_to_start_page(self):
        self.driver.get(self.new_link)

    def get_table(self):
        table = self.driver.find_element_by_tag_name("tbody")
        t_rows = table.find_elements_by_tag_name("tr")
        return t_rows

    def click_links(self):
        t_rows = self.get_table()
        columns = t_rows[self.at_opp].find_elements_by_tag_name("td")
        columns[4].find_element_by_tag_name("a").click()
        self.warning_sound()
        time.sleep(20)
        data = self.get_data()
        return data

    def go_back(self):
        self.driver.get(self.new_link)

    def pagination(self):
        self.new_link = self.link + "?page={}".format(self.at_page)
        self.driver.get(self.new_link)

    def get_data(self):
        info_list = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        info_list.append(soup.find('td', string="ePublished Date").find_next_siblings(width="20%")[0].text.strip())
        info_list.append(soup.find('td', string="Organisation Name").find_next_siblings(id="tenderDetailDivTd")[0]
                         .text.strip())
        info_list.append(
            soup.find('td', string="Tender Title").find_next_siblings(id="tenderDetailDivTd")[0].text.strip())

        reference_number = soup.find('td', string="Tender Reference Number").find_next_siblings(width="20%")[
            0].text.strip()
        info_list.append(reference_number)
        info_list.append(soup.find('td', string="Product Category").find_next_siblings(width="20%")[0].text.strip())
        info_list.append(soup.find('td', string="Product Sub-Category").find_next_siblings(width="20%")[0].text.strip())
        info_list.append(soup.find('td', string="Work Description").find_next_siblings(id="tenderDetailDivTd")[0]
                         .text.strip())

        link_text = soup.find('td', string="Tender Document").find_next_siblings(id="tenderDetailDivTd")[0].text.strip()
        if "FrontEndTenderDetailsExternal" in link_text:
            self.download(link_text)
            file_operator = HandleFiles(reference_number, self.folder_id)
            file_operator.extract_files(["zip"])
            info_list.append(file_operator.read_pdfs())
            info_list.append(file_operator.upload_files())
            file_operator.delete_all_files()
        else:
            logging.info("This tender does not have any files")
            info_list.append(None)
            info_list.append(None)

        self.go_back()
        time.sleep(20)
        return info_list

    def download(self, link_text):
        self.driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(link_text)).click()
        try:
            self.driver.find_element_by_xpath("//*[contains(text(), 'Download as zip file')]").click()
            try:
                self.driver.find_element_by_xpath("//button[@id='captcha']")
            except Exception:
                logging.error("Exception occurred", exc_info=True)
                pass
            else:
                self.warning_sound()
                time.sleep(20)
                self.driver.find_element_by_xpath("//*[contains(text(), 'Download as zip file')]").click()

            self.driver.find_element_by_xpath("//*[contains(text(), 'Tendernotice_1')]").click()
            time.sleep(20)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            pass
