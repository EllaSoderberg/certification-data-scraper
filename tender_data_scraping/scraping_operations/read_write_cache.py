"""
Functions to read and write to a cache file. Separate for each scraper. Stored in the same folder as the scraper as a pickle.
{
name: "project_name",
last_run: "2021-07-30",
run_successful: True,
sheet_id: "sfdjn23434k2n23kn34kj",
last_tender_title: "Tender for laptops",
last_tender_published: "2021-07-27",
at_page: 3,
at_opp: 2,
}
"""
import pickle
import os
from dotenv import load_dotenv

load_dotenv()

proj_path = os.environ.get("PROJECT_PATH")


def read_cache(project_name):
    os.chdir(proj_path)
    file_path = "cache/{}.p".format(project_name)
    if not os.path.exists(file_path):
        file_path = "cache/template_cache.p"
    with open(file_path, "rb") as cache_file:
        project_info = pickle.load(cache_file)
    return project_info


def write_cache(project_name, data):
    os.chdir(proj_path)
    with open("cache/{}.p".format(project_name), "wb") as cache_file:
        pickle.dump(data, cache_file)
