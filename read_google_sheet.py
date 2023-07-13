from __future__ import print_function
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauthCreds import get_google_creds


def get_email_list(creds):
    data = json.load(open('config.json'))

    SHEET_ID = data["sheet_id"]
    RANGE_NAME = data["sheet_range"]

    try: 
        service = build('sheets', 'v4', credentials=creds)

        # Call the sheets api 
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        
        # print('Name, Email:')
        # for row in values: 
        #     # Print columns A and B
        #     print('%s, %s' % (row[0], row[1]))
        return values
    
    except HttpError as err: 
        print(err)

# if __name__ == '__main__':
#     creds = get_google_creds()
#     get_email_list(creds)