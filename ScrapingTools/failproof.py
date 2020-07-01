import logging
from ScrapingTools import read_write


class Runner:
    def __init__(self, project, end_opp, end_page):
        self.project = project
        self.data_list = []
        self.first_run = True
        self.table_len = 10
        self.start_opp = 1
        self.at_opp = self.start_opp
        self.end_opp = end_opp
        self.start_page = 1
        self.at_page = self.start_page
        self.end_page = end_page
        self.retries = 0
        self.first_page = True

    def calc_range(self):
        if self.at_page == self.end_page:
            run_range = range(self.at_opp - 1, self.end_opp - 1)
        else:
            run_range = range(self.at_opp - 1, self.table_len)
        return run_range
