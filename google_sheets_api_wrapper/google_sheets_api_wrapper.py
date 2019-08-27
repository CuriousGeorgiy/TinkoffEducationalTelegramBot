from datetime import datetime
import os.path
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class GoogleSheetsAPIWrapper:

    def __init__(self, config):
        self._SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self._config = config

        self._authorization()

        self._service = build('sheets', 'v4', credentials=self._credentials)

    def _authorization(self):
        self._credentials = None

        if os.path.exists('google_sheets_api_wrapper/misc/token.pickle'):
            with open('google_sheets_api_wrapper/misc/token.pickle', 'rb') as token:
                self._credentials = pickle.load(token)

        if not self._credentials or not self._credentials.valid:
            if self._credentials and self._credentials.expired and self._credentials.refresh_token:
                self._credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('google_sheets_api_wrapper/misc/credentials.json',
                                                                 self._SCOPES)
                self._credentials = flow.run_local_server()

            with open('google_sheets_api_wrapper/misc/token.pickle', 'wb') as token:
                pickle.dump(self._credentials, token)

    def _get_values(self, range):
        return self._service.spreadsheets().values().get(spreadsheetId=self._config['DATABASE_SPREADSHEET_ID'],
                                                         range=range).execute().get('values', [])

    def _append_values(self, range, insert_values):
        return self._service.spreadsheets().values().append(spreadsheetId=self._config['DATABASE_SPREADSHEET_ID'],
                                                            range=range, valueInputOption='USER_ENTERED',
                                                            body={'values': [insert_values]}).execute()

    def append_values_to_people_sheet(self, insert_values: list):
        self._append_values(GoogleSheetsAPIWrapper._range_from_sheet_name_a1_notation(
            self._config['PEOPLE_SHEET_NAME'], self._config['PEOPLE_SHEET_RANGE']), insert_values)

    """ Extract methods """

    def _extract_people_sheet(self):
        return self._get_values(GoogleSheetsAPIWrapper._range_from_sheet_name_a1_notation(
            self._config['PEOPLE_SHEET_NAME'], self._config['PEOPLE_SHEET_RANGE']))

    def _extract_push_notifications_sheet(self):
        def convert_sheet(row):
            row[2] = datetime.strptime(row[2], '%d.%m.%Y %H:%M')

            """ datetime.datetime.today() is UTC+0, Moscow's timezone is UTC+3 """
            time_offset = 3 * 3600
            row[2] = datetime.fromtimestamp(row[2].timestamp() - time_offset)

            return row

        return list(map(convert_sheet,
                        self._get_values(GoogleSheetsAPIWrapper._range_from_sheet_name_a1_notation(
                            self._config['PUSH_NOTIFICATIONS_SHEET_NAME'],
                            self._config['PUSH_NOTIFICATIONS_SHEET_RANGE']))))

    def _extract_faq_sheet(self):
        return self._get_values(GoogleSheetsAPIWrapper._range_from_sheet_name_a1_notation(
            self._config['FAQ_SHEET_NAME'], self._config['FAQ_SHEET_RANGE']))

    def _extract_classes_schedule_sheet(self):
        def convert_sheet(row):
            row[2] = datetime.strptime(row[2], '%d.%m.%Y %H:%M')
            row[1] = row[1].lower()

            return row

        return list(map(convert_sheet,
                        self._get_values(GoogleSheetsAPIWrapper._range_from_sheet_name_a1_notation(
                            self._config['CLASSES_SCHEDULE_SHEET_NAME'],
                            self._config['CLASSES_SCHEDULE_SHEET_RANGE']))))

    def extract_all_sheets(self):
        return {'people_sheet': self._extract_people_sheet(),
                'push_notifications_sheet': self._extract_push_notifications_sheet(),
                'faq_sheet': self._extract_faq_sheet(),
                'classes_schedule_sheet': self._extract_classes_schedule_sheet()}

    """ Static methods """

    @staticmethod
    def _range_from_sheet_name_a1_notation(sheet_name, a1_notation):
        return "'" + sheet_name + "'" + '!' + a1_notation
