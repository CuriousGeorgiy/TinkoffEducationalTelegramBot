from server.telegram.telegram_api import TelegramAPI

from resources.google_sheets_api import GoogleSheetsAPI


class TelegramUtil:
    _telegram_api = None
    _google_sheets_api = None

    @staticmethod
    def attach_telegram_api(telegram_api: TelegramAPI):
        TelegramUtil._telegram_api = telegram_api

    @staticmethod
    def attach_google_sheets_api(google_sheets_api: GoogleSheetsAPI):
        TelegramUtil._google_sheets_api = google_sheets_api

    @staticmethod
    def _extract_google_sheets():
        return TelegramUtil._google_sheets_api.extract_all_sheets()

    @staticmethod
    def update_telegram_api_data_lists():
        if TelegramUtil._telegram_api and TelegramUtil._google_sheets_api:
            TelegramUtil._telegram_api.update_data_lists(*TelegramUtil._extract_google_sheets())
