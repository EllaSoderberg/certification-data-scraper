from FileHandleler import HandleFiles
import time
import re
import urllib.request
import shutil

from Scrapers.base_scraper import BaseScraper


class BidSearch(BaseScraper):
    def __init__(self, end_opp, end_page, at_opp=1, sheet_id=None):
        super(BidSearch, self).__init__(
            link="https://app.bidsearch.com/bids?alertId=601040e8bdfada0021033605&title=Search20210126",
            doc_folder_id="1LoX4ElhECIEUe06Dm6NNSBiNPcPfRtqV",
            sheet_folder_id="1JGKM0C-zAAc4etupLhnD36ULksil51VA",
            project="Bidsearch",
            header=["Link", "Reference number", "Due date", "State/Province", "Agency", "Title", "Description",
                    "Contact information", "TCO mentioned", "EPEAT mentioned", "Interesting words", "Link to files"],
            end_opp=end_opp,
            end_page=end_page,
            username="clare.hobby@tcodevelopment.com",
            password="tcod20$",
            sheet_id=sheet_id
        )
        self.at_opp = at_opp

    def pagination(self):
        pass

    def login(self):
        time.sleep(60)
        user_box = self.driver.find_element_by_id('ObservableObject@21.email')
        user_box.send_keys(self.username)
        password_box = self.driver.find_element_by_id('ObservableObject@21.password')
        password_box.send_keys(self.password)
        time.sleep(5)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(60)

    def get_table(self):
        time.sleep(30)
        table_parent = self.driver.find_element_by_class_name("chakra-table")
        tbody = table_parent.find_element_by_xpath("//tbody")
        return tbody.find_elements_by_xpath("//tr")

    def click_links(self):
        tenders = self.get_table()
        info_list, is_new = self.get_basic_info(tenders[self.at_opp].find_elements_by_xpath("//td")[self.at_opp*8:(self.at_opp + 1)*8])
        print(info_list, "ye")
        print("Is new", is_new)
        if is_new:
            link = tenders[0].find_elements_by_xpath("//td//a")[self.at_opp].get_attribute("href")
            print(link)
            self.driver.get(link)
            print("clicked(?)")
            time.sleep(20)
            data = self.extract_bidsearch_info([link] + info_list)
            print("this is the data", data)
            time.sleep(10)
            return data
        else:
            return None


    def get_basic_info(self, td):
        #for el in td:
         #   print(el.text)
        due = td[1].text
        name = td[2].text
        title = td[3].text
        description = td[4].text
        #website = td[4].text
        reference = td[5].text
        state = td[6].text
        new = td[7].text
        print(new)
        is_new = True
        if len(new) != 0:
            is_new = False
        return [reference, due, state, name, title, description], is_new

    def download_file(self, url):
        urllib.request.urlretrieve(url, "C:/Users/Movie Computer/{}".format(url.split("/")[-1]))

    def extract_bidsearch_info(self, info_list):
        print("yooo")


        text = self.driver.find_elements_by_xpath("//body//div")
        #contact_div = []
        email_addresses = []
        for div in text:
            for address in re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", div.text):
                email_addresses.append(address)
            #if "contact" in div.text.lower():
             #   contact_div.append(div.text)
        #print(contact_div[-1])
        print("before set", email_addresses)
        email_addresses = list(set(email_addresses))
        print("after set", email_addresses)

        description = ""
        for el in text:
            description += "{} ".format(el.text)

        if description is not None:
            find_tco = self.find_text(description.strip(), r'((Tco|TCO|tco).\w+|(\w+).(Tco|TCO|tco))')
            find_epeat = self.find_text(description.strip(), r'((Epeat|EPEAT|epeat).\w+|(\w+).(Epeat|EPEAT|epeat))')

        else:
            find_tco = "None"
            find_epeat = "None"

        email_string = ""
        if len(email_addresses) != 0:
            for email in email_addresses:
                email_string += email
                email_string += ", "

        full_info_list = info_list + [email_string, find_tco, find_epeat]

        file_endings = ["pdf", "doc", "docx"]

        try:
            #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(5)
            self.driver.find_element_by_xpath("//div/div/button[2]").click()
            files = self.driver.find_elements_by_xpath("//div/div/div/a/img")
            downl_f = False
            for file in files:
                file.click()
                downl_f = True

            if downl_f:
                time.sleep(60)
                file_operator = HandleFiles(info_list[1], self.doc_folder_id)
                file_operator.extract_files(["zip"])
                time.sleep(10)
                file_operator.read_pdfs()
                words = file_operator.read_docx()
                time.sleep(20)
                drive_link = file_operator.upload_files()
                time.sleep(20)
                file_operator.delete_all_files()
            else:
                words = "None"
                drive_link = "None"

            full_info_list.append(words)
            full_info_list.append(drive_link)
        except Exception as e:
            print(e)


        print(full_info_list)
        return full_info_list

    def go_back(self):
        self.driver.execute_script("window.history.go(-1)")
        time.sleep(20)

    def find_text(self, soup, regex):
        matchobj = re.search(regex, soup)
        if matchobj:
            item = matchobj.group()
        else:
            item = None
        return item