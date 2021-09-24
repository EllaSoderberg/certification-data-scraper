from dotenv import load_dotenv
import os

load_dotenv()

proj_path = os.environ.get("TEMP_FOLDER")
os.chdir(proj_path)
