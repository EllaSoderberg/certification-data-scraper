from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import os


def new_chrome_browser(executable_path, download_path=None):
    """ Helper function that creates a new Selenium browser """
    options = Options()
    if download_path is not None:
        os.makedirs(download_path, exist_ok=True)
        options.add_experimental_option("prefs", {
            "download.default_directory": download_path,
            #"download.directory_upgrade": True,
            #"safebrowsing.enabled": True,
            #"download.prompt_for_download": False,
        })
    #driver = webdriver.Chrome(service=Service('/Users/feliciaatterling/desktop/chromedriver'))
    print(executable_path)
    driver = webdriver.Chrome(options=options, service=Service(executable_path))
    return driver
