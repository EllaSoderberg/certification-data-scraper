from scrapers.TED_europe import TED
from scrapers.TED_expanded import TedExpanded
from scrapers.gebiz_singapore import Gebiz
from scraping_operations import read_write_cache
from scrapers.eavrop_sweden import Eavrop
from scrapers.eprocure_india import Eprocure
from scrapers.tendium import Tendium
from scrapers.sam_gov_us import SamGov
from scrapers.merx_canada import Merx
from scrapers.evergabe_germany import Evergabe

def read(file):
    return read_write_cache.read_cache(file)


def write_to_cache(file):
    dict = {
        'last_run': '2021-09-21',
         'run_successful': True,
         'sheet_id': None,
         'last_tender_title': 'Combined Synopsis/Solicitation (Updated)',
         'last_tender_published': '2021-09-13',
         'first_tender_title': None,
         'first_tender_published': None,
         'at_page': 0,
         'at_opp': 0

    }
    read_write_cache.write_cache(file, dict)


def update_cache(file):
    dict = read(file)
    dict.update({'first_tender_title': None, 'first_tender_published': None })
    read_write_cache.write_cache(file, dict)


if __name__ == '__main__':
    #TED().run()
    #TedExpanded().run()
    #Gebiz().run()
    #Eprocure().run()
    #Tendium().run()
    SamGov().run()
    #Merx().run()
    #Evergabe().run()

    #write_to_cache("SamGov")
    #update_cache("SamGov")
    print(read("SamGov"))