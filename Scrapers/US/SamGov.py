from selenium.common.exceptions import NoSuchElementException

from ScrapingTools import read_write
from DataUploader import Sheet
from FileHandleler import HandleFiles
import time
import re
import winsound
from selenium import webdriver

this_week = "https://beta.sam.gov/search?index=opp&sort=-relevance&page=1&keywords=%22all-in-one%22%20laptop%20laptops%20computer%20workstation%20hp%20philips%20dell%20lenovo%20desktop%20display&inactive_filter_values=false&naics=334&notice_type=k&opp_inactive_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_publish_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%222020-06-11%22,%22endDate%22:%222020-06-18%22%7D%7D&opp_modified_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_response_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&date_filter_index=0"
#this_week="https://beta.sam.gov/search?index=opp&sort=-relevance&page=1&keywords=%22all-in-one%22%20laptop%20laptops%20computer%20workstation%20hp%20philips%20dell%20lenovo%20desktop%20display&inactive_filter_values=false&naics=334&opp_inactive_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_publish_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%222020-06-04%22,%22endDate%22:%222020-06-11%22%7D%7D&opp_modified_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_response_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&date_filter_index=0&notice_type=k"
#this_week="https://beta.sam.gov/search?index=opp&sort=-relevance&page=1&keywords=%22all-in-one%22%20laptop%20laptops%20computer%20workstation%20hp%20philips%20dell%20lenovo%20desktop%20Display&inactive_filter_values=false&opp_inactive_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_publish_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%222020-05-30%22,%22endDate%22:%222020-06-03%22%7D%7D&opp_modified_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_response_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&date_filter_index=0&naics=334"
#this_week = "https://beta.sam.gov/search?index=opp&page=1&keywords=laptops%20laptop%20computer%20datacenter%20tablet%20tablets%20dell%20lenovo%20samsung%20hp%20epeat%20projector&inactive_filter_values=false&sort=-relevance&notice_type=k&naics=334,541519&psc=&opp_inactive_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_publish_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%222020-05-19%22,%22endDate%22:%22%22%7D%7D&opp_modified_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_response_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&date_filter_index=0"

lap_link ="https://beta.sam.gov/search?index=opp&page=1&keywords=laptop%20laptops%20notebook%20notchebooks&inactive" \
          "_filter_values=false&naics=&sort=-relevance&opp_response_date_filter_model=%7B%22dateRange%22:%7B%22" \
          "startDate%22:%222020-01-01%22,%22endDate%22:%22%22%7D%7D&date_filter_index=0"

naics_link = "https://beta.sam.gov/search?index=opp&page=1&keywords=&opp_response_date_filter_model=%7B%22dateRange" \
       "%22:%7B%22startDate%22:%222020-01-01%22,%22endDate%22:%22%22%7D%7D&date_filter_index=0&" \
       "inactive_filter_values=false&naics=334118,334111,334112"

pages = 8

folder_id = "1bupED_ONXjdQ7yhb_Q9denAHVVk3KCQh"

info_list = read_write.read_pickle("samgov.pickle")

def pagination(driver):
    nav = driver.find_element_by_class_name("page-next")
    nav.click()
    time.sleep(10)


def samlinks(driver, link, is_rerun, num_pages, start_opp, stop_opp):
    """if is_rerun:
        info_list = []
        info_list += read_write.read_pickle("samgov.pickle")
        #info_list = read_write.read_csv("samfile.csv")
    else:
        info_list = []
    """

    global info_list
    print(len(info_list))

    driver.get(link)

    # Perform search
    time.sleep(30)  # Let the user actually see something!

    first_page = True
    start_page = 3
    at_page = 1

    while start_page > at_page:
        pagination(driver)
        at_page += 1

    while at_page <= num_pages:
        time.sleep(3)
        result = driver.find_element_by_id("search-results")
        opp_len = len(result.find_elements_by_class_name("opportunity-title"))

        if first_page and num_pages == at_page:
            run_range = range(start_opp - 1, stop_opp)
        elif first_page:
            run_range = range(start_opp - 1, opp_len)
        elif num_pages == at_page:
            run_range = range(stop_opp)
        else:
            run_range = range(opp_len)

        i = 1
        for opp in run_range:
            result = driver.find_element_by_id("search-results")
            opportunity = result.find_elements_by_class_name("opportunity-title")
            opportunity[opp].find_element_by_tag_name("a").click()
            time.sleep(10)
            info = extract_sam_info(driver)
            for ii in info:
                print(type(ii))
            info_list.append(info)
            print("At opp {} of {} on page {}".format(i, len(opportunity), at_page))
            i += 1
            #read_write.save_csv(info_list, "../../ScrapingTools/samfile.csv")
            read_write.save_pickle(info_list, "samgov.pickle")
            driver.execute_script("window.history.go(-1)")
            time.sleep(10)
        read_write.save_csv(info_list, "samfile.csv")
        pagination(driver)
        first_page = False
        at_page += 1
    return info_list


def try_by_id(driver, id):
    try:
        result = driver.find_element_by_id(id)
    except NoSuchElementException:
        result = None
    return result


def try_extraction(query):
    try:
        extraction = query.text
    except Exception as e:
        extraction = None
    return extraction

def split_text(ext):
    if ext is not None:
        result = ext.split(":")[1]
    return result


def extract_sam_info(driver):

    title = try_extraction(driver.find_element_by_xpath('//h1[@class="\'sam-ui-header"]'))
    reference_id = try_extraction(try_by_id(driver, "header-solicitation-number")
                                  .find_element_by_class_name("description"))
    try:
        description = try_extraction(try_by_id(driver, "description").find_element_by_class_name("ng-star-inserted"))
    except Exception:
        description = None
    published = split_text(try_extraction(try_by_id(driver, "general-original-published-date")))
    gen_type = split_text(try_extraction(try_by_id(driver, "general-type")))
    naics = split_text(try_extraction(try_by_id(driver, "classification-naics-code")))
    pcs = split_text(try_extraction(try_by_id(driver, "classification-classification-code")))
    name = try_by_id(driver, "contact-primary-poc-full-name")
    if name is not None:
        name = name.text
    else:
        name = None
    phone = try_extraction(try_by_id(driver, "contact-primary-poc-phone"))
    contractor = try_by_id(driver, "-contracting-office")
    if contractor is not None:
        contractor = contractor.find_element_by_class_name("ng-star-inserted").text
    else:
        contractor = None

    if description is not None:
        find_tco = find_text(description.strip(), r'((Tco|TCO|tco).\w+|(\w+).(Tco|TCO|tco))')
        find_epeat = find_text(description.strip(), r'((Epeat|EPEAT|epeat).\w+|(\w+).(Epeat|EPEAT|epeat))')
    else:
        find_tco = None
        find_epeat = None



    info = [driver.current_url,
                 published,
                 gen_type,
                 title,
                 reference_id,
                 try_extraction(driver.find_element_by_xpath(
                     "//*[text()=' Department/Ind. Agency ']/following-sibling::div")),
                 naics,
                 pcs,
                 description,
                 contractor,
                 name,
                 phone,
                 try_extraction(try_by_id(driver, "contact-primary-poc-email")),
                 find_tco,
                 find_epeat
                 ]

    print(info)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    try:
        driver.find_element_by_xpath("//*[@class='fa fa-cloud-download']").click()
    except Exception as e:
        print(e)
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
        pass

    time.sleep(60)
    if reference_id is not None:
        folder_name = reference_id
    else:
        folder_name = title
    file_operator = HandleFiles(folder_name, folder_id)
    file_operator.extract_files(["zip"])
    time.sleep(10)
    file_operator.read_pdfs()
    words = file_operator.read_docx()
    time.sleep(20)
    drive_link = file_operator.upload_files()
    time.sleep(20)
    file_operator.delete_all_files()

    info.append(words)
    info.append(drive_link)
    print(info)

    return info


def find_text(soup, regex):
    matchobj = re.search(regex, soup)
    if matchobj:
        item = matchobj.group()
    else:
        item = None
    return item


def run_sam(driver, link, date, num_pages):

    header = ["Link", "Published", "Type", "Title", "Notice ID", "Agency", "NAICS", "PSC", "Description",
              "Postal Address", "Contact Person", "Phone number", "Email address", "TCO mentioned",
              "EPEAT mentioned", "Interesting words", "Link to documents"]

    request_list = read_write.read_pickle("samgov.pickle")#samlinks(driver, link, True, num_pages, 1, 10) ##

    i = 0
    for data in request_list:
        j = 0
        for d in data:
            if d is not None:
                if len(d) > 40000:
                    print(d)
                    request_list[i][j] = d[:40000]
            j += 1
        i += 1


    sam_sheet = Sheet("155JpRxPZv25UHq7gG-o3kOzDsy7VbS0u", "Sam.gov", date)
    sam_sheet.init_sheet(header)
    print("time to upload...")
    sam_sheet.append_row(request_list)



#driver = webdriver.Chrome(executable_path='C:/Users/Movie Computer/Desktop/drivers/chromedriver.exe')
run_sam(webdriver.Chrome("C:/Users/Movie Computer/Desktop/drivers/chromedriver.exe"), this_week, "2020-06-25", pages)

