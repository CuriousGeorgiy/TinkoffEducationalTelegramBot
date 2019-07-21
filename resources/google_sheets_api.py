from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import os.path
import pickle

import datetime


class GoogleSheetsAPI:

    def __init__(self, ids):
        self._SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self._ids = ids

        self._authorization()

        self._service = build('sheets', 'v4', credentials=self._credentials)

    def _authorization(self):
        self._credentials = None

        if os.path.exists('misc/google_sheets_api_token.pickle'):
            with open('misc/google_sheets_api_token.pickle', 'rb') as token:
                self._credentials = pickle.load(token)

        if not self._credentials or not self._credentials.valid:
            if self._credentials and self._credentials.expired and self._credentials.refresh_token:
                self._credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('misc/google_sheets_api_credentials.json',
                                                                 self._SCOPES)
                self._credentials = flow.run_local_server()

            with open('misc/google_sheets_api_token.pickle', 'wb') as token:
                pickle.dump(self._credentials, token)

    def _get_values(self, range):
        return self._service.spreadsheets().values().get(spreadsheetId=self._ids['DATABASE_SPREADSHEET'],
                                                         range=range).execute().get('values', [])

    @staticmethod
    def _range_from_sheet_name_a1_notation(sheet_name, a1_notation):
        return "'" + sheet_name + "'" + '!' + a1_notation

    def _extract_people_sheet(self):
        return self._get_values(GoogleSheetsAPI._range_from_sheet_name_a1_notation(self._ids['PEOPLE_SHEET'], 'A1:ZZZ'))

    def _extract_push_notifications_sheet(self):
        def convert_table_date_time(row):
            row[2] = datetime.datetime.strptime(row[2], '%d.%m.%Y %H:%M')

            return row

        return list(map(convert_table_date_time, self._get_values(GoogleSheetsAPI._range_from_sheet_name_a1_notation(
            self._ids['PUSH_NOTIFICATIONS_SHEET'], 'A2:C'))))

    def _extract_faq_sheet(self):
        return self._get_values(GoogleSheetsAPI._range_from_sheet_name_a1_notation(self._ids['FAQ_SHEET'], 'A2:B'))

    def extract_all_sheets(self):
        return self._extract_people_sheet(), self._extract_push_notifications_sheet(), self._extract_faq_sheet()
