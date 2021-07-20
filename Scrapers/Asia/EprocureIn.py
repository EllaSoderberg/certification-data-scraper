from ScrapingTools import read_write, failproof
from FileHandleler import HandleFiles
from DataUploader import Sheet
import time
from bs4 import BeautifulSoup
import winsound

import logging

doc_folder_ID = "1ZiyNH8ADT4rQsOv0qaX9IY_-LgtwucIU"


def eprocure_links(driver, link, end_opp, end_page):
    """
    Visits the eprocure site and extracts the data and downloads the files
    :param start_opp:
    :param stop_opp:
    :param num_pages:
    :param is_rerun:
    :param driver:
    :param link: a link to the search result
    """

    eprocure_runner = failproof.Runner(project="eprocure", end_opp=end_opp, end_page=end_page)

    while eprocure_runner.retries < 5:
        try:

            logging.info("Starting at:")

            driver.get(new_link)
            time.sleep(5)

            table = driver.find_element_by_tag_name("tbody")
            t_rows = table.find_elements_by_tag_name("tr")
            eprocure_runner.table_len = len(t_rows)

            while eprocure_runner.end_page >= eprocure_runner.at_page:
                run_range = eprocure_runner.calc_range()
                for tender_no in run_range:
                    eprocure_runner.at_opp = tender_no
                    table = driver.find_element_by_tag_name("tbody")
                    t_rows = table.find_elements_by_tag_name("tr")
                    columns = t_rows[tender_no].find_elements_by_tag_name("td")
                    columns[4].find_element_by_tag_name("a").click()
                    frequency = 2500  # Set Frequency To 2500 Hertz
                    duration = 1000  # Set Duration To 1000 ms == 1 second
                    winsound.Beep(frequency, duration)
                    time.sleep(20)
                    data = eprocure_search(driver)
                    eprocure_runner.data_list.append(data)
                    driver.get(new_link)
                    logging.info("Number of datapoints:", len(eprocure_runner.data_list))
                    logging.info("Currently at", tender_no+1, "of", eprocure_runner.table_len)
                    read_write.save_pickle(eprocure_runner.data_list, "eprocure.pickle")

            eprocure_runner.first_page = False
            eprocure_runner.at_page += 1
            new_link = link + "?page={}".format(eprocure_runner.at_page)
            driver.get(new_link)

        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            print("Stopped at page {} and on opportunity {}".format(eprocure_runner.at_page, eprocure_runner.at_opp+1))
            eprocure_runner.retries += 1
            logging.warning("Retry no. {}".format(eprocure_runner.retries))

    if eprocure_runner.retries == 5:
        logging.warning("Maximum retries exceeded, quitting program and saving logs.")
        read_write.save_pickle(eprocure_runner, "runner.p")
        quit(1)

    read_write.save_pickle(eprocure_runner.data_list, "eprocure.pickle")
    driver.close()
    return eprocure_runner.data_list


def eprocure_search(driver):
    """
    Search for information on the page with the data
    :param driver:
    :param web_element: the web element containing all the data
    """
    info_list = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    info_list.append(soup.find('td', string="ePublished Date").find_next_siblings(width="20%")[0].text.strip())
    info_list.append(soup.find('td', string="Organisation Name").find_next_siblings(id="tenderDetailDivTd")[0]
                     .text.strip())
    info_list.append(soup.find('td', string="Tender Title").find_next_siblings(id="tenderDetailDivTd")[0].text.strip())

    reference_number = soup.find('td', string="Tender Reference Number").find_next_siblings(width="20%")[0].text.strip()
    info_list.append(reference_number)
    info_list.append(soup.find('td', string="Product Category").find_next_siblings(width="20%")[0].text.strip())
    info_list.append(soup.find('td', string="Product Sub-Category").find_next_siblings(width="20%")[0].text.strip())
    info_list.append(soup.find('td', string="Work Description").find_next_siblings(id="tenderDetailDivTd")[0]
                     .text.strip())

    link_text = soup.find('td', string="Tender Document").find_next_siblings(id="tenderDetailDivTd")[0].text.strip()
    if "FrontEndTenderDetailsExternal" in link_text:
        download_file(driver, link_text)
        file_operator = HandleFiles(reference_number, doc_folder_ID)
        file_operator.extract_files(["zip"])
        info_list.append(file_operator.read_pdfs())
        info_list.append(file_operator.upload_files())
        file_operator.delete_all_files()
    else:
        logging.info("This tender does not have any files")
        info_list.append(None)
        info_list.append(None)

    driver.execute_script("window.history.go(-3)")
    time.sleep(20)
    return info_list


def download_file(driver, link):
    """
    Downloads files on website
    :param driver:
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
        logging.error("Exception occurred", exc_info=True)
        pass


def run_eprocurein(driver, date, link, end_opp, end_page):
    header = ["Date published", "Organisation Name", "Tender Title", "Reference Number", "Product Category",
              "Product Sub-Category", "Description", "Keywords", "Found", "Link to folder"]

    request_list = eprocure_links(driver, link, end_opp, end_page)
    epocure_sheet = Sheet("1Q9dT-AaNlExuFZMtkn2WPRFWzdye0KWy", "Eprocure India TEST", date)
    epocure_sheet.init_sheet(header)
    logging.info("time to upload...")
    epocure_sheet.append_row(request_list)
