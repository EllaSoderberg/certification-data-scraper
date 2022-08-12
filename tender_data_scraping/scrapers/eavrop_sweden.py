from selenium.webdriver.common.by import By
import time
import logging
from datetime import datetime

from scraping_operations.scraping_machine import ScrapingMachine


class Eavrop(ScrapingMachine):
    def __init__(self):
        super(Eavrop, self).__init__(
            link="https://www.e-avrop.com/e-Upphandling/Default.aspx",
            doc_folder_id="1cn_Szi2FaMGuE8_xxxV747NDK_5WyEns",
            sheet_folder_id="1y6Jt75q_BUHCLpE_SV3U_0rGSQQKEaR_",
            project="Eavrop",
            data={"Title": None, "Reference": None, "Agency": None,
                  "Published": None, "Procurement type": None, "Main CPV": None, "Secondary CPV": None,
                  "Estimated value": None, "TCOC mentioned": None, "EPEAT mentioned": None,
                  "Keywords in files": None, "Link to files": None},
            username="annika.overodder@tcodevelopment.com",
            password="Upphandla2021",
        )

    def login(self):
        """
        Function to use the driver to log in to the database
        """
        self.driver.find_element(By.ID, "loginButton").click()
        login_fields = self.driver.find_element(By.ID, "loginPrompt")
        login_fields.find_element(By.XPATH, "*/input[@aria-label='Username']").send_keys(self.username)
        login_fields.find_element(By.ID, "Header1_LoginControl1_ctl04_password").send_keys(self.password)
        login_fields.find_element(By.ID, "verify").click()
        time.sleep(10)

    def go_to_database(self):
        """
        Function to go to the page where the database is found
        """
        self.driver.find_element(By.ID, "navigationContent_tenders").click()
        time.sleep(10)
        self.driver.find_element(By.CLASS_NAME, "cpvSearch").send_keys("30200000")
        self.driver.find_element(By.ID, "navigationContent_searchButton").click()
        time.sleep(10)

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
        return self.driver.find_elements(By.CLASS_NAME, "rowline")

    def go_to_tender(self, tender):
        """
        :return: dictionary with all the data with at least the values:
        {
        title:,
        date_published:,
        }
        """
        self.data["Title"] = self.driver.find_element(By.TAG_NAME, "a").text
        tender.find_element(By.TAG_NAME, "a").click()
        time.sleep(10)

        type = self.driver.find_element(By.CLASS_NAME, "navNodeCurrent").text
        if type == "RFI":
            self.data["Reference"] = self.data["Title"]
            self.data["Agency"] = self.driver.find_element(By.ID, "mainContent_RfiHead_Datalist1").text
            self.data["Published"] = self.driver.find_element(By.ID, "mainContent_RfiHead_UpdatedLabel").text.split("(")[0]
            self.data["Procurement type"] = self.driver.find_element(By.ID, "mainContent_RfiHead_SpecificationLabel").text
            self.data["Main CPV"] = self.driver.find_element(By.XPATH, "*/form/table/tbody/tr[6]/td").text
            full_text = self.driver.find_element(By.TAG_NAME, "body").text

        else:
            main_box = self.driver.find_element(By.ID, "container_mainContent_ContractNotice")
            self.data["Reference"] = main_box.find_element(By.XPATH, "*/form/div[5]/div/div/div/div[1]/span[1]/div/span").text
            self.data["Agency"] = main_box.find_element(By.XPATH, "*/form/div[5]/div/div/div/div[1]/span[2]/div/h3/span").text
            self.data["Published"] = main_box.find_element(By.XPATH, "*/form/div[5]/div/div/div/div[1]/span[4]/div[2]/div/div/span").text
            self.data["Procurement type"] = main_box.find_element(By.XPATH, "*/form/div[5]/div/div/div/div[1]/span[4]/div[1]/span").text
            self.data["Main CPV"] = main_box.find_element(By.CLASS_NAME, "cpv-code").text
            second_cpv = ""
            for cpv in main_box.find_elements(By.CLASS_NAME, "cpv-code")[1:]:
                second_cpv += cpv
                second_cpv += " "
            self.data["Secondary CPV"] = second_cpv
            full_text = main_box.text

        return self.data, full_text

    def documents_exist(self):
        """
        Check if there are any documents to download
        :return: True or False
        """
        try:
            self.driver.find_element(By.ID, "navigationContent_subscribeBtn")
            return False
        except Exception:
            return True

    def download_documents(self):
        """
        Download documents
        :return:
        """
        self.driver.find_element(By.ID, "mainContent_createZip").click()
        time.sleep(10)

    def go_back(self):
        """
        Go back to database page
        """
        self.driver.back()

    def pagination(self):
        """
        Paginate trough the pages
        """
        pass