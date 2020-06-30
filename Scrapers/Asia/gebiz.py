from FileHandleler import HandleFiles
from DataUploader import Sheet
from ScrapingTools import read_write
import time
import winsound
import logging

doc_folder_id = "1ckD74zWxLjDJSpNuJYu1MAQT1KtwlPrG"


def pagination(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    nav = driver.find_element_by_class_name("formRepeatPagination2_NAVIGATION-BUTTONS-DIV")
    nav.find_element_by_xpath("//*[@value='Next']").click()
    time.sleep(20)


def enter_gebiz(driver, link, username, password, is_rerun, num_pages, start_page, stop_opp, start_opp=1):
    if is_rerun:
        data_list = read_write.read_pickle("gebiz_temp.pickle")
    else:
        data_list = []

    driver.get(link)
    logging.info("Starting at:", link)

    # Login part
    time.sleep(5)
    user_box = driver.find_element_by_xpath("//*[@name='contentForm:j_idt140_inputText']")
    user_box.send_keys(username)
    password_box = driver.find_element_by_id('contentForm:password_inputText')
    password_box.send_keys(password)
    time.sleep(5)
    driver.find_element_by_id("contentForm:buttonSubmit").click()
    time.sleep(10)

    # Go to opportunities page
    driver.find_element_by_id("contentForm:j_id56").click()
    time.sleep(5)

    first_page = True
    at_page = 1
    at_opp = start_opp

    while start_page > at_page:
        pagination(driver)
        at_page += 1

    while num_pages >= at_page:
        tenders = len(driver.find_elements_by_class_name("commandLink_TITLE-BLUE"))
        if first_page and num_pages == at_page:
            run_range = range(start_opp-1, stop_opp)
        elif first_page:
            run_range = range(start_opp-1, tenders)
        elif num_pages == at_page:
            run_range = range(stop_opp)
        else:
            run_range = range(tenders)

        for tender_no in run_range:
            try:
                tenders = driver.find_elements_by_class_name("commandLink_TITLE-BLUE")
                reference = driver.find_elements_by_class_name("formSectionHeader6_TEXT")[tender_no].text
                title = tenders[tender_no].text
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                tenders[tender_no].click()
                time.sleep(10)
                data = extract_gebiz_info(driver, title, reference)
                data_list.append(data)
                time.sleep(10)
                at_opp += 1
                logging.info("Number of datapoints:", len(data_list))
                logging.info("Currently at", tender_no+1, "of 10")
                read_write.save_pickle(data_list, "gebiz_temp.pickle")
            except Exception as e:
                logging.error("Exception occurred", exc_info=True)
                print("Stopped at page {} and on opportunity {}".format(at_page, at_opp))
                read_write.save_pickle(data_list, "gebiz_temp.pickle")
                quit(1)

        pagination(driver)
        first_page = False
        at_page += 1
        read_write.save_pickle(data_list, "gebiz_temp.pickle")

    read_write.save_pickle(data_list, "gebiz_temp.pickle")
    driver.close()
    return data_list


def try_extraction(driver, xpath):
    try:
        extraction = driver.find_element_by_xpath(xpath).find_element_by_class_name("formOutputText_VALUE-DIV ").text
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        extraction = None
    return extraction


def extract_gebiz_info(driver, title, reference):
    info_list = [title, reference, try_extraction(driver, "//span[text()='Reference No.']/../../../../.."),
                 try_extraction(driver, "//span[text()='Agency']/../../../../.."),
                 try_extraction(driver, "//span[text()='Published']/../../../../.."),
                 try_extraction(driver, "//span[text()='Procurement Type']/../../../../.."),
                 try_extraction(driver, "//span[text()='Procurement Category']/../../../../..")]

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_class_name("formAttachmentsList_DOWNLOAD-BUTTON").click()
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
        pass

    time.sleep(60)

    file_operator = HandleFiles(reference, doc_folder_id)
    file_operator.extract_files(["zip"])
    time.sleep(10)
    file_operator.read_pdfs()
    words = file_operator.read_docx()
    time.sleep(20)
    drive_link = file_operator.upload_files()
    time.sleep(20)
    file_operator.delete_all_files()
    contact_info = driver.find_element_by_xpath(
        "//*[text()='WHO TO CONTACT']/../../../../../../following-sibling::div").text.split("\n")
    i = 0
    if "PRIMARY" in contact_info[0]:
        i = 1

    info_list.append(contact_info[i])
    info_list.append(contact_info[i+1])
    info_list.append(contact_info[i+2])
    info_list.append(contact_info[-1])

    info_list.append(words)
    info_list.append(drive_link)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_xpath("//input[@value='Back to Search Results']").click()

    return info_list


def run_gebiz(driver, link, date, is_rerun, num_pages, start_page, stop_opp, start_opp):
    username = "301776080"
    password = "TcoDevelopment"
    header = ["Title", "Reference",	"Reference number", "Agency", "Published", "Procurement type", "Category",
              "Contact person", "Email", "Mobile phone number", "Address", "Found words", "Link to files"]

    request_list = enter_gebiz(driver, link, username, password, is_rerun, num_pages, start_page, stop_opp, start_opp)
    gebiz_sheet = Sheet("1_3CkwtS6EMUdD3WRUQ7B3jhgUn3T1v-y", "Gebiz", date)
    gebiz_sheet.init_sheet(header)
    logging.info("Time to upload...")
    gebiz_sheet.append_row(request_list)


def save_gebiz():
    data_list = read_write.read_pickle("gebiz_temp.pickle")
    header = ["Title", "Reference", "Reference number", "Agency", "Published", "Procurement type", "Category",
              "Contact person", "Email", "Mobile phone number", "Address", "Found words", "Link to files"]

    gebiz_sheet = Sheet("1_3CkwtS6EMUdD3WRUQ7B3jhgUn3T1v-y", "Gebiz", "2020-06-26")
    gebiz_sheet.init_sheet(header)
    print("time to upload...")
    gebiz_sheet.append_row(data_list)
