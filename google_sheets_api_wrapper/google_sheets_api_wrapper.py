from datetime import datetime
from os.path import exists
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class GoogleSheetsAPIWrapper:

    def __init__(self, config: dict):
        self._config = config
        credentials = None

        if exists(config['token_path']):
            with open(config['token_path'], 'rb') as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(config['credentials_path'],
                                                                 config['scopes'])
                credentials = flow.run_local_server()

            with open(config['token_path'], 'wb') as token:
                pickle.dump(credentials, token)
                
        self._service = build('sheets', 'v4', credentials=credentials)

    def _get_values(self, range):
        try:
            return self._service.spreadsheets().values().get(spreadsheetId=self._config['database_spreadsheet_id'],
                                                             range=range).execute().get('values', [])
        except:
            pass

    def _append_values(self, range, insert_values):
        return self._service.spreadsheets().values().append(spreadsheetId=self._config['database_spreadsheet_id'],
                                                            range=range, valueInputOption='USER_ENTERED',
                                                            body={'values': [insert_values]}).execute()

    def append_values_to_people_sheet(self, insert_values: list):
        self._append_values(GoogleSheetsAPIWrapper._range_from_sheet_name_a1_notation(
            self._config['people_sheet_name'], self._config['people_sheet_range']), insert_values)

    """ Extract methods """

    def _extract_people_sheet(self):
        return self._get_values(GoogleSheetsAPIWrapper._range_from_sheet_name_a1_notation(
            self._config['people_sheet_name'], self._config['people_sheet_range']))

    def _extract_push_notifications_sheet(self):
        def convert_sheet(row):
            row[2] = datetime.strptime(row[2], '%d.%m.%Y %H:%M')

            """ datetime.datetime.today() is UTC+0, Moscow's timezone is UTC+3 """
            time_offset = 3 * 3600
            row[2] = datetime.fromtimestamp(row[2].timestamp() - time_offset)

            return row

        return list(map(convert_sheet,
                        self._get_values(GoogleSheetsAPIWrapper._range_from_sheet_name_a1_notation(
                            self._config['push_notifications_sheet_name'],
                            self._config['push_notifications_sheet_range']))))

    def _extract_faq_sheet(self):
        return self._get_values(GoogleSheetsAPIWrapper._range_from_sheet_name_a1_notation(
            self._config['faq_sheet_name'], self._config['faq_sheet_range']))

    def _extract_classes_schedule_sheet(self):
        def convert_sheet(row):
            row[2] = datetime.strptime(row[2], '%d.%m.%Y %H:%M')
            row[1] = row[1].lower()

            return row

        return list(map(convert_sheet,
                        self._get_values(GoogleSheetsAPIWrapper._range_from_sheet_name_a1_notation(
                            self._config['classes_schedule_sheet_name'],
                            self._config['classes_schedule_sheet_range']))))

    def extract_all_sheets(self) -> dict:
        return {'people_sheet': self._extract_people_sheet(),
                'push_notifications_sheet': self._extract_push_notifications_sheet(),
                'faq_sheet': self._extract_faq_sheet(),
                'classes_schedule_sheet': self._extract_classes_schedule_sheet()}

    """ Static methods """

    @staticmethod
    def _range_from_sheet_name_a1_notation(sheet_name, a1_notation):
        return "'" + sheet_name + "'" + '!' + a1_notation
