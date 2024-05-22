from google.oauth2 import id_token
from google.auth.transport import requests

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImEzYjc2MmY4NzFjZGIzYmFlMDA0NGM2NDk2MjJmYzEzOTZlZGEzZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI3MzY0MjA3MDQxMzEtdW5uMms5YnFldjUwMGU3ajQxMjI4bzc1Y2VqN2hxYzguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3MzY0MjA3MDQxMzEtOWM3bjFmNHA1YTNsMDR0Mm5xamswOHVrMGp0NTB0bDAuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTc2NzA5NzQzNDk5MDgzMjE0ODIiLCJlbWFpbCI6InJpc2h1c2g4MDRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5vbmNlIjoiNmMwNjRjODk3NTg1M2M2ZTE4YWMzM2ZmYjI5MWI1YjFhYmM1YzNlNmQ3ZjVjN2JiMzc4YWRmODBhZWQ4MjViMyIsIm5hbWUiOiJSaXNodSBTaGFybWEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTFFUTUIyMnhrYnFST0RHU3FhcUZNX3RBVmdKMHVLQm1lbWRqTlRhS3RoVEJ3VV9iNkQ9czk2LWMiLCJnaXZlbl9uYW1lIjoiUmlzaHUiLCJmYW1pbHlfbmFtZSI6IlNoYXJtYSIsImlhdCI6MTcxNTMxMTYyMCwiZXhwIjoxNzE1MzE1MjIwfQ.btY7uHiQJo3ZjA2LYT6OoJy5TGhw4dHQ931o8K1Sr5HifhaGkjiPe2z469wJwsPbp9Pn2zHMnh9uIk_rwcCNoi_0C8jMPhX8lGPt66YkTbzcH03CUqQGFRSeYpGvmr2ggrE2fpq0NTindCItIvRphgqTeZCLpLDlyXKv9gOlVE97PngHJ08Wn0JkD_cWAHnyziKuyeWpowrDVJisUctjCE8NUndif6zpmN6t_7OsbSFmdVZkGy8l9jfDBPBxWI2NHPlh0j6shMvRpK3iwUSsCaY2WLbYxJ2rnKF9zYqACkR4QVhlqAQUk4gKp7239mAC9bt_mnYYeVIwnLKYgB6XpQ"
CLIENT_ID = "736420704131-9c7n1f4p5a3l04t2nqjk08uk0jt50tl0.apps.googleusercontent.com"

def x1():
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        print(idinfo)
        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If the request specified a Google Workspace domain
        # if idinfo['hd'] != DOMAIN_NAME:
        #     raise ValueError('Wrong domain name.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
    except ValueError:
        # Invalid token
        pass

def x2():
    from googleapiclient.discovery import build

    # Replace with your actual credentials
    credentials = # Your OAuth 2.0 credentials

    # Define the service object for Drive API
    service = build('drive', 'v3', credentials=credentials)

    # Get all files (including trashed)
    # files = service.files().list().execute()  # Uncomment for all files

    # Get files within a specific folder (replace 'folder_id' with your folder ID)
    folder_id = 'folder_id'
    files = service.files().list(
                pageSize=10,
                fields="nextPageToken, files(id, name, mimeType)"
                ).execute()

    print(files)
    # Remember to handle pagination for large datasets



if __name__=="__main__":
    x1()