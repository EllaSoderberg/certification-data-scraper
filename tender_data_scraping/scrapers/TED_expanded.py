import datetime
from . import TED_europe


class TedExpanded(TED_europe.TED):
    def __init__(self):
        super(TedExpanded, self).__init__(
            sheet_folder_id="1jsaSTs3XdfPxO5wSY0HQEERZY7vN6wfA",
            project="TED_Expanded",
        )
        self.search = "PD=[{} <> {}] AND PC=[30200000] AND TD=[3]".format((self.last_run + datetime.timedelta(days=1))
                                                                          .strftime("%Y%m%d"),
                                                                          self.today.strftime("%Y%m%d"))
