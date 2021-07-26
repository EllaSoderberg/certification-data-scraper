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
from Scrapers.Europe.TED_class2 import TED2
from Scrapers.Asia.gebiz_class import Gebiz
from Scrapers.Europe.vergabe_class import Evergabe
from Scrapers.Asia.eprocure import Eprocure
from Scrapers.US.SamGov import SamGov
from Scrapers.US.bidsearch import BidSearch
from Scrapers.US.merx import Merx

this_week = "https://beta.sam.gov/search?index=opp&sort=-relevance&page=1&keywords=%22all-in-one%22%20laptop%20laptops%20computer%20workstation%20hp%20philips%20dell%20lenovo%20desktop%20display&inactive_filter_values=false&naics=334&notice_type=k&opp_inactive_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_publish_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%222020-06-11%22,%22endDate%22:%222020-06-18%22%7D%7D&opp_modified_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&opp_response_date_filter_model=%7B%22dateRange%22:%7B%22startDate%22:%22%22,%22endDate%22:%22%22%7D%7D&date_filter_index=0"

today = date.today()

logging.basicConfig(filename='{}.log'.format(today), filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


def main():
    #BidSearch(end_opp=100, end_page=1, at_opp=1, sheet_id=None).run()
    #TED2(end_page=8, date_range="20210625 <> 20210705", sheet_id=None).run()
    #TED(end_page=4, date_range="20210625 <> 20210705", sheet_id=None).run()
    #Gebiz(end_opp=3, end_page=2, at_page=1, at_opp=1, doc_id=None).run()
    #Evergabe(end_opp=5, end_page=1).run()
    #Eprocure(end_opp=2, end_page=3, at_opp=1, at_page=1, sheet_id=None).run()
    #SamGov(end_opp=9, end_page=15, sheet_id=None).run()
    Merx(end_opp=20, end_page=1, sheet_id="114evang1GNgl3pgmKIvtlhjPYkBY5cmtK_r22iW2ZC4").run()



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


