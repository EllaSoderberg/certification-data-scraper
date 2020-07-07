"""
from Scrapers.Europe.TED import run_ted
from Scrapers.Europe.vergabe import run_evergabe
from Scrapers.Asia.EprocureIn import run_eprocurein
from Scrapers.Asia.eprocure import Eprocure

from Scrapers.Asia.gebiz import run_gebiz, save_gebiz
from Scrapers.US.SamGov import run_sam
#from Scrapers.Asia.gebiz_full import run_gebiz, save_gebiz
from ScrapingTools import read_write
"""
import logging
from datetime import date
from Scrapers.Europe.TED_class import TED


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


ted_link = "https://ted.europa.eu/TED/browse/browseByMap.do"
evergabe_link = "https://www.evergabe.nrw.de/VMPCenter/common/project/search.do?method=showExtendedSearch&fromExternal=true#eyJjcHZDb2RlcyI6W3sibmFtZSI6IkFyYmVpdHNwbMOkdHplIiwiY29kZSI6IjMwMjE0MDAwLTIifSx7Im5hbWUiOiJCaWxkc2NoaXJtZSIsImNvZGUiOiIzMDIzMTMwMC0wIn0seyJuYW1lIjoiQ29tcHV0ZXJiaWxkc2NoaXJtZSB1bmQgS29uc29sZW4iLCJjb2RlIjoiMzAyMzEwMDAtNyJ9LHsibmFtZSI6IkZlcm5zcHJlY2hrb3BmaMO2cmVyZ2Fybml0dXJlbiIsImNvZGUiOiIzMjU1MTMwMC0zIn0seyJuYW1lIjoiRmlsbXZvcmbDvGhyZ2Vyw6R0ZSIsImNvZGUiOiIzODY1MjAwMC0wIn0seyJuYW1lIjoiUGVyc29uYWxjb21wdXRlciIsImNvZGUiOiIzMDIxMzAwMC01In0seyJuYW1lIjoiVGFibGV0dGNvbXB1dGVyIiwiY29kZSI6IjMwMjEzMjAwLTcifSx7Im5hbWUiOiJUYXNjaGVuY29tcHV0ZXIiLCJjb2RlIjoiMzAyMTM1MDAtMCJ9LHsibmFtZSI6IlRpc2NoY29tcHV0ZXIiLCJjb2RlIjoiMzAyMTMzMDAtOCJ9LHsibmFtZSI6IlRyYWdiYXJlIENvbXB1dGVyIiwiY29kZSI6IjMwMjEzMTAwLTYifV0sImNvbnRyYWN0aW5nUnVsZXMiOlsiVk9MIiwiVk9CIiwiVlNWR1YiLCJTRUtUVk8iLCJPVEhFUiJdLCJwdWJsaWNhdGlvblR5cGVzIjpbIlRlbmRlciJdLCJkaXN0YW5jZSI6MCwicG9zdGFsQ29kZSI6IiIsIm9yZGVyIjoiMCIsInBhZ2UiOiIxIiwic2VhcmNoVGV4dCI6IiIsInNvcnRGaWVsZCI6IlBST0pFQ1RfUFVCTElDQVRJT05fREFURV9MTkcifQ"
eprocure_link = "https://eprocure.gov.in/cppp/searchbyproduct/byUjI5dlpITT1BMTNoMVEyOXRjSFYwWlhJZ1NHRnlaSGRoY21VPUExM2gxY0hWaWJHbHphR1ZrWDJSaGRHVT1BMTNoMWMyRnNkQT09"
gebiz_link = "https://www.gebiz.gov.sg/ptn/loginGeBIZID.xhtml"
today = date.today()

logging.basicConfig(filename='{}.log'.format(today), filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def main():
    #eprocure = Eprocure(end_opp=1, end_page=1)
    ted = TED(end_page=2, date_range="20200620 <> 20200626")
    ted.run()
    #eprocure.run()
    """
    run_eprocurein(driver, today, eprocure_link, end_opp=2, end_page=1)  # 12 rows
    
    logging.info("Running Gebiz...")
    run_gebiz(driver, gebiz_link, today, is_rerun=False, num_pages=2, start_page=1, stop_opp=1, start_opp=8)
    logging.info("Done with Gebiz...")
    print("Running Sam.gov...")
    run_sam(driver, this_week, today, is_rerun=False, num_pages=8, start_page=1, start_opp=1, stop_opp=10)
    logging.info("Running Evergabe...")
    run_evergabe(driver, today, evergabe_link, False, 2, 1)  # 2 rows
    logging.info("Done with Evergabe...")
    logging.info("Running TED...")
    contacts = run_ted(driver, ted_link, "20200620 <> 20200626", today, 2)
    logging.info("Done with TED...")
    logging.info("len contacts", len(contacts))
    unique = list(set(contacts))
    logging.info("len unique", len(unique))
    read_write.save_pickle(unique, "temp_files/TED_contacts_new.p")
    """


if __name__ == '__main__':
    main()


