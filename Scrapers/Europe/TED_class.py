from ScrapingTools import translater, analyze_text
import time
import re
import requests
from bs4 import BeautifulSoup

from Scrapers.base_scraper import BaseScraper

class TED(BaseScraper):
    def __init__(self, end_page):
        super(TED, self).__init__(
            link="https://ted.europa.eu/TED/browse/browseByMap.do",
            sheet_folder_id="1LoN1ufjKEGyMhEtC-cGdUqDDE465DDml",
            doc_folder_id="",
            project="TED",
            header=["Link", "Date published", "Authority name", "Country", "Contact person", "E-mail", "Is duplicate",
                    "Website", "Title", "CPV", "Secondary CPV", "Total value", "Award criteria",
                    "Found words", "EU funding", "Documents", "TCOC mentioned", "EPEAT mentioned"],
            end_opp=10,
            end_page=end_page)
        self.search = "PD=[{}] AND PC=[30231000 or 38652000 or 32551300 or 30214000 or 30213000 or 30213100 or " \
                      "30213200 or 30213300 or 30213500] AND TD=[3]".format("20200620 <> 20200626")
        self.rlv_cpv_codes = ["30231000", "30214000", "30213000", "30213100",
                              "30213200", "30213300", "30213500", "38652000", "32551300"]
        self.interesting_words = ["energy", "efficiency", "environment", "environmental", "tco", "sustainability",
                                  "life", "cycle",
                                  "ergonomic", "ecological", "circular", "economy", "circulaire", "economie",
                                  "certification",
                                  "certificates"]
        self.address = ""

    def go_to_start_page(self):
        time.sleep(5)
        search_box = self.driver.find_element_by_xpath(
            '//*[@title="Go to the expert search form"]')
        search_box.click()
        text_box = self.driver.find_element_by_id('expertSearchCriteria.query')
        time.sleep(5)
        text_box.send_keys(self.search)

        time.sleep(5)
        search_button = self.driver.find_element_by_xpath(
            '//*[@title="Perform search"]')
        search_button.click()
        time.sleep(2)

        self.address = self.driver.current_url

    def pagination(self):
        new_address = self.address + '?page=' + str(self.at_page)
        self.driver.get(new_address)

    def get_table(self):
        return self.driver.find_elements_by_xpath("//*[@title='View this notice']")

    def click_links(self):
        links = self.get_table()
        self.get_data(links[self.at_opp].get_attribute("href"))

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

    def get_data(self, link):
        info_list = []

        # Get the link
        link_html = requests.get(link)
        soup = BeautifulSoup(link_html.content, 'html.parser')
        info_list.append(link)

        # Find date published
        date = soup.find('span', class_="date").text
        info_list.append(date)

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

        # Add contact info to document
        info_list.append(name)
        info_list.append(country)
        info_list.append(responsible)

        # Add email
        email = None
        email = soup.find("a", class_='ojsmailto').string
        e_mail = email
        info_list.append(email)

        # See if the contact is a duplicate
        is_duplicate = False


        """
        for contact in contact_list:
            if e_mail[3:-3] in contact:
                is_duplicate = True
        """

        #new_contacts.append(e_mail)

        if is_duplicate:
            info_list.append("YES")
        else:
            info_list.append("NO")

        # Add website
        website = None

        website = soup.find('a', class_="ojshref").text
        info_list.append(website)

        # Find section two
        info = soup.find("span", id='id1-II.').parent.parent
        print("time to translate")

        transl = translater.Trans()
        # Get the title of the project
        try:
            title = self.get_sibling(info, "Title:").text.strip()
        except Exception:
            title = " "

        try:
            # Translate title to english and add to file
            eng_title = transl.translate(title).replace(";", ",")
        except Exception:
            eng_title = title

        info_list.append(eng_title)
        print("title found")

        # Find cpv code and add code and description
        cpv_codes = soup.find_all("span", class_="cpvCode")
        print(cpv_codes)

        main_cpv = None
        main_cpv = cpv_codes[0].text
        print(main_cpv)

        info_list.append(main_cpv)

        add_cpv = None
        add_cpv = ""
        for cpv in cpv_codes[1:]:
            add_cpv += cpv.text + ","
        print(add_cpv)
        info_list.append(add_cpv)

        # Find total value and add it
        try:
            total_value = self.get_sibling(info, 'Estimated total value')
            value = total_value.text
        except Exception:
            value = None

        info_list.append(value)

        # Find, translate, write and save award criteria
        award_string = ""
        try:
            award_criteria = soup.find_all(
                "span", string='Award criteria')
            print(award_criteria)
            for award in award_criteria:
                awards = award.find_next_siblings("div")
                print(awards)
                for a in awards:
                    try:
                        eng = transl.translate(a.text)
                    except Exception:
                        eng = a.text
                    award_string += str(eng)
                    award_string += " "
        except Exception:
            award_string = None

        print(award_string)
        info_list.append(award_string)

        # Analyze the Award criteria
        info_list.append(analyze_text.analysis(award_string))

        # Find EU funds and add it
        try:
            eu_funds = self.get_sibling(
                info, 'Information about European Union funds')
            funds = eu_funds.text.split(":")[1]
        except Exception:
            funds = None
        info_list.append(funds)

        # Find and write website
        try:
            communication = soup.find(
                'span', string="Communication").next_sibling
            doc_link = communication.find('a', class_="ojshref").text
        except Exception:
            doc_link = None
        info_list.append(doc_link)

        # Find if TCO is mentioned
        full_doc = soup.find(id="mainContent")
        TCO_item = self.find_text(full_doc, r'((Tco|TCO|tco).\w+|(\w+).(Tco|TCO|tco))')
        info_list.append(TCO_item)

        # Find if EPEAT is mentioned
        EPEAT_item = self.find_text(full_doc, r'((Epeat|EPEAT|epeat).\w+|(\w+).(Epeat|EPEAT|epeat))')
        info_list.append(EPEAT_item)

        return info_list