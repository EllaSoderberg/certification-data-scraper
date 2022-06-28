import time
from datetime import datetime
import logging

from scraping_operations.scraping_machine import ScrapingMachine


class Evergabe(ScrapingMachine):
    def __init__(self):
        super(Evergabe, self).__init__(
            link="https://www.evergabe.nrw.de/VMPCenter/common/project/search.do?method=showExtendedSearch&fromExternal"
                 "=true#eyJjcHZDb2RlcyI6W3sibmFtZSI6IkFyYmVpdHNwbMOkdHplIiwiY29kZSI6IjMwMjE0MDAwLTIifSx7Im5hbWUiOiJCaWx"
                 "kc2NoaXJtZSIsImNvZGUiOiIzMDIzMTMwMC0wIn0seyJuYW1lIjoiQ29tcHV0ZXJiaWxkc2NoaXJtZSB1bmQgS29uc29sZW4iLCJj"
                 "b2RlIjoiMzAyMzEwMDAtNyJ9LHsibmFtZSI6IkZlcm5zcHJlY2hrb3BmaMO2cmVyZ2Fybml0dXJlbiIsImNvZGUiOiIzMjU1MTMwM"
                 "C0zIn0seyJuYW1lIjoiRmlsbXZvcmbDvGhyZ2Vyw6R0ZSIsImNvZGUiOiIzODY1MjAwMC0wIn0seyJuYW1lIjoiUGVyc29uYWxjb2"
                 "1wdXRlciIsImNvZGUiOiIzMDIxMzAwMC01In0seyJuYW1lIjoiVGFibGV0dGNvbXB1dGVyIiwiY29kZSI6IjMwMjEzMjAwLTcifSx"
                 "7Im5hbWUiOiJUYXNjaGVuY29tcHV0ZXIiLCJjb2RlIjoiMzAyMTM1MDAtMCJ9LHsibmFtZSI6IlRpc2NoY29tcHV0ZXIiLCJjb2Rl"
                 "IjoiMzAyMTMzMDAtOCJ9LHsibmFtZSI6IlRyYWdiYXJlIENvbXB1dGVyIiwiY29kZSI6IjMwMjEzMTAwLTYifV0sImNvbnRyYWN0a"
                 "W5nUnVsZXMiOlsiVk9MIiwiVk9CIiwiVlNWR1YiLCJTRUtUVk8iLCJPVEhFUiJdLCJwdWJsaWNhdGlvblR5cGVzIjpbIlRlbmRlci"
                 "JdLCJkaXN0YW5jZSI6MCwicG9zdGFsQ29kZSI6IiIsIm9yZGVyIjoiMCIsInBhZ2UiOiIxIiwic2VhcmNoVGV4dCI6IiIsInNvcnR"
                 "GaWVsZCI6IlBST0pFQ1RfUFVCTElDQVRJT05fREFURV9MTkcifQ",
            doc_folder_id="1zVLDxvny4kr5ZopfnPI2ATATq9yu3AOc",
            sheet_folder_id="1wfNNoTwJyXzCEIinJnRe8lLduMw1VAzd",
            project="Evergabe",
            data={"Reference": None, "Title": None, "Published": None, "Offizielle Bezeichnung": None,
                  "Kontaktstelle": None, "zu Händen von": None, "Telefon": None, "E-Mail": None,
                  "Internet-Adresse (URL)": None, "TCOC mentioned": "", "EPEAT mentioned": "",
                  "Keywords in description": "", "Keywords in documents": "", "Link to documents": None})
        self.handles = None

    def login(self):
        """
        Function to use the driver to log in to the database
        """
        pass

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
        table = self.driver.find_element_by_id("listTemplate")
        tbody = table.find_element_by_tag_name("tbody")
        row = tbody.find_elements_by_tag_name("tr")
        return row

    def go_to_tender(self, tender):
        """
        :return: dictionary with all the data with at least the values:
        {
        title:,
        date_published:,
        }
        """
        td = tender.find_elements_by_tag_name("td")
        published = datetime.strptime(td[0].text, "%d.%m.%Y").strftime("%Y-%m-%d")
        title = td[2].text
        tender.find_element_by_class_name("noTextDecorationLink").click()
        time.sleep(5)
        self.handles = self.driver.window_handles
        done, to_analyze = self.extract_info()
        while not done:
            time.sleep(15)
        self.data.update({"Title": title, "Published": published})
        return self.data, ""

    def extract_info(self):
        self.driver.switch_to.window(self.handles[-1])
        tenderid = self.try_extraction("//span[text()='Ausschreibungs-ID']/../../following-sibling::div")
        time.sleep(5)
        try:
            self.driver.find_element_by_xpath("//*[@href='./processdata']").click()
            time.sleep(5)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            pass
        finally:
            organization = self.try_extraction("//*[text()='Offizielle Bezeichnung']/following-sibling::div")
            contact = self.try_extraction("//*[text()='Kontaktstelle']/following-sibling::div")
            contact_person = self.try_extraction("//*[text()='zu Händen von']/following-sibling::div")
            phone = self.try_extraction("//*[text()='Telefon']/following-sibling::div")
            email = self.try_extraction("//*[text()='E-Mail']/following-sibling::div")
            web_address = self.try_extraction("//*[text()='Internet-Adresse (URL)']/following-sibling::div")
            to_analyze = self.driver.find_element_by_id("content").text

        self.data.update({"Reference": tenderid, "Offizielle Bezeichnung": organization, "Kontaktstelle": contact,
                          "zu Händen von": contact_person, "Telefon": phone, "E-Mail": email,
                          "Internet-Adresse (URL)": web_address})
        return True, to_analyze

    def try_extraction(self, xpath):
        try:
            extraction = self.driver.find_element_by_xpath(xpath).text
        except Exception as e:
            extraction = None
        return extraction

    def documents_exist(self):
        """
        Check if there are any documents to download
        """
        try:
            self.driver.find_element_by_xpath("//*[@href='./documents']").click()
            time.sleep(5)
        except Exception:
            return False
        return True

    def download_documents(self):
        """
        Download documents
        """
        self.driver.find_element_by_xpath("//*[@title='Alle Dokumente als ZIP-Datei herunterladen']").click()

    def go_back(self):
        self.driver.switch_to.window(self.handles[0])

