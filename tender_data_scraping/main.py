from scrapers.TED_europe import TED
from scrapers.TED_expanded import TedExpanded
from scrapers.TED_prior_notice import TedPriorNotice
from scrapers.gebiz_singapore import Gebiz
from scraping_operations import read_write_cache
from scrapers.eavrop_sweden import Eavrop
from scrapers.eprocure_india import Eprocure
from scrapers.sam_gov_us import SamGov
from scrapers.merx_canada import Merx
from scrapers.evergabe_germany import Evergabe


def read(file):
    return read_write_cache.read_cache(file)


def write_to_cache(file):
    """
    Overwrites the cache of the cache-file specified
    :param file: name of the cache-file
    """
    dict = {'last_run': '2022-08-17',
            'run_successful': True,
            'sheet_id': None,
            'last_tender_title': 'Supply, Installation, Testing and Commissioning of DELL EMC Hot Plug Serial Attached SCSI SAS Hard Disk Drive',
            'last_tender_published': '2022-06-14',
            'first_tender_title': None,
            'first_tender_published': None,
            'at_page': 0,
            'at_opp': 0}

    read_write_cache.write_cache(file, dict)


def update_cache(file):
    """
    Updates fields in a cache-file
    :param file: name of the cache-file
    """
    dict = read(file)
    dict.update({
        'at_page': 0,
        'at_opp': 0
    })
    read_write_cache.write_cache(file, dict)

def check_doneness():
    """
    Function that prints the status of the scripts
    """
    db_names = ["TED", "TED_expanded", "Gebiz", "Eprocure", "SamGov", "Evergabe"]
    for name in db_names:
        cache = read_write_cache.read_cache(name)
        print("{} run successful: {}, at date {}".format(name, cache["run_successful"], cache["last_run"]))

if __name__ == '__main__':
    # Relevant scripts
    #TED().run()
    #TedExpanded().run()
    #TedPriorNotice().run()
    #Gebiz().run()
    #Eprocure().run() # The only one where you need to monitor by filling in captchas (about 3-5 in the beginning)
    #SamGov().run()
    #Evergabe().run()

    # Utdaterade skript (pga. GDPR)
    #Merx().run()

    # Funktioner för att kolla vilka skript som körts och för att ändra cache.
    # print(read("SamGov"))
    #write_to_cache("SamGov")
    #update_cache("TED_priornotice")
    #check_doneness()