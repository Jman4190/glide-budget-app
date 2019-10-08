# import modules
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
PLAID_ENV = os.getenv('PLAID_ENV')
BOFA_ACCESS_TOKEN=os.getenv('BOFA_ACCESS_TOKEN')
CHASE_ACCESS_TOKEN=os.getenv('CHASE_ACCESS_TOKEN')
SPREADSHEET_ID=os.getenv('SPREADSHEET_ID')

def get_google_sheet_id(sheet_name):
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    SCOPES = 'https://www.googleapis.com/auth/drive'
    # authenticate access
    store = oauth_file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    title = sheets[0].get("properties", {}).get("title", sheet_name)
    sheet_id = sheets[0].get("properties", {}).get("sheetId", 0)
    return sheet_id

def get_gsheet_length():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    gc = gspread.authorize(credentials)
    ws = gc.open("personal-finance-budgeting-app").worksheet("transactions")
    # Get all values from the first row
    length = len(ws.col_values(1))
    return length

#def insert2gsheet(data, spreadsheet_id, sheet_id, length):
def insert2gsheet(data, sheet_id, length):
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    SCOPES = 'https://www.googleapis.com/auth/drive'
    # authenticate access
    store = oauth_file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    # insert data into google sheet
    # may be too big...
    batch_update_spreadsheet_request_body = {
    "requests": [
        {
        "pasteData": {
            "coordinate": {
            "sheetId": sheet_id
            },
            "data": data.to_csv(index=False, header=None),
            "type": "PASTE_VALUES",
            "delimiter": ",",
            "coordinate": {
                "sheetId": sheet_id,
                "rowIndex": length,
                        }
                    }
        }
    ]
    }

    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=batch_update_spreadsheet_request_body)
    response = request.execute()
    return response

