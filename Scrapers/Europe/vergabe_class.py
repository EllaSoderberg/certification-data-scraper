import time
import os
from DataUploader import Sheet
from FileHandleler import HandleFiles
from ScrapingTools import read_write
from Scrapers.base_scraper import BaseScraper
import logging

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
            doc_folder_id="1zVLDxvny4kr5ZopfnPI2ATATq9yu3AOc",
            sheet_folder_id="1wfNNoTwJyXzCEIinJnRe8lLduMw1VAzd",
            project="Evergabe",
            header=["ID", "Title", "Offizielle Bezeichnung", "Kontaktstelle", "zu Händen von", "Telefon",
                    "E-Mail", "Internet-Adresse (URL)", "Keywords Found", "Link to folder"],
            end_opp=end_opp,
            end_page=end_page)
        self.handles = None

    def try_extraction(self, xpath):
        try:
            extraction = self.driver.find_element_by_xpath(xpath).text
        except Exception as e:
            extraction = None
        return extraction

    def get_table(self):
        table = self.driver.find_element_by_id("listTemplate")
        documents = table.find_elements_by_class_name("noTextDecorationLink")
        return documents

    def click_links(self):
        documents = self.get_table()
        documents[self.at_opp].click()
        self.handles = self.driver.window_handles
        done, info_list = self.extract_info()
        while not done:
            time.sleep(15)
        return info_list

    def extract_info(self):
        info_list = []
        self.driver.switch_to.window(self.handles[-1])
        title = self.try_extraction('//*[@id="projectRoomTitleText"]')
        tenderid = self.try_extraction("//span[text()='Ausschreibungs-ID']/../../following-sibling::div")
        time.sleep(5)
        try:
            self.driver.find_element_by_xpath("//*[@href='./processdata']").click()
            time.sleep(3)
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
        self.driver.switch_to.window(self.handles[0])

