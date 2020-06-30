import logging
from ScrapingTools import read_write


class Runner:
    def __init__(self, project, end_opp, end_page):
        self.project = project
        self.data_list = []
        self.first_run = first_run
        self.table_len = 10
        self.start_opp = 1
        self.at_opp = 1
        self.end_opp = end_opp
        self.start_page = 1
        self.at_page = 1
        self.end_page = end_page
        self.retries = 0
        self.first_page = True

    def calc_range(self):
        if self.first_page and self.end_page == self.at_page:
            run_range = range(self.start_opp - 1, self.stop_opp)
        elif self.first_page:
            run_range = range(self.start_opp - 1, self.table_len)
        elif self.end_page == self.at_page:
            run_range = range(self.end_opp)
        else:
            run_range = range(self.table_len)
        return run_range
