from __future__ import print_function
from oauthCreds import get_google_creds
from read_google_sheet import get_email_list

import base64
import json
from email.message import EmailMessage

from googleapiclient.discovery import build 
from googleapiclient.errors import HttpError

config = None
creds = None 

def gmail_create_draft(name,email):
    """
        Create and insert a draft email. 
        Print the returned draft's message and id. 
        Returns: Draft object, including draft id and message meta data. 
    """
    
    try:
        # read in email 
        with open('email.txt', 'r') as file:
            email_content = file.read()
        email_content = email_content.replace("<<donorname>>", name)

        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()

        # email body
        message.set_content(email_content)


        message['To'] = email
        message['From'] = config['from_email']
        message['Subject'] = config['email_subject']

        # encode the message 
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_message = {
                'raw' : encoded_message
            }

        # pylint: disable=E1101
        sent_msg = service.users().messages().send(userId="me",
                                                body=send_message).execute()
        
        print(f'Email sent to {name} at {email}')

    except HttpError as error:
        print(f'An error occurred: {error}') 



def gmail_list_drafts():
    try:
        service = build('gmail', 'v1', credentials=creds)
        draft_list = service.users().drafts().list(userId="me").execute()
        print(draft_list)

    except HttpError as err:
        print(err)


# def gmail_get_draft():
#     try:
#         config = json.load(open('config.json'))
#         service = build('gmail', 'v1', credentials=creds)
#         draft = service.users().drafts().get(userId="me",
#                                              id=config["draft_id"],
#                                              format="raw").execute()
#         decoded_email = base64.urlsafe_b64decode(draft['message']['raw']).decode()
#         edited_email = decoded_email.replace("<<donorname>>", "Padma Jonnadula").replace("&lt;&lt;donorname&gt;&gt;", "Padma Jonnadula")
#         print(edited_email)
#         to_email = edited_email.replace("Sriya Vudata <svsriya@gmail.com>", "pjonnadula@gmail.com")
#         encoded_email = base64.urlsafe_b64encode(to_email.encode()).decode()
#         create_message = {
#             'message' : {
#                 'raw' : encoded_email
#             }
#         }

#         # pylint: disable=E1101
#         draft = service.users().drafts().create(userId="me",
#                                                 body=create_message).execute()
#         print(draft)


#     except HttpError as err:
#         print(err)


if __name__ == '__main__':
    config = json.load(open('config.json'))
    creds = get_google_creds()
    spreadsheet = get_email_list(creds)

    for row in spreadsheet:
        gmail_create_draft(row[0], row[1])
    