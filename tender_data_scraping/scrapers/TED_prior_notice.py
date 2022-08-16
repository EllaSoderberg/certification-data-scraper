from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
import datetime
from . import TED_europe


class TedPriorNotice(TED_europe.TED):
    def __init__(self):
        super(TedPriorNotice, self).__init__(
            sheet_folder_id="1gIDkP1eEEid0kPywsUIpMBTuGKY2_twd",
            project="TED_PriorNotice",
        )
        self.search = "PD=[{} <> {}] AND PC=[30200000 or 38652000 or 32551300 or 32252000] AND TD=[I or 0 or 4 or A]".format((self.last_run + datetime.timedelta(days=1))
                                                                          .strftime("%Y%m%d"),
                                                                          self.today.strftime("%Y%m%d"))