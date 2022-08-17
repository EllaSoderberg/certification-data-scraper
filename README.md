# tender-data-scraping
 A project for scraping tender data and looking for specific keywords

# Prerequisits 
- Python 3.9
- The python package [Pipenv](https://pipenv.pypa.io/en/latest/)
- Chrome and [ChromeDriver](https://chromedriver.chromium.org/downloads) installed.

# Getting started
1. Clone the project
2. Open cmd and go to the project folder 
3. Run pipenv install. This will install all required packages on your system. 
4. Create a .env file based upon .env.example and change the PROJECT_PATH variable to point to the root folder of the project and DRIVER_PATH to point to the chromedriver execution file.
5. Create a google cloud account and add the credentials file to the root folder
   
# To run the script
1. run 'py pipenv shell' or 'py -m pipenv shell' (or your own virtual environment) to start the virtual environment
2. go to the folder "tender_data_scraping", 'cd tender_data_scraping'
3. Uncomment the script you want to run
4. Run main by writing ´py main.py´
5. Wait for the script to run. If there are any problems, fix and rerun, if running eprocure, fill in captchas.
6. Repeat from 3 for new script

# Procedure
1. Each script for each database in the main.py file is run (about) once per week (TED, Gebiz, eprocure..)
2. Send PEG an email with the links to the scraped files

# To think about
- When adding a new database and a login is required, read the terms and conditions. If it says scraping is not allowed, don't scrape the database. 

