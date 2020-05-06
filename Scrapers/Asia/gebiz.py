from FileHandleler import HandleFiles
from DataUploader import Sheet
from ScrapingTools import read_write
import time
import pickle
import winsound

doc_folder_id = "1ckD74zWxLjDJSpNuJYu1MAQT1KtwlPrG"


def pagination(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    nav = driver.find_element_by_class_name("formRepeatPagination2_NAVIGATION-BUTTONS-DIV")
    nav.find_element_by_xpath("//*[@value='Next']").click()
    time.sleep(20)


def enter_gebiz(driver, link, username, password, is_rerun, num_pages, stop_opp, start_opp=1):
    if is_rerun:
        data_list = read_write.read_pickle("gebiz.pickle")
    else:
        data_list = []

    driver.get(link)

    # Login part
    time.sleep(5)
    user_box = driver.find_element_by_id("contentForm:j_idt139_inputText")
    user_box.send_keys(username)
    password_box = driver.find_element_by_id('contentForm:j_idt140_inputText')
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

    while num_pages >= at_page:
        tenders = len(driver.find_elements_by_class_name("commandLink_TITLE-BLUE"))
        if first_page and num_pages == at_page:
            run_range = range(start_opp-1, stop_opp-1)
        elif first_page:
            run_range = range(start_opp-1, tenders)
        elif num_pages == at_page:
            run_range = range(stop_opp-1)
        else:
            run_range = range(tenders)

        for tender_no in run_range:
            try:
                tenders = driver.find_elements_by_class_name("commandLink_TITLE-BLUE")
                reference = driver.find_elements_by_class_name("formSectionHeader6_TEXT")[tender_no].text
                title = tenders[tender_no].text
                tenders[tender_no].click()
                time.sleep(10)
                data = extract_gebiz_info(driver, title, reference)
                data_list.append(data)
                time.sleep(10)
                at_opp += 1
                print(tender_no, "of", range(tenders), "done")
            except Exception as e:
                print(e)
                print("Stopped at page {} and on opportunity {}".format(at_page, at_opp))
                read_write.save_pickle(data_list, "gebiz.pickle")

        pagination(driver)
        first_page = False
        at_page += 1

    driver.close()
    return data_list


def try_extraction(driver, xpath):
    try:
        extraction = driver.find_element_by_xpath(xpath).find_element_by_class_name("formOutputText_VALUE-DIV ").text
    except Exception as e:
        print(e)
        extraction = None
    return extraction


start_height = 1000


def extract_gebiz_info(driver, title, reference):
    info_list = [title, reference, try_extraction(driver, "//span[text()='Reference No.']/../../../../.."),
                 try_extraction(driver, "//span[text()='Agency']/../../../../.."),
                 try_extraction(driver, "//span[text()='Published']/../../../../.."),
                 try_extraction(driver, "//span[text()='Procurement Type']/../../../../.."),
                 try_extraction(driver, "//span[text()='Procurement Category']/../../../../..")]

    try:
        driver.find_element_by_class_name("formAttachmentsList_DOWNLOAD-BUTTON").click()
    except Exception as e:
        print(e)
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

    driver.find_element_by_class_name("commandButton_BACK-BLUE-TEXT").click()

    pickle_file = open("gebiz_data_extra.p", "wb")
    pickle.dump(info_list, pickle_file)

    return info_list


def run_gebiz(driver, link, date, is_rerun, num_pages, stop_opp, start_opp):
    username = "301776080"
    password = "TcoDevelopment"
    header = ["Title", "Reference",	"Reference number", "Agency", "Published", "Procurement type", "Category",
              "Contact person", "Email", "Mobile phone number", "Address", "Found words", "Link to files"]

    request_list = enter_gebiz(driver, link, username, password, is_rerun, num_pages, stop_opp, start_opp)
    gebiz_sheet = Sheet("1_3CkwtS6EMUdD3WRUQ7B3jhgUn3T1v-y", "Gebiz", date)
    gebiz_sheet.init_sheet(header)
    print("time to upload...")
    gebiz_sheet.append_row(request_list)
