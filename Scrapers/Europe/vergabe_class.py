import time
import os
from DataUploader import Sheet
from FileHandleler import HandleFiles
from ScrapingTools import read_write
from Scrapers.base_scraper import BaseScraper


class Evergabe(BaseScraper):
    def __init__(self, end_opp, end_page):
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
            folder_id="1zVLDxvny4kr5ZopfnPI2ATATq9yu3AOc",
            sheet_folder_id="1wfNNoTwJyXzCEIinJnRe8lLduMw1VAzd",
            project="Evergabe",
            header=["ID", "Title", "Offizielle Bezeichnung", "Kontaktstelle", "zu Händen von", "Telefon",
                    "E-Mail", "Internet-Adresse (URL)", "Keywords Found", "Link to folder"],
            end_opp=end_opp,
            end_page=end_page)

    def try_extraction(self, xpath):
        try:
            extraction = self.driver.find_element_by_xpath(xpath).text
        except Exception as e:
            extraction = None
        return extraction

    def get_table(self):
        return self.driver.find_element_by_id("listTemplate")

    def click_links(self):
        table = self.get_table()
        documents = table.find_elements_by_class_name("noTextDecorationLink")
        documents[self.at_opp].click()
        handles = self.driver.window_handles
        done, info_list = extract_info(handles)
        while not done:
            time.sleep(15)
        return info_list

    def extract_info(self, handles):
        info_list = []
        self.driver.switch_to.window(handles[-1])
        title = try_extraction(self.driver, '//*[@id="projectRoomTitleText"]')
        tenderid = try_extraction(self.driver, "//span[text()='Ausschreibungs-ID']/../../following-sibling::div")
        time.sleep(5)
        try:
            self.driver.find_element_by_xpath("//*[@href='./processdata']").click()
            time.sleep(3)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            pass
        finally:
            organization = try_extraction(self.driver, "//*[text()='Offizielle Bezeichnung']/following-sibling::div")
            contact = try_extraction(self.driver, "//*[text()='Kontaktstelle']/following-sibling::div")
            contact_person = try_extraction(self.driver, "//*[text()='zu Händen von']/following-sibling::div")
            phone = try_extraction(self.driver, "//*[text()='Telefon']/following-sibling::div")
            email = try_extraction(self.driver, "//*[text()='E-Mail']/following-sibling::div")
            web_address = try_extraction(self.driver, "//*[text()='Internet-Adresse (URL)']/following-sibling::div")
        try:
            self.driver.find_element_by_xpath("//*[@href='./documents']").click()
            time.sleep(3)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            pass
        else:
            self.driver.find_element_by_xpath("//*[@title='Alle Dokumente als ZIP-Datei herunterladen']").click()

        info_list.append(tenderid)
        info_list.append(title)
        info_list.append(organization)
        info_list.append(contact)
        info_list.append(contact_person)
        info_list.append(phone)
        info_list.append(email)
        info_list.append(web_address)

        time.sleep(20)

        file_operator = HandleFiles(tenderid, self.doc_folder_id)
        file_operator.extract_files(["zip"])
        info_list.append(file_operator.read_pdfs())
        info_list.append(file_operator.upload_files())
        file_operator.delete_all_files()

        return True, info_list

    def go_back(self):
        self.driver.switch_to.window(handles[0])

