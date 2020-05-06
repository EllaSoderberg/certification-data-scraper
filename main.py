from Scrapers.Europe.TED import run_ted
from Scrapers.Europe.vergabe import run_evergabe
from Scrapers.Asia.EprocureIn import run_eprocurein
from Scrapers.Asia.gebiz import run_gebiz
from selenium import webdriver


date = "2020-05-05"
ted_link = "https://ted.europa.eu/TED/browse/browseByMap.do"
evergabe_link = "https://www.evergabe.nrw.de/VMPCenter/common/project/search.do?method=showExtendedSearch&fromExternal=true#eyJjcHZDb2RlcyI6W3sibmFtZSI6IkFyYmVpdHNwbMOkdHplIiwiY29kZSI6IjMwMjE0MDAwLTIifSx7Im5hbWUiOiJCaWxkc2NoaXJtZSIsImNvZGUiOiIzMDIzMTMwMC0wIn0seyJuYW1lIjoiQ29tcHV0ZXJiaWxkc2NoaXJtZSB1bmQgS29uc29sZW4iLCJjb2RlIjoiMzAyMzEwMDAtNyJ9LHsibmFtZSI6IkZlcm5zcHJlY2hrb3BmaMO2cmVyZ2Fybml0dXJlbiIsImNvZGUiOiIzMjU1MTMwMC0zIn0seyJuYW1lIjoiRmlsbXZvcmbDvGhyZ2Vyw6R0ZSIsImNvZGUiOiIzODY1MjAwMC0wIn0seyJuYW1lIjoiUGVyc29uYWxjb21wdXRlciIsImNvZGUiOiIzMDIxMzAwMC01In0seyJuYW1lIjoiVGFibGV0dGNvbXB1dGVyIiwiY29kZSI6IjMwMjEzMjAwLTcifSx7Im5hbWUiOiJUYXNjaGVuY29tcHV0ZXIiLCJjb2RlIjoiMzAyMTM1MDAtMCJ9LHsibmFtZSI6IlRpc2NoY29tcHV0ZXIiLCJjb2RlIjoiMzAyMTMzMDAtOCJ9LHsibmFtZSI6IlRyYWdiYXJlIENvbXB1dGVyIiwiY29kZSI6IjMwMjEzMTAwLTYifV0sImNvbnRyYWN0aW5nUnVsZXMiOlsiVk9MIiwiVk9CIiwiVlNWR1YiLCJTRUtUVk8iLCJPVEhFUiJdLCJwdWJsaWNhdGlvblR5cGVzIjpbIlRlbmRlciJdLCJkaXN0YW5jZSI6MCwicG9zdGFsQ29kZSI6IiIsIm9yZGVyIjoiMCIsInBhZ2UiOiIxIiwic2VhcmNoVGV4dCI6IiIsInNvcnRGaWVsZCI6IlBST0pFQ1RfUFVCTElDQVRJT05fREFURV9MTkcifQ"
eprocure_link = "https://eprocure.gov.in/cppp/searchbyproduct/byUjI5dlpITT1BMTNoMVEyOXRjSFYwWlhJZ1NHRnlaSGRoY21VPUExM2gxY0hWaWJHbHphR1ZrWDJSaGRHVT1BMTNoMWMyRnNkQT09"
gebiz_link = "https://www.gebiz.gov.sg/ptn/loginGeBIZID.xhtml"
driver = webdriver.Chrome('C:/Users/Ella/Desktop/Drivers/chromedriver')

print("Running Evergabe...")
run_evergabe(driver, date, evergabe_link, False, 2, 1)  # 2 rows
print("Done with Evergabe...")

"""
print("Running TED...")
run_ted(driver, ted_link, "20200502 <> 20200506", date, 1)
print("Done with TED...")

print("Running Eprocure...")
run_eprocurein(driver, date, eprocure_link, False, 1, 9, 1)  # 9 rows
print("Done with Eprocure...")
print("Running Gebiz...")
run_gebiz(driver, gebiz_link, date, False, 1, 2, 1)  # 2 rows
print("Done with Gebiz...")
"""


