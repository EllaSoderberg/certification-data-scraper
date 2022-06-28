from scrapers.TED_europe import TED
from scrapers.TED_expanded import TedExpanded
from scrapers.TED_prior_notice import TedPriorNotice
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
    dict = {'last_run': '2022-05-26',
            'run_successful': True,
            'sheet_id': None,
            'last_tender_title': '3610--EPSON P20000 64-INCH PRINTER - " BRAND NAME OR EQUAL TO EPSON" IAW SALIENT FEATURES AS SPECIFIED IN SOW',
            'last_tender_published': "2022-05-26",
            'first_tender_title': None,
            'first_tender_published': None,
            'at_page': 0,
            'at_opp': 0}

    read_write_cache.write_cache(file, dict)


def update_cache(file):
    dict = read(file)
    dict.update({
        'last_run': '2022-04-19'
    })
    read_write_cache.write_cache(file, dict)

def check_doneness():
    db_names = ["TED", "TED_expanded", "Gebiz", "Eprocure", "SamGov", "Evergabe"]
    for name in db_names:
        cache = read_write_cache.read_cache(name)
        print("{} run successful: {}, at date {}".format(name, cache["run_successful"], cache["last_run"]))

if __name__ == '__main__':
    #TED().run()
    #TedExpanded().run()
    TedPriorNotice().run()
    #Gebiz().run()
    #Eprocure().run()
    #SamGov().run()
    #Evergabe().run()

    #Merx().run()
    #Tendium().run()
    #write_to_cache("SamGov")
    #update_cache("TedPriorNotice")
    #print(read("SamGov"))
    #check_doneness()