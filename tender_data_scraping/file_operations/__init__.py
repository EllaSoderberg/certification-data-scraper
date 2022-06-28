from dotenv import load_dotenv
import os


proj_path = os.environ.get("TEMP_FOLDER")
#listan = os.listdir("/Users/feliciaatterling/Documents/GitHub/certification-data-scraper/")
new_path = os.path.join('/Users/feliciaatterling/Documents/GitHub/certification-data-scraper/' , 'temp')
os.chdir(new_path)
