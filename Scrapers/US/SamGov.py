from selenium.common.exceptions import NoSuchElementException

from FileHandleler import HandleFiles
import time
import re
import winsound
import logging

from Scrapers.base_scraper import BaseScraper

class SamGov(BaseScraper):
    def __init__(self, end_opp, end_page, sheet_id=None):
        super(SamGov, self).__init__(
            link="https://beta.sam.gov/search/?index=opp&page=1&sort=-relevance&sfm%5Bstatus%5D%5Bis_active%5D=true&sfm%5Bkeywords%5D%5B0%5D%5Bkey%5D=%22All-in-one%22&sfm%5Bkeywords%5D%5B0%5D%5Bvalue%5D=%22All-in-one%22&sfm%5Bkeywords%5D%5B1%5D%5Bkey%5D=laptop&sfm%5Bkeywords%5D%5B1%5D%5Bvalue%5D=laptop&sfm%5Bkeywords%5D%5B2%5D%5Bkey%5D=laptops&sfm%5Bkeywords%5D%5B2%5D%5Bvalue%5D=laptops&sfm%5Bkeywords%5D%5B3%5D%5Bkey%5D=hp&sfm%5Bkeywords%5D%5B3%5D%5Bvalue%5D=hp&sfm%5Bkeywords%5D%5B4%5D%5Bkey%5D=lenovo&sfm%5Bkeywords%5D%5B4%5D%5Bvalue%5D=lenovo&sfm%5Bkeywords%5D%5B5%5D%5Bkey%5D=acer&sfm%5Bkeywords%5D%5B5%5D%5Bvalue%5D=acer&sfm%5Bkeywords%5D%5B6%5D%5Bkey%5D=asus&sfm%5Bkeywords%5D%5B6%5D%5Bvalue%5D=asus&sfm%5Bkeywords%5D%5B7%5D%5Bkey%5D=epeat&sfm%5Bkeywords%5D%5B7%5D%5Bvalue%5D=epeat&sfm%5Bkeywords%5D%5B8%5D%5Bkey%5D=notebook&sfm%5Bkeywords%5D%5B8%5D%5Bvalue%5D=notebook&sfm%5Bkeywords%5D%5B9%5D%5Bkey%5D=aoc&sfm%5Bkeywords%5D%5B9%5D%5Bvalue%5D=aoc&sfm%5Bkeywords%5D%5B10%5D%5Bkey%5D=dell&sfm%5Bkeywords%5D%5B10%5D%5Bvalue%5D=dell&sfm%5Bkeywords%5D%5B11%5D%5Bkey%5D=casio&sfm%5Bkeywords%5D%5B11%5D%5Bvalue%5D=casio&sfm%5Bkeywords%5D%5B12%5D%5Bkey%5D=epson&sfm%5Bkeywords%5D%5B12%5D%5Bvalue%5D=epson&sfm%5Bkeywords%5D%5B13%5D%5Bkey%5D=headset&sfm%5Bkeywords%5D%5B13%5D%5Bvalue%5D=headset&sfm%5Bkeywords%5D%5B14%5D%5Bkey%5D=projectors&sfm%5Bkeywords%5D%5B14%5D%5Bvalue%5D=projectors&sfm%5Bkeywords%5D%5B15%5D%5Bkey%5D=notebooks&sfm%5Bkeywords%5D%5B15%5D%5Bvalue%5D=notebooks&sfm%5Bdates%5D%5BpublishedDate%5D%5BpublishedDateSelect%5D=pastWeek",
            doc_folder_id="1bupED_ONXjdQ7yhb_Q9denAHVVk3KCQh",
            sheet_folder_id="155JpRxPZv25UHq7gG-o3kOzDsy7VbS0u",
            project="SamGov",
            header=["Link", "Published", "Type", "Title", "Notice ID", "Agency", "NAICS", "PSC", "Description",
              "Postal Address", "Contact Person", "Phone number", "Email address", "TCO mentioned",
              "EPEAT mentioned", "Interesting words", "Link to documents"],
            end_opp=end_opp,
            end_page=end_page,
            sheet_id=sheet_id)
        self.at_opp = 1
        self.at_page = 1
        self.current_link = "https://beta.sam.gov/search/?index=opp&page={}&sort=-relevance&sfm%5Bstatus%5D%5Bis_active%5D=true&sfm%5Bkeywords%5D%5B0%5D%5Bkey%5D=%22All-in-one%22&sfm%5Bkeywords%5D%5B0%5D%5Bvalue%5D=%22All-in-one%22&sfm%5Bkeywords%5D%5B1%5D%5Bkey%5D=laptop&sfm%5Bkeywords%5D%5B1%5D%5Bvalue%5D=laptop&sfm%5Bkeywords%5D%5B2%5D%5Bkey%5D=laptops&sfm%5Bkeywords%5D%5B2%5D%5Bvalue%5D=laptops&sfm%5Bkeywords%5D%5B3%5D%5Bkey%5D=hp&sfm%5Bkeywords%5D%5B3%5D%5Bvalue%5D=hp&sfm%5Bkeywords%5D%5B4%5D%5Bkey%5D=lenovo&sfm%5Bkeywords%5D%5B4%5D%5Bvalue%5D=lenovo&sfm%5Bkeywords%5D%5B5%5D%5Bkey%5D=acer&sfm%5Bkeywords%5D%5B5%5D%5Bvalue%5D=acer&sfm%5Bkeywords%5D%5B6%5D%5Bkey%5D=asus&sfm%5Bkeywords%5D%5B6%5D%5Bvalue%5D=asus&sfm%5Bkeywords%5D%5B7%5D%5Bkey%5D=epeat&sfm%5Bkeywords%5D%5B7%5D%5Bvalue%5D=epeat&sfm%5Bkeywords%5D%5B8%5D%5Bkey%5D=notebook&sfm%5Bkeywords%5D%5B8%5D%5Bvalue%5D=notebook&sfm%5Bkeywords%5D%5B9%5D%5Bkey%5D=aoc&sfm%5Bkeywords%5D%5B9%5D%5Bvalue%5D=aoc&sfm%5Bkeywords%5D%5B10%5D%5Bkey%5D=dell&sfm%5Bkeywords%5D%5B10%5D%5Bvalue%5D=dell&sfm%5Bkeywords%5D%5B11%5D%5Bkey%5D=casio&sfm%5Bkeywords%5D%5B11%5D%5Bvalue%5D=casio&sfm%5Bkeywords%5D%5B12%5D%5Bkey%5D=epson&sfm%5Bkeywords%5D%5B12%5D%5Bvalue%5D=epson&sfm%5Bkeywords%5D%5B13%5D%5Bkey%5D=headset&sfm%5Bkeywords%5D%5B13%5D%5Bvalue%5D=headset&sfm%5Bkeywords%5D%5B14%5D%5Bkey%5D=projectors&sfm%5Bkeywords%5D%5B14%5D%5Bvalue%5D=projectors&sfm%5Bkeywords%5D%5B15%5D%5Bkey%5D=notebooks&sfm%5Bkeywords%5D%5B15%5D%5Bvalue%5D=notebooks&sfm%5Bdates%5D%5BpublishedDate%5D%5BpublishedDateSelect%5D=pastWeek".format(str(self.at_page)),


    def pagination(self):
        self.driver.get("https://beta.sam.gov/search/results?index=opp&page={}&sort=-relevance&sfm%5Bstatus%5D%5Bis_active%5D=true&sfm%5Bkeywords%5D%5B0%5D%5Bkey%5D=headphones&sfm%5Bkeywords%5D%5B0%5D%5Bvalue%5D=headphones&sfm%5Bkeywords%5D%5B1%5D%5Bkey%5D=monitors&sfm%5Bkeywords%5D%5B1%5D%5Bvalue%5D=monitors&sfm%5Bkeywords%5D%5B2%5D%5Bkey%5D=displays&sfm%5Bkeywords%5D%5B2%5D%5Bvalue%5D=displays&sfm%5Bkeywords%5D%5B3%5D%5Bkey%5D=notebooks&sfm%5Bkeywords%5D%5B3%5D%5Bvalue%5D=notebooks&sfm%5Bkeywords%5D%5B4%5D%5Bkey%5D=tablets&sfm%5Bkeywords%5D%5B4%5D%5Bvalue%5D=tablets&sfm%5Bkeywords%5D%5B5%5D%5Bkey%5D=projectors&sfm%5Bkeywords%5D%5B5%5D%5Bvalue%5D=projectors&sfm%5Bkeywords%5D%5B6%5D%5Bkey%5D=smartphones&sfm%5Bkeywords%5D%5B6%5D%5Bvalue%5D=smartphones".format(str(self.at_page)))
        time.sleep(10)

    def go_to_start_page(self):
        time.sleep(10)
        while self.start_page < self.at_page:
            self.pagination()
            self.start_page += 1

    def get_table(self):
        time.sleep(5)
        result = self.driver.find_element_by_id("search-results")
        return result.find_elements_by_class_name("opportunity-title")

    def go_back(self):
        print(self.current_link)
        self.driver.get("https://beta.sam.gov/search/results?index=opp&page={}&sort=-relevance&sfm%5Bstatus%5D%5Bis_active%5D=true&sfm%5Bkeywords%5D%5B0%5D%5Bkey%5D=headphones&sfm%5Bkeywords%5D%5B0%5D%5Bvalue%5D=headphones&sfm%5Bkeywords%5D%5B1%5D%5Bkey%5D=monitors&sfm%5Bkeywords%5D%5B1%5D%5Bvalue%5D=monitors&sfm%5Bkeywords%5D%5B2%5D%5Bkey%5D=displays&sfm%5Bkeywords%5D%5B2%5D%5Bvalue%5D=displays&sfm%5Bkeywords%5D%5B3%5D%5Bkey%5D=notebooks&sfm%5Bkeywords%5D%5B3%5D%5Bvalue%5D=notebooks&sfm%5Bkeywords%5D%5B4%5D%5Bkey%5D=tablets&sfm%5Bkeywords%5D%5B4%5D%5Bvalue%5D=tablets&sfm%5Bkeywords%5D%5B5%5D%5Bkey%5D=projectors&sfm%5Bkeywords%5D%5B5%5D%5Bvalue%5D=projectors&sfm%5Bkeywords%5D%5B6%5D%5Bkey%5D=smartphones&sfm%5Bkeywords%5D%5B6%5D%5Bvalue%5D=smartphones".format(str(self.at_page)))
        time.sleep(15)


    def click_links(self):
        opps = self.get_table()
        opps[self.at_opp].find_element_by_tag_name("a").click()
        time.sleep(10)
        info = self.extract_sam_info()
        self.go_back()
        return info

    def extract_sam_info(self):
        title = self.try_extraction(self.driver.find_element_by_xpath('//h1[@class="\'sam-ui-header"]'))
        reference_id = self.try_extraction(self.try_by_id("header-solicitation-number")
                                      .find_element_by_class_name("description"))
        try:
            description = self.try_extraction(
                self.try_by_id("description").find_element_by_class_name("ng-star-inserted"))
        except Exception:
            logging.error("Exception occurred", exc_info=True)
            description = None
        published = self.split_text(self.try_extraction(self.try_by_id("general-original-published-date")))
        gen_type = self.split_text(self.try_extraction(self.try_by_id("general-type")))
        naics = self.split_text(self.try_extraction(self.try_by_id("classification-naics-code")))
        pcs = self.split_text(self.try_extraction(self.try_by_id("classification-classification-code")))
        name = self.try_by_id("contact-primary-poc-full-name")
        if name is not None:
            name = name.text
        else:
            name = None
        phone = self.try_extraction(self.try_by_id("contact-primary-poc-phone"))
        contractor = self.try_by_id("-contracting-office")
        if contractor is not None:
            contractor = contractor.find_element_by_class_name("ng-star-inserted").text
        else:
            contractor = None

        if description is not None:
            find_tco = self.find_text(description.strip(), r'((Tco|TCO|tco).\w+|(\w+).(Tco|TCO|tco))')
            find_epeat = self.find_text(description.strip(), r'((Epeat|EPEAT|epeat).\w+|(\w+).(Epeat|EPEAT|epeat))')
            if len(description) > 40000:
                description = description[:40000]
        else:
            find_tco = None
            find_epeat = None

        info = [self.driver.current_url,
                published,
                gen_type,
                title,
                reference_id,
                self.try_extraction(self.driver.find_element_by_xpath(
                    "//*[text()=' Department/Ind. Agency ']/following-sibling::div")),
                naics,
                pcs,
                description,
                contractor,
                name,
                phone,
                self.try_extraction(self.try_by_id("contact-primary-poc-email")),
                find_tco,
                find_epeat
                ]

        for height in range(10):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/{});".format(height))
            time.sleep(5)

        try:
            print(self.driver.find_element_by_class_name("usa-accordion-button").text)
            if self.driver.find_element_by_class_name("usa-accordion-button").text != "Links":
                self.driver.find_element_by_xpath("//*[@class='fa fa-cloud-download']").click()
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)
            pass

        time.sleep(60)
        if reference_id is not None:
            folder_name = reference_id
        else:
            folder_name = title
        file_operator = HandleFiles(folder_name, self.doc_folder_id)
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

        return info

    def try_by_id(self, id):
        try:
            result = self.driver.find_element_by_id(id)
        except NoSuchElementException:
            logging.error("Exception occurred", exc_info=True)
            result = None
        return result

    def try_extraction(self, query):
        try:
            extraction = query.text
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            extraction = None
        return extraction

    def split_text(self, ext):
        if ext is not None:
            result = ext.split(":")[1]
        return result

    def find_text(self, soup, regex):
        matchobj = re.search(regex, soup)
        if matchobj:
            item = matchobj.group()
        else:
            item = None
        return item




