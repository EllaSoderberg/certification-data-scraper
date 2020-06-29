from Scrapers.Europe.TED import run_ted
from Scrapers.Europe.vergabe import run_evergabe
from Scrapers.Asia.EprocureIn import run_eprocurein
from Scrapers.Asia.gebiz import run_gebiz, save_gebiz
#from Scrapers.Asia.gebiz_full import run_gebiz, save_gebiz
from selenium import webdriver
from ScrapingTools import read_write



date = "2020-06-26-2"
ted_link = "https://ted.europa.eu/TED/browse/browseByMap.do"
evergabe_link = "https://www.evergabe.nrw.de/VMPCenter/common/project/search.do?method=showExtendedSearch&fromExternal=true#eyJjcHZDb2RlcyI6W3sibmFtZSI6IkFyYmVpdHNwbMOkdHplIiwiY29kZSI6IjMwMjE0MDAwLTIifSx7Im5hbWUiOiJCaWxkc2NoaXJtZSIsImNvZGUiOiIzMDIzMTMwMC0wIn0seyJuYW1lIjoiQ29tcHV0ZXJiaWxkc2NoaXJtZSB1bmQgS29uc29sZW4iLCJjb2RlIjoiMzAyMzEwMDAtNyJ9LHsibmFtZSI6IkZlcm5zcHJlY2hrb3BmaMO2cmVyZ2Fybml0dXJlbiIsImNvZGUiOiIzMjU1MTMwMC0zIn0seyJuYW1lIjoiRmlsbXZvcmbDvGhyZ2Vyw6R0ZSIsImNvZGUiOiIzODY1MjAwMC0wIn0seyJuYW1lIjoiUGVyc29uYWxjb21wdXRlciIsImNvZGUiOiIzMDIxMzAwMC01In0seyJuYW1lIjoiVGFibGV0dGNvbXB1dGVyIiwiY29kZSI6IjMwMjEzMjAwLTcifSx7Im5hbWUiOiJUYXNjaGVuY29tcHV0ZXIiLCJjb2RlIjoiMzAyMTM1MDAtMCJ9LHsibmFtZSI6IlRpc2NoY29tcHV0ZXIiLCJjb2RlIjoiMzAyMTMzMDAtOCJ9LHsibmFtZSI6IlRyYWdiYXJlIENvbXB1dGVyIiwiY29kZSI6IjMwMjEzMTAwLTYifV0sImNvbnRyYWN0aW5nUnVsZXMiOlsiVk9MIiwiVk9CIiwiVlNWR1YiLCJTRUtUVk8iLCJPVEhFUiJdLCJwdWJsaWNhdGlvblR5cGVzIjpbIlRlbmRlciJdLCJkaXN0YW5jZSI6MCwicG9zdGFsQ29kZSI6IiIsIm9yZGVyIjoiMCIsInBhZ2UiOiIxIiwic2VhcmNoVGV4dCI6IiIsInNvcnRGaWVsZCI6IlBST0pFQ1RfUFVCTElDQVRJT05fREFURV9MTkcifQ"
eprocure_link = "https://eprocure.gov.in/cppp/searchbyproduct/byUjI5dlpITT1BMTNoMVEyOXRjSFYwWlhJZ1NHRnlaSGRoY21VPUExM2gxY0hWaWJHbHphR1ZrWDJSaGRHVT1BMTNoMWMyRnNkQT09"
gebiz_link = "https://www.gebiz.gov.sg/ptn/loginGeBIZID.xhtml"
driver = webdriver.Chrome(executable_path='C:/Users/Movie Computer/Desktop/drivers/chromedriver.exe')

"""
print("Running Gebiz...")
run_gebiz(driver, gebiz_link, date, False, 1, 1, 7, 1)  # 3 rows
print("Done with Gebiz...")
"""

print("Running Gebiz...")
run_gebiz(driver, gebiz_link, date, is_rerun=False, num_pages=1, start_page=1, stop_opp=9, start_opp=1)
print("Done with Gebiz...")



"""
print("Running Eprocure...")
run_eprocurein(driver, date, eprocure_link, is_rerun=True, num_pages=3, start_page=1, stop_opp=1, start_opp=4)  # 12 rows
print("Done with Eprocure...")
print("Running Evergabe...")
run_evergabe(driver, date, evergabe_link, True, 2, 1)  # 2 rows
print("Done with Evergabe...")

print("Running Gebiz...")
run_gebiz(driver, gebiz_link, date, is_rerun=True, num_pages=2, start_page=1, stop_opp=2, start_opp=8)
print("Done with Gebiz...")


print("Running TED...")
contacts = run_ted(driver, ted_link, "20200620 <> 20200626", date, 2)
print("Done with TED...")
print("len contacts", len(contacts))
unique = list(set(contacts))
print("len unique", len(unique))
read_write.save_pickle(unique, "TED_contacts_new.p")




"""


