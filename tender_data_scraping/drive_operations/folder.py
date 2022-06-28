from __future__ import print_function
import pickle
import os.path
import glob
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload
import io
from dotenv import load_dotenv

from file_operations import handle_files
from . import check_creds

load_dotenv()
PATH = os.environ.get("TEMP_FOLDER")


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


def upload_to_drive(folder_name, dest_folder):
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
    file_formats = ["pdf", "doc", "docx", "xlsx"]
    for format in file_formats:
        files = handle_files.get_files(format)
        paths += files
    #files = glob.glob(PATH + "/*")
    #for f in files:
    #    paths.append(f)

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
