import datetime
import time
import re
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from scraping_operations.scraping_machine import ScrapingMachine


class TED(ScrapingMachine):
    def __init__(self, sheet_folder_id="1LoN1ufjKEGyMhEtC-cGdUqDDE465DDml", project="TED"):
        super(TED, self).__init__(
            link="https://ted.europa.eu/TED/browse/browseByMap.do",
            doc_folder_id="",
            sheet_folder_id=sheet_folder_id,
            project=project,
            data={"Link": None, "Published": None, "Authority name": None, "Country": None,
                  # "Contact person", "E-mail", "Is duplicate",
                  "Website": None, "Title": None, "CPV": None, "Secondary CPV": None, "Type": None, "Total value": None,
                  "Award criteria": None, "EU funding": None, "Documents": None, "TCOC mentioned": "", "EPEAT mentioned": "",
                  "Keywords in description": "", "Keywords in documents": "", "Link to documents": None}
        )
        self.address = ""
        self.search = "PD=[{} <> {}] AND PC=[30231000 or 38652000 or 32551300 or 30214000 or 30213000 or 30213100 or " \
                      "30213200 or 30213300 or 30213500 or 32252000] AND TD=[3]".format((self.last_run + datetime.timedelta(days=1))
                                                                            .strftime("%Y%m%d"),
                                                                            self.today.strftime("%Y%m%d"))
        self.rlv_cpv_codes = ["30231000", "30214000", "30213000", "30213100",
                              "30213200", "30213300", "30213500", "38652000", "32551300"]

    def login(self):
        pass

    def go_to_database(self):
        # Wait for page to load
        time.sleep(5)
        # Click to accept cookies button
        cookie_button = self.driver.find_element(By.XPATH, '//*[@class="wt-link cck-actions-button"]')
        cookie_button.click()
        close_button = self.driver.find_element(By.XPATH, '//*[@href="#close"]')
        close_button.click()
        time.sleep(5)
        # Go to the expert search page
        expert_search = self.driver.find_element(By.XPATH, '//*[@title="Go to the expert search form"]')
        # expert_search = self.driver.find_element_by_xpath('//*[@title="Go to the expert search form"]')
        expert_search.click()
        # Wait for page to load
        time.sleep(5)
        # Find the text box and type in the search string
        text_box = self.driver.find_element(By.ID, 'expertSearchCriteria.query')
        text_box.send_keys(self.search)
        print(self.search)
        # Ensure all keys have been sent
        time.sleep(5)
        # Click search button
        search_button = self.driver.find_element(By.XPATH, '//*[@title="Perform search"]')
        search_button.click()
        time.sleep(2)
        # Save the current address
        self.address = self.driver.current_url

    def navigate_to_current_page(self):
        """
        If the script has previously failed, this function will go to the correct page.
        """
        if self.at_page > 0:
            self.pagination()

    def find_final_page(self):
        """
        Function to find where the final page is.
        :return: final page as an int
        """
        try:
            # Find the banner with all the page numbers
            page_links = self.driver.find_element(By.CLASS_NAME, "pagelinks")
            page_numbers = page_links.find_elements(By.CLASS_NAME, "pager-number")
            # Return the last page number
            final_page = page_numbers[-1].text
        except Exception:
            final_page = 1
        return final_page

    def get_table(self):
        return self.driver.find_elements(By.XPATH, "//*[@title='View this notice']")

    def documents_exist(self):
        """
        Check if there are any documents to download
        """
        # For the TED database there are no documents to download
        return False

    def download_documents(self):
        """
        Download documents
        """
        pass

    def go_back(self):
        """
        Go back to database page
        """
        pass

    def pagination(self):
        """
        Paginate trough the pages
        :return:
        """
        new_address = self.address + '?page=' + str(self.at_page)
        self.driver.get(new_address)

    def go_to_tender(self, tender):
        """
        :return: dictionary with all the data with at least the values:
        {
        title:,
        published_date:,
        }
        """
        # links = self.get_table()
        print("going to tender")
        return self.get_data(tender.get_attribute("href"))
        # return self.get_data(links[self.at_opp].get_attribute("href"))

    def get_data(self, link):

        # Get the link
        print("Getting link", link)
        link_html = requests.get(link)
        time.sleep(3)
        soup = BeautifulSoup(link_html.content, 'html.parser')
        print(soup)
        self.data["Link"] = link
        print(link)

        # Find date published
        self.data["Published"] = soup.find('span', class_="date").text

        print(self.data["Published"])
        # Get the info under headline Name and addresses
        try:
            contact_info = soup.find("span", string='Name and addresses').next_sibling.strings
        except Exception:
            contact_info = soup.find("span", string='Name, addresses and contact point(s)').next_sibling.strings

        name = None
        country = None
        responsible = None

        # Loop thought contact info
        for info in contact_info:
            name_found = re.search('Official name: ', info)
            if name_found is not None:
                name = info[name_found.span()[1]:]
            country_found = re.search('Country: ', info)
            if country_found is not None:
                country = info[country_found.span()[1]:]
            responsible_found = re.search('Contact person:', info)
            if responsible_found is not None:
                responsible = info[responsible_found.span()[1]:]

         # "Contact person", "E-mail", "Is duplicate",

        # Add contact info to document
        self.data["Authority name"] = name
        self.data["Country"] = country

        # Add email
        email = Nonepy 
        email = soup.find("a", class_='ojsmailto').string
        e_mail = email
        #self.data["email"] = email

        """
        # See if the contact is a duplicate
        is_duplicate = self.find_duplicates(e_mail)

        if is_duplicate:
            info_list.append("YES")
        else:
            info_list.append("NO")
        """

        # Add website
        website = None
        try:
            website = soup.find('a', class_="ojshref").text
        except AttributeError:
            pass

        self.data["Website"] = website


        # Find section two
        info = soup.find("span", id='id1-II.').parent.parent

        try:
            title = self.get_sibling(info, "Title:").text.strip()
        except Exception:
            title = " "

        self.data["Title"] = title

        # Find cpv code and add code and description
        cpv_codes = soup.find_all("span", class_="cpvCode")

        main_cpv = None
        main_cpv = cpv_codes[0].text

        self.data["CPV"] = main_cpv

        add_cpv = None
        add_cpv = ""
        for cpv in cpv_codes[1:]:
            add_cpv += cpv.text + ","
        self.data["Secondary CPV"] = add_cpv

        self.data["Type"] = soup.find("div", class_="DocumentBody").find("div", class_="stdoc").text
        print(self.data["Type"])

        # Find total value and add it
        try:
            total_value = self.get_sibling(info, 'Estimated total value')
            value = total_value.text
        except Exception:
            value = None

        self.data["Total value"] = value

        # Find, translate, write and save award criteria
        award_string = ""
        try:
            award_criteria = soup.find_all(
                "span", string='Award criteria')
            for award in award_criteria:
                awards = award.find_next_siblings("div")
                for a in awards:
                    eng = a.text
                    award_string += str(eng)
                    award_string += " "
        except Exception:
            award_string = None

        self.data["Award criteria"] = award_string

        # Analyze the Award criteria
        #info_list.append(analyze_text.analysis(award_string))

        # Find EU funds and add it
        try:
            eu_funds = self.get_sibling(
                info, 'Information about European Union funds')
            funds = eu_funds.text.split(":")[1]
        except Exception:
            funds = None

        self.data["EU funding"] = funds

        # Find and write website
        try:
            communication = soup.find(
                'span', string="Communication").next_sibling
            doc_link = communication.find('a', class_="ojshref").text
        except Exception:
            doc_link = None
        self.data["Documents"] = doc_link


        # Find if TCO is mentioned
        full_doc = soup.find(id="mainContent")

        return self.data, full_doc

    def get_sibling(self, parent, name):
        sibling = parent.find('span', string=name).next_sibling
        return sibling

    def find_text(self, soup, regex):
        print(str(soup(text=(re.compile(regex)))))
        matchobj = re.search(regex, str(soup(text=(re.compile(regex)))))
        if matchobj:
            item = matchobj.group()
        else:
            item = None
        return item


