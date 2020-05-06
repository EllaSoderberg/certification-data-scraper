from ScrapingTools import read_write
from FileHandleler import HandleFiles
from DataUploader import Sheet
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import winsound

driver = webdriver.Chrome('C:/Users/Ella/Desktop/Drivers/chromedriver')
doc_folder_ID = "1ZiyNH8ADT4rQsOv0qaX9IY_-LgtwucIU"


def eprocure_links(link):
    """
    Visits the eprocure site and extracts the data and downloads the files
    :param link: a link to the search result
    """
    data_list = []
    driver.get(link)

    time.sleep(5)

    pages = driver.find_element_by_class_name("pagination").text
    number_pages = 3 #max(re.findall(r'\d+', pages))

    new_link = link

    curr_page = 1
    while int(number_pages) >= curr_page:
        # table = driver.find_element_by_tag_name("tbody")
        # t_rows = table.find_elements_by_tag_name("tr")
        for i in range(10):
            table = driver.find_element_by_tag_name("tbody")
            t_rows = table.find_elements_by_tag_name("tr")
            columns = t_rows[i].find_elements_by_tag_name("td")
            columns[4].find_element_by_tag_name("a").click()
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)
            time.sleep(20)
            data = eprocure_search(driver)
            data_list.append(data)
            driver.get(new_link)
            # link_list.append(columns[4].find_element_by_tag_name("a").get_attribute("href"))
        curr_page += 1
        new_link = link + "?page={}".format(curr_page)
        driver.get(new_link)

        table = driver.find_element_by_tag_name("tbody")
        t_rows = table.find_elements_by_tag_name("tr")
        columns = t_rows[0].find_elements_by_tag_name("td")
        columns[4].find_element_by_tag_name("a").click()
        time.sleep(20)
        data = eprocure_search(driver)
        data_list.append(data)

    driver.close()
    return data_list


def eprocure_search(web_element):
    """
    Search for information on the page with the data
    :param web_element: the web element containing all the data
    """
    info_list = []
    soup = BeautifulSoup(web_element.page_source, 'html.parser')

    info_list.append(soup.find('td', string="ePublished Date").find_next_siblings(width="20%")[0].text.strip())
    info_list.append(soup.find('td', string="Organisation Name").find_next_siblings(id="tenderDetailDivTd")[0]
                     .text.strip())
    info_list.append(soup.find('td', string="Tender Title").find_next_siblings(id="tenderDetailDivTd")[0].text.strip())

    reference_number = soup.find('td', string="Tender Reference Number").find_next_siblings(width="20%")[0].text.strip()
    info_list.append(reference_number)
    info_list.append(soup.find('td', string="Product Category").find_next_siblings(width="20%")[0].text.strip())
    info_list.append(soup.find('td', string="Product Sub-Category").find_next_siblings(width="20%")[0].text.strip())
    info_list.append(soup.find('td', string="Work Description").find_next_siblings(id="tenderDetailDivTd")[0].text.strip())

    link_text = soup.find('td', string="Tender Document").find_next_siblings(id="tenderDetailDivTd")[0].text.strip()
    if "FrontEndTenderDetailsExternal" in link_text:
        download_file(link_text)
        file_operator = HandleFiles(reference_number, doc_folder_ID)
        file_operator.extract_files(["zip"])
        info_list.append(file_operator.read_pdfs())
        info_list.append(file_operator.upload_files())
        file_operator.delete_all_files()
    else:
        info_list.append(None)
        info_list.append(None)

    read_write.save_pickle(info_list, "india_info_2.p")

    driver.execute_script("window.history.go(-3)")
    time.sleep(20)
    return info_list


def download_file(link):
    """
    Downloads files on website
    :param link: The link to the page with the folders
    """
    driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(link)).click()
    try:
        driver.find_element_by_xpath("//*[contains(text(), 'Download as zip file')]").click()
        try:
            driver.find_element_by_xpath("//button[@id='captcha']")
        except Exception:
            pass
        else:
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)
            time.sleep(20)
            driver.find_element_by_xpath("//*[contains(text(), 'Download as zip file')]").click()

        driver.find_element_by_xpath("//*[contains(text(), 'Tendernotice_1')]").click()
        time.sleep(20)
    except Exception:
        pass


def get_final_links():
    link = 'https://eprocure.gov.in/cppp/searchbyproduct/byUjI5dlpITT1BMTNoMVEyOXRjSFYwWlhJZ1NHRnlaSGRoY21VPUExM2gxY0hWaWJHbHphR1ZrWDJSaGRHVT1BMTNoMWMyRnNkQT09?page=2'
    driver.get(link)
    time.sleep(5)

    table = driver.find_element_by_tag_name("tbody")
    t_rows = table.find_elements_by_tag_name("tr")
    for i in range(3, len(t_rows)):
        table = driver.find_element_by_tag_name("tbody")
        t_rows = table.find_elements_by_tag_name("tr")
        columns = t_rows[i].find_elements_by_tag_name("td")
        columns[4].find_element_by_tag_name("a").click()
        eprocure_search(driver)
        driver.get(link)


def read_files_again(info_list):
    curr_path = "C:\\Users\\Ella\\Desktop\\Spara\\Jobb\\Tenders\\Demo0320\\"
    file_list = []  # get_files(curr_path, "*.pdf")

    for info in info_list:
        matched_words = []
        clean_words = []
        if info["Link to folder"] is not None:
            folder_id = info["Link to folder"].split("/")[-1]
            for file_name in file_list:
                if folder_id in file_name:
                    print("uo")
                    #  pdf_text = read_pdf(curr_path + file_name)
                    #  matched_words.append(find_search_words(pdf_text))
            for match in matched_words:
                if match is not None:
                    for word in match:
                        clean_words.append(word)
            print(set(clean_words))
        info['Keywords Found'] = set(clean_words)
    return info_list


def run_eprocurein(date):
    link = "https://eprocure.gov.in/cppp/searchbyproduct/byUjI5dlpITT1BMTNoMVEyOXRjSFYwWlhJZ1NHRnlaSGRoY21VPUExM2gxY0hWaWJHbHphR1ZrWDJSaGRHVT1BMTNoMWMyRnNkQT09"
    header = ["Date published", "Organisation Name", "Tender Title", "Reference Number", "Product Category",
              "Product Sub-Category", "Description", "Keywords", "Found", "Link to folder"]
    epocure_sheet = Sheet("1Q9dT-AaNlExuFZMtkn2WPRFWzdye0KWy", "Eprocure India", date)
    epocure_sheet.init_sheet(header)

    request_list = eprocure_links(link)
    print("time to upload...")
    epocure_sheet.append_row(request_list)

