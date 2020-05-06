import time
from DataUploader import Sheet
from FileHandleler import HandleFiles
from ScrapingTools import read_write


# ausschreibungen_folder_ID = "18agl3lrZSmynIWAvdAiIMPcgGayPyLcL"


def try_extraction(driver, xpath):
    try:
        extraction = driver.find_element_by_xpath(xpath).text
    except Exception as e:
        print(e)
        extraction = None
    return extraction


def evergabe(driver, link, is_rerun, stop_opp, start_opp=1):
    if is_rerun:
        all_info = read_write.read_pickle("evergabe.pickle")
    else:
        all_info = []

    driver.get(link)

    time.sleep(3)
    table = driver.find_element_by_id("listTemplate")

    documents = table.find_elements_by_class_name("noTextDecorationLink")

    at_opp = start_opp

    doc_range = documents[start_opp:stop_opp+1]

    for document in doc_range:
        try:
            document.click()
            handles = driver.window_handles
            done, info_list = extract_info(driver, handles)
            all_info.append(info_list)
            while not done:
                time.sleep(15)
            driver.switch_to.window(handles[0])
            print(at_opp, "of", len(doc_range), "done")
            at_opp += 1
        except Exception as e:
            print(e)
            print("Stopped at opportunity {}".format(at_opp))
            read_write.save_pickle(all_info, "evergabe.pickle")

    driver.close()
    return all_info


def extract_info(driver, handles):
    info_list = []
    driver.switch_to.window(handles[-1])
    title = try_extraction(driver, '//*[@id="projectRoomTitleText"]')
    tenderid = try_extraction(driver, "//span[text()='Ausschreibungs-ID']/../../following-sibling::div")
    time.sleep(5)
    try:
        driver.find_element_by_xpath("//*[@href='./processdata']").click()
        time.sleep(3)
    except Exception:
        pass
    finally:
        organization = try_extraction(driver, "//*[text()='Offizielle Bezeichnung']/following-sibling::div")
        contact = try_extraction(driver, "//*[text()='Kontaktstelle']/following-sibling::div")
        contact_person = try_extraction(driver, "//*[text()='zu Händen von']/following-sibling::div")
        phone = try_extraction(driver, "//*[text()='Telefon']/following-sibling::div")
        email = try_extraction(driver, "//*[text()='E-Mail']/following-sibling::div")
        web_address = try_extraction(driver, "//*[text()='Internet-Adresse (URL)']/following-sibling::div")
    try:
        driver.find_element_by_xpath("//*[@href='./documents']").click()
        time.sleep(3)
    except Exception:
        pass
    else:
        driver.find_element_by_xpath("//*[@title='Alle Dokumente als ZIP-Datei herunterladen']").click()

    info_list.append(tenderid)
    info_list.append(title)
    info_list.append(organization)
    info_list.append(contact)
    info_list.append(contact_person)
    info_list.append(phone)
    info_list.append(email)
    info_list.append(web_address)

    time.sleep(20)

    evergabe_folder_id = "1zVLDxvny4kr5ZopfnPI2ATATq9yu3AOc"

    file_operator = HandleFiles(tenderid, evergabe_folder_id)
    file_operator.extract_files(["zip"])
    info_list.append(file_operator.read_pdfs())
    info_list.append(file_operator.upload_files())
    file_operator.delete_all_files()

    return True, info_list


def run_evergabe(driver, date, link, is_rerun, stop_opp, start_opp):
    header = ["ID", "Title", "Offizielle Bezeichnung", "Kontaktstelle", "zu Händen von", "Telefon",
              "E-Mail", "Internet-Adresse (URL)", "Keywords Found", "Link to folder"]

    request_list = evergabe(driver, link, is_rerun, stop_opp, start_opp)
    evergabe_sheet = Sheet("1wfNNoTwJyXzCEIinJnRe8lLduMw1VAzd", "Evergabe", date)
    evergabe_sheet.init_sheet(header)
    print("time to upload...")
    evergabe_sheet.append_row(request_list)
