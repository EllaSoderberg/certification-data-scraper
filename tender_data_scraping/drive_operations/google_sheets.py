from __future__ import print_function
from . import check_creds
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']


class Sheet:
    def __init__(self, folder_id, project, date, sheet_id=None):
        self.folder_id = folder_id
        self.project_name = project + " " + str(date)
        self.creds = check_creds()
        if not sheet_id:
            self.sheet_id = self.new_sheet()
            self.add_banded_range()
        else:
            self.sheet_id = sheet_id

    def new_sheet(self):
        service = build('drive', 'v3', credentials=self.creds)
        sheet_body = {
            'name': self.project_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': [self.folder_id]
        }
        results = service.files().create(body=sheet_body, fields='id').execute()
        return results.get('id')

    def init_sheet(self, header):
        service = build('sheets', 'v4', credentials=self.creds)
        sheet_header = {
            'values': [header]
        }
        service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id, range="Sheet1", valueInputOption="USER_ENTERED", body=sheet_header).execute()

        requests = [{
            "updateSheetProperties":
                {
                    "properties": {
                        "gridProperties": {
                            "frozenRowCount": 1
                        }
                    },
                    "fields": "gridProperties.frozenRowCount"
                }
        }]

        freeze_row = {
            "requests": requests,
        }

        request = service.spreadsheets().batchUpdate(spreadsheetId=self.sheet_id,
                                                     body=freeze_row)
        request.execute()

    def add_banded_range(self):
        service = build('sheets', 'v4', credentials=self.creds)

        request = [
            {
                "addBanding": {
                    "bandedRange": {
                        "range": {"sheetId": 0},
                        "rowProperties": {
                            'headerColor': {
                                'red': 0.3882353,
                                'green': 0.8235294,
                                'blue': 0.5921569
                            },
                            'firstBandColor': {
                                'red': 1,
                                'green': 1,
                                'blue': 1
                            },
                            'secondBandColor': {
                                'red': 0.90588236,
                                'green': 0.9764706,
                                'blue': 0.9372549
                            },
                            'headerColorStyle': {
                                'rgbColor': {
                                    'red': 0.3882353,
                                    'green': 0.8235294,
                                    'blue': 0.5921569
                                }
                            },
                            'firstBandColorStyle': {
                                'rgbColor': {
                                    'red': 1,
                                    'green': 1,
                                    'blue': 1
                                }
                            },
                            'secondBandColorStyle': {
                                'rgbColor': {
                                    'red': 0.90588236,
                                    'green': 0.9764706,
                                    'blue': 0.9372549
                                }
                            }
                        }
                    }
                }
            }

        ]
        banding = {
            "requests": request,
        }
        request = service.spreadsheets().batchUpdate(spreadsheetId=self.sheet_id,
                                                     body=banding)
        request.execute()

    def append_row(self, values):
        print("uploadign", values)

        for i in range(len(values[0])):
            if values[0][i] and len(values[0][i]) > 40000:
                values[0][i] = values[0][i][:40000]


        service = build('sheets', 'v4', credentials=self.creds)
        sheet_header = {
            'values': values
        }
        service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id, range="Sheet1", valueInputOption="RAW", body=sheet_header,
            fields="tableRange").execute()


def create_sheet(sheet_folder_id, project, date, header):
    sheet = Sheet(sheet_folder_id, project, date)
    sheet.init_sheet(header)
    return sheet


def init_sheet_from_id(sheet_folder_id, project, date, sheet_id):
    sheet = Sheet(sheet_folder_id, project, date, sheet_id=sheet_id)
    return sheet
