import time
from selenium import webdriver
from DataUploader import Sheet
from FileHandleler import HandleFiles

driver = webdriver.Chrome('C:/Users/Ella/Desktop/Drivers/chromedriver')
# ausschreibungen_folder_ID = "18agl3lrZSmynIWAvdAiIMPcgGayPyLcL"


def try_extraction(driver, xpath):
    try:
        extraction = driver.find_element_by_xpath(xpath).text
    except Exception as e:
        print(e)
        extraction = None
    return extraction


def evergabe(link):
    all_info = []
    driver.get(link)

    time.sleep(3)
    table = driver.find_element_by_id("listTemplate")

    documents = table.find_elements_by_class_name("noTextDecorationLink")

    doc_range = documents[:2]

    progress = 1
    for document in doc_range:
        document.click()
        handles = driver.window_handles
        done, info_list = extract_info(driver, handles)
        all_info.append(info_list)
        while not done:
            time.sleep(15)
        driver.switch_to.window(handles[0])
        print(progress, "of", len(doc_range), "done")
        progress += 1

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


def run_evergabe(date):
    link = "https://www.evergabe.nrw.de/VMPCenter/common/project/search.do?method=showExtendedSearch&fromExternal=true#eyJjcHZDb2RlcyI6W3sibmFtZSI6IkFyYmVpdHNwbMOkdHplIiwiY29kZSI6IjMwMjE0MDAwLTIifSx7Im5hbWUiOiJCaWxkc2NoaXJtZSIsImNvZGUiOiIzMDIzMTMwMC0wIn0seyJuYW1lIjoiQ29tcHV0ZXJiaWxkc2NoaXJtZSB1bmQgS29uc29sZW4iLCJjb2RlIjoiMzAyMzEwMDAtNyJ9LHsibmFtZSI6IkZlcm5zcHJlY2hrb3BmaMO2cmVyZ2Fybml0dXJlbiIsImNvZGUiOiIzMjU1MTMwMC0zIn0seyJuYW1lIjoiRmlsbXZvcmbDvGhyZ2Vyw6R0ZSIsImNvZGUiOiIzODY1MjAwMC0wIn0seyJuYW1lIjoiUGVyc29uYWxjb21wdXRlciIsImNvZGUiOiIzMDIxMzAwMC01In0seyJuYW1lIjoiVGFibGV0dGNvbXB1dGVyIiwiY29kZSI6IjMwMjEzMjAwLTcifSx7Im5hbWUiOiJUYXNjaGVuY29tcHV0ZXIiLCJjb2RlIjoiMzAyMTM1MDAtMCJ9LHsibmFtZSI6IlRpc2NoY29tcHV0ZXIiLCJjb2RlIjoiMzAyMTMzMDAtOCJ9LHsibmFtZSI6IlRyYWdiYXJlIENvbXB1dGVyIiwiY29kZSI6IjMwMjEzMTAwLTYifV0sImNvbnRyYWN0aW5nUnVsZXMiOlsiVk9MIiwiVk9CIiwiVlNWR1YiLCJTRUtUVk8iLCJPVEhFUiJdLCJwdWJsaWNhdGlvblR5cGVzIjpbIlRlbmRlciJdLCJkaXN0YW5jZSI6MCwicG9zdGFsQ29kZSI6IiIsIm9yZGVyIjoiMCIsInBhZ2UiOiIxIiwic2VhcmNoVGV4dCI6IiIsInNvcnRGaWVsZCI6IlBST0pFQ1RfUFVCTElDQVRJT05fREFURV9MTkcifQ"
    header = ["ID",	"Title", "Offizielle Bezeichnung", "Kontaktstelle", "zu Händen von", "Telefon",
                              "E-Mail", "Internet-Adresse (URL)", "Keywords Found", "Link to folder"]
    evergabe_sheet = Sheet("1wfNNoTwJyXzCEIinJnRe8lLduMw1VAzd", "Evergabe", date)
    evergabe_sheet.init_sheet(header)
    request_list = evergabe(link)
    print("time to upload...")
    evergabe_sheet.append_row(request_list)

