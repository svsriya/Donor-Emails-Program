from __future__ import print_function

from oauthCreds import get_google_creds
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
    """
    Shows basic usage of the Gmail API. 
    Lists the user's Gmail labels. 
    """
    
    creds = get_google_creds()

    try:
        # call the Gmail API 
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])
        
    except HttpError as error:
        # TODO - handle errors from gmail API 
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
    