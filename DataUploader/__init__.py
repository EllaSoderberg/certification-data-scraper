from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']


class Sheet:
    def __init__(self, folder_id, project, date):
        self.folder_id = folder_id
        self.project_name = project + " " + date
        self.creds = self.check_credentials()
        self.sheet_id = self.new_sheet()
        self.add_banded_range()

    def check_credentials(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

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
            spreadsheetId=self.sheet_id, range="Blad1", valueInputOption="USER_ENTERED", body=sheet_header).execute()

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
        service = build('sheets', 'v4', credentials=self.creds)
        sheet_header = {
            'values': values
        }
        service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id, range="Blad1", valueInputOption="USER_ENTERED", body=sheet_header,
            fields="tableRange").execute()
