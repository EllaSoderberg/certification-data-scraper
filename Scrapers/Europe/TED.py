from ScrapingTools import read_write, translater, analyze_text
from DataUploader import Sheet
import time
import re
import requests
from bs4 import BeautifulSoup

rlv_cpv_codes = ["30231000", "30214000", "30213000", "30213100",
                 "30213200", "30213300", "30213500", "38652000", "32551300"]

interesting_words = ["energy", "efficiency", "environment", "environmental", "tco", "sustainability", "life", "cycle",
                     "ergonomic", "ecological", "circular", "economy", "circulaire", "economie", "certification",
                     "certificates"]


def tedlinks(driver, link, search, num_pages):
    """
    Get the link to each tender
    :param num_pages:
    :param link: The link to the tender database
    :param search: The string to put into the expert search box
    :return: A list of all the links
    """
    link_list = []
    driver.get(link)

    # Perform search
    time.sleep(5)  # Let the user actually see something!
    search_box = driver.find_element_by_xpath(
        '//*[@title="Go to the expert search form"]')
    search_box.click()
    text_box = driver.find_element_by_id('expertSearchCriteria.query')
    time.sleep(5)  # Let the user actually see something!
    text_box.send_keys(search)

    time.sleep(5)  # Let the user actually see something!
    search_button = driver.find_element_by_xpath(
        '//*[@title="Perform search"]')
    search_button.click()
    time.sleep(2)

    address = driver.current_url

    at_page = 1
    while at_page <= num_pages:
        time.sleep(3)
        new_address = address + '?page=' + str(at_page)
        driver.get(new_address)
        links = driver.find_elements_by_xpath("//*[@title='View this notice']")
        for lin in links:
            link_list.append(lin.get_attribute("href"))
        at_page += 1

    return link_list


def extract_ted_info(link_list, contact_list):
    total = len(link_list)
    request_list = []
    progress = 1
    for link in link_list:
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

        responsible = None
        country = None
        name = None

        # Add email
        email = soup.find("a", class_='ojsmailto').string
        e_mail = email
        info_list.append(email)
        email = None

        # See if the contact is a duplicate
        is_duplicate = False

        for contact in contact_list:
            if e_mail[3:-3] in contact:
                is_duplicate = True

        if is_duplicate:
            info_list.append("YES")
        else:
            info_list.append("NO")

        # Add website
        website = soup.find('a', class_="ojshref").text
        info_list.append(website)
        website = None

        # Find section two
        info = soup.find("span", id='id1-II.').parent.parent

        transl = translater.Trans()
        # Get the title of the project
        try:
            title = get_sibling(info, "Title:").text.strip()
            # Translate title to english and add to file
            eng_title = transl.translate(title).replace(";", ",")
        except Exception:
            eng_title = None

        info_list.append(eng_title)

        # Find cpv code and add code and description
        cpv_codes = []
        try:
            cpv = get_sibling(info, 'Main CPV code')
            cpv_nr = cpv.span.text
            cpv_codes.append(cpv_nr)
            cpv_text = cpv.span['title'].replace(";", ",")
        except Exception:
            cpv_nr = None
            cpv_text = None

        info_list.append(cpv_nr)
        info_list.append(cpv_text)

        # Find secondary CPV codes
        try:
            cpv_nrs = info.find(
                "span", string='Additional CPV code(s)').find_next_siblings("div")
            cpv_string = ""
            cpv_text_string = ""
            for cpv in cpv_nrs:
                cpv_codes.append(cpv.text)
                text = cpv.text + ", "
                cpv_string += text
                text = cpv.span['title'] + ", "
                cpv_text_string += text
        except Exception:
            cpv_string = None
            cpv_text_string = None

        info_list.append(cpv_string)
        info_list.append(cpv_text_string)

        # Find total value and add it
        try:
            total_value = get_sibling(info, 'Estimated total value')
            value = total_value.text
        except Exception:
            value = None

        info_list.append(value)

        # Find, translate, write and save award criteria
        award_string = ""
        try:
            award_criteria = info.find(
                "span", string='Award criteria').find_next_siblings("div")
            for award in award_criteria:
                eng = transl.translate(award.text)
                award_string += str(eng)
                award_string += " "
        except Exception:
            award_string = None
        info_list.append(award_string)

        # Analyze the Award criteria
        info_list.append(analyze_text.analysis(award_string))

        # Find EU funds and add it
        try:
            eu_funds = get_sibling(
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
        TCO_item = find_text(full_doc, r'((Tco|TCO|tco).\w+|(\w+).(Tco|TCO|tco))')
        info_list.append(TCO_item)

        # Find if EPEAT is mentioned
        EPEAT_item = find_text(full_doc, r'((Epeat|EPEAT|epeat).\w+|(\w+).(Epeat|EPEAT|epeat))')
        info_list.append(EPEAT_item)

        request_list.append(info_list)
        print(progress, "of", total, "done")
        progress += 1
    return request_list


def find_text(soup, regex):
    matchobj = re.search(regex, str(soup(text=(re.compile(regex)))))
    if matchobj:
        item = matchobj.group()
    else:
        item = None
    return item


def get_sibling(parent, name):
    sibling = parent.find('span', string=name).next_sibling
    return sibling


def run_ted(driver, link, searchdate, date, num_pages):
    search = "PD=[{}] AND PC=[30231000 or 38652000 or 32551300 or 30214000 or 30213000 or 30213100 or " \
             "30213200 or 30213300 or 30213500] AND TD=[3]".format(searchdate)
    header = ["Link", "Date published", "Authority name", "Country", "Contact person", "E-mail", "Is duplicate",
              "Website", "Title", "CPV nr", "CPV text", "Secondary CPV", "S CPV text", "Total value", "Award criteria",
              "Found words", "EU funding", "Documents", "TCOC mentioned", "EPEAT mentioned"]

    contact_list = read_write.read_pickle("ScrapingTools/TED_contacts.p")
    links = tedlinks(driver, link, search, num_pages)
    request_list = extract_ted_info(links, contact_list)
    ted_sheet = Sheet("1LoN1ufjKEGyMhEtC-cGdUqDDE465DDml", "TED", date)
    ted_sheet.init_sheet(header)
    print("time to upload...")
    ted_sheet.append_row(request_list)
