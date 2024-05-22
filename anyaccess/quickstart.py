import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


import io

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
    ]

def get_or_make_creds():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(   
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

def make_search(mimeType:str, searchStr:str = ""):
    # get_or_make_creds()
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
                            q=f"name='{searchStr}' and mimeType='{mimeType}'",
                            spaces='drive'
                        ).execute()
        
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return None
        
        for ind,item in enumerate(items):
            print(f"{ind} : {item['name']} ({item['id']}) {item['mimeType']}")
            if item['name']==searchStr:
                return item["id"]
        
        return None

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")

def check_folder(folder_name:str = "Anyaccess Files"):
    return make_search("application/vnd.google-apps.folder", folder_name)

def get_file_list():
    # get_or_make_creds()
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    try:
        service = build("drive", "v3", credentials=creds)
        parfolder_id = check_folder()
        if parfolder_id is None:
            print("No folder found")
            raise FileNotFoundError("Folder Anyaccess Files not found on your drive")
        # Call the Drive v3 API
        print("parfolder_id",parfolder_id)
        results = (
            service.files()
            .list(
                pageSize=10,
                fields="nextPageToken, files(id, name, mimeType)",
                q = f"'{parfolder_id}' in parents",
                )
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return
        
        for ind,item in enumerate(items):
            print(f"{ind} : {item['name']} ({item['id']}) {item['mimeType']}")

        # file_id = items[int(input())]["id"]
        # print("-------------------------")
        # print(file_id)
        # request = service.files().get_media(fileId=file_id)
        # file = io.BytesIO()
        # downloader = MediaIoBaseDownload(file, request)
        # done = False
        # while done is False:
        #     status, done = downloader.next_chunk()
        #     print(f"Download {int(status.progress() * 100)}.")
        
        # with open("output", "wb") as f:
        #     f.write(file.getbuffer())

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")
    
def create_folder():
    get_or_make_creds()
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    try:
        service = build("drive", "v3", credentials=creds)
        file_metadata = {
            "name": "Anyaccess Files",
            "mimeType": "application/vnd.google-apps.folder",
        }

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields="id").execute()
        print(f'Folder ID: "{file.get("id")}".')
        return file.get("id")
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

if __name__ == "__main__":
    pass
    create_folder()
    get_file_list()