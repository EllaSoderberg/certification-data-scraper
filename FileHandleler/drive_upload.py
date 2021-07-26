from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload
import io

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
proj_path = "C:\\Users\\Ella_\\Desktop\\certification-data-scraper"


def check_creds(creds=None):
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    os.chdir(proj_path)
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


def new_folder(service, dest_folder, folder_name):
    """
    Create a new folder under a decided folder
    :param service: The ongoing session object
    :param dest_folder: the ID of the destination folder
    :param folder_name: The name of the new folder
    :return: the link to the new folder
    """

    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [dest_folder]
    }

    file = service.files().create(body=file_metadata, fields='webViewLink, id').execute()
    return file.get('id'), file.get("webViewLink")


def upload_files(service, folder, files):
    """
    Upload files to a selected folder
    :param service: The ongoing session object
    :param folder: The ID of the folder the files should be uploaded to
    :param files: The path to the files to be uploaded
    """
    for file in files:
        name = file.split("\\")[-1]
        file_metadata = {
            'name': name,
            'parents': [folder]
        }
        media = MediaFileUpload(file,
                                mimetype='application/pdf')
        service.files().create(body=file_metadata,
                               media_body=media,
                               fields='id').execute()


def upload_to_drive(folder_name, dest_folder, file_names, path="C:\\Users\\Movie Computer\\Downloads"):
    """
    Creates a new folder and uploads files to drive
    :param folder_name: The name of the new folder
    :param dest_folder: The ID of the parent folder
    :param file_names: The names of the files
    :param path: The path where the folders are
    :return: the link to the folder
    """
    creds = check_creds()
    service = build('drive', 'v3', credentials=creds)
    print("Uploading...")

    paths = []
    for name in file_names:
        paths.append(path + '\\' + name)

    folder_id, folder_link = new_folder(service, dest_folder, folder_name)
    upload_files(service, folder_id, paths)
    return folder_link


def update_list(lists):
    creds = check_creds()

    service = build('drive', 'v3', credentials=creds)

    for info in lists:
        if info["Link to folder"] is not None:
            folder_id = info["Link to folder"].split("/")[-1]

            response = service.files().list(q="'{}' in parents and trashed=false".format(folder_id),
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)').execute()
            for file in response.get('files', []):
                file_id = file.get('id')
                request = service.files().get_media(fileId=file_id)
                fh = io.FileIO(folder_id + file_id + ".pdf", 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))
