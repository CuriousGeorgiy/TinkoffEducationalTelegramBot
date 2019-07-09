from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os.path
import pickle

import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def authorization():
    credentials = None

    if os.path.exists('misc/google_sheets_api_token.pickle'):
        with open('misc/google_sheets_api_token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'misc/google_sheets_api_credentials.json', SCOPES)
            credentials = flow.run_local_server()

        with open('misc/google_sheets_api_token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return credentials


def parse_date_time(date_time):
    date, time = date_time.split()

    return datetime.datetime(*list(map(int, date.split('.')))[::-1], *list(map(int, time.split(':'))))


def get_values(service, table_id, range):
    return service.spreadsheets().values().get(spreadsheetId=table_id, range=range).execute().get('values', [])


def extract_faq_table(service, faq_table_id):
    return get_values(service, faq_table_id, 'A2:B')


def extract_pushes_table(service, faq_table_id):
    def convert_table_date_time(row):
        row[2] = parse_date_time(row[2])

        return row

    return list(map(convert_table_date_time, get_values(service, faq_table_id, 'A2:C')))
