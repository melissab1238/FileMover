import os
import io
import pickle
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# Import google.auth for loading credentials from the environment
import google.auth


import os


def download_file(service, file_id, destination_folder):
    """
    Downloads a file from Google Drive to a local destination.
    Handles Google Docs files by exporting them to a downloadable format.

    Args:
    - service: The authenticated Google Drive API service object.
    - file_id: The ID of the file to download.
    - destination_folder: The local path where the file should be saved.
    """
    try:
        # Get the file's metadata
        file_metadata = (
            service.files().get(fileId=file_id, fields="mimeType,name").execute()
        )

        # Determine the destination filename
        filename = file_metadata.get("name")
        if file_metadata["mimeType"].startswith("application/vnd.google-apps"):
            # Append.pdf to the filename for Google Docs files
            filename += ".pdf"

        # Construct the full destination path
        destination = os.path.join(destination_folder, filename)

        # Ensure the directory exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Check if the file is a Google Docs file
        if file_metadata["mimeType"].startswith("application/vnd.google-apps"):
            # Export the file to a PDF (you can change the mimeType to another format if needed)
            request = service.files().export_media(
                fileId=file_id, mimeType="application/pdf"
            )
        else:
            # Direct download for non-Google Docs files
            request = service.files().get_media(fileId=file_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
            print("Done.")

        # Write the file to disk
        with open(destination, "wb") as f:
            f.write(fh.getvalue())

    except Exception as error:
        print(f"An error occurred: {error}")
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    # # Load pre-authorized user credentials from the environment
    # creds, _ = google.auth.default()

    # Load credentials from a JSON key file
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", ["https://www.googleapis.com/auth/drive"]
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    # Create drive api client
    service = build("drive", "v3", credentials=creds)

    # Specify the folder ID
    folder_id = input("Please enter the ID of the Google Drive folder: ")

    # List files in the specified folder
    results = (
        service.files()
        .list(
            q=f"'{folder_id}' in parents",
            pageSize=10,
            fields="nextPageToken, files(id, name)",
        )
        .execute()
    )
    items = results.get("files", [])

    if not items:
        print("No files found in the specified folder.")
    else:
        print("Files in the specified folder:")
        for item in items:
            print(f"{item['name']} ({item['id']})")

            # Specify the destination path for the downloaded file
            destination_folder = input("Destination path for the downloaded file(s): ")

            download_file(service, item["id"], destination_folder)
