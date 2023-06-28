from __future__ import print_function

import base64
import os.path
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.readonly']


def get_google_creds():
    creds = None
    # the file token.json stores the user's access and refresh tokens, and is 
    # created automatically when the authorization flow completes for the first 
    # time. 
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in. 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run 
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def gmail_create_draft(creds):
    """
        Create and insert a draft email. 
        Print the returned draft's message and id. 
        Returns: Draft object, including draft id and message meta data. 
    """
    
    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()

        message.set_content('This is automated draft mail')

        message['To'] = ''
        message['From'] = ''
        message['Subject'] = 'Automated draft'

        # encode the message 
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'message' : {
                'raw' : encoded_message
            }
        }

        # pylint: disable=E1101
        draft = service.users().drafts().create(userId="me",
                                                body=create_message).execute()
        
        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

    except HttpError as error:
        print(f'An error occurred: {error}')
        draft = None 

    return draft


if __name__ == '__main__':
    creds = get_google_creds()
    gmail_create_draft(creds)