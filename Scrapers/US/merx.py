from FileHandleler import HandleFiles
import time
import re
import urllib.request
import shutil

from Scrapers.base_scraper import BaseScraper


class Merx(BaseScraper):
    def __init__(self, end_opp, end_page, sheet_id=None):
        super(Merx, self).__init__(
            link="https://merx.com",
            doc_folder_id="18StvdkIgclwHxIA79tJvNsNaUnXa917f",
            sheet_folder_id="1rfGa51k5md7Zcupar7rtzQPju11w64nk",
            project="Merx",
            header=["Link", "Reference number", "Published", "Due date", "Agency", "Title", "Location", "Contact information",
                    "TCO mentioned", "EPEAT mentioned"],
            end_opp=end_opp,
            end_page=end_page,
            username="chobby1",
            password="tcodmerx",
            sheet_id=sheet_id
        )
        self.at_opp = 5

    def pagination(self):
        pass

    def login(self):
        self.driver.find_element_by_id("menu_mobileAvatarToggle").click()
        time.sleep(2)
        self.driver.find_element_by_id("mainHeader_btnLogin_mobile").click()
        time.sleep(15)
        user_box = self.driver.find_element_by_id('j_username')
        user_box.send_keys(self.username)
        password_box = self.driver.find_element_by_id('j_password')
        password_box.send_keys(self.password)
        time.sleep(5)
        self.driver.find_element_by_id('loginButton').click()
        time.sleep(20)
        self.driver.find_element_by_name("ContinueButton").click()
        time.sleep(20)

    def click_links(self):
        tenders = self.driver.find_elements_by_class_name("mets-table-row")
        title = tenders[self.at_opp].find_element_by_class_name("solicitationTitle").text
        org = tenders[self.at_opp].find_element_by_class_name("buyerIdentification").text
        closing_date = tenders[self.at_opp].find_element_by_class_name("dateValue").text
        pub_date = tenders[self.at_opp].find_element_by_class_name("publicationDate").text.split(" ")[-1]
        location = tenders[self.at_opp].find_element_by_class_name("regionValue").text
        data = [pub_date, closing_date, org, title, location]
        tenders[self.at_opp].find_element_by_tag_name("a").click()
        print("clicked(?)")
        time.sleep(20)
        start, end = self.extract_info()
        data = start + data + end
        self.go_back()
        return data

    def download_file(self, url):
        urllib.request.urlretrieve(url, "C:/Users/Movie Computer/{}".format(url.split("/")[-1]))

    def extract_info(self):
        link = self.driver.current_url
        reference = self.driver.find_element_by_xpath('//span[contains(string(), "Reference")]/following-sibling::div').text
        contact = self.driver.find_element_by_xpath('//h3[contains(string(), "Contact")]/following-sibling::div').text

        try:
            self.driver.find_element_by_id("descriptionTextReadMore").click()
        except:
            pass

        description = self.driver.find_element_by_class_name("description").text
        print(description)

        if description is not None:
            find_tco = self.find_text(description.strip(), r'((Tco|TCO|tco).\w+|(\w+).(Tco|TCO|tco))')
            find_epeat = self.find_text(description.strip(), r'((Epeat|EPEAT|epeat).\w+|(\w+).(Epeat|EPEAT|epeat))')

        else:
            find_tco = None
            find_epeat = None

        return [link, reference], [contact, find_tco, find_epeat]



    def go_back(self):
        self.driver.get("https://www.merx.com/private/supplier/solicitations/search")
        time.sleep(20)

    def find_text(self, soup, regex):
        matchobj = re.search(regex, soup)
        if matchobj:
            item = matchobj.group()
        else:
            item = None
        return item