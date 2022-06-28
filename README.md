# tender-data-scraping
 A project for scraping tender data and looking for specific keywords

# Prerequisits 
- Python 3.9
- The python package [Pipenv](https://pipenv.pypa.io/en/latest/)
- Chrome and [ChromeDriver](https://chromedriver.chromium.org/downloads) installed.

# Getting started
1. Clone the project
2. Open command line and go to the project folder 
3. Run "pipenv install". This will install all required packages on your system. 
4. Create a .env file based upon .env.example and change the PROJECT_PATH variable to point to the root folder of the project and DRIVER_PATH to point to the chromedriver execution file.
5. Create a folder in the root directory named "temp"
6. Create a google cloud account and add the credentials file to the root folder
7. Run 'py pipenv shell' to start the virtual environment
8. Go to the folder "tender_data_scraping" and run "py main.py" 

# Todo
- Explain step five better
- Add todos in bitbucket
