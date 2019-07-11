from server.telegram.telegram_api import TelegramAPI

import schedule

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
    def _update_telegram_api_google_sheets():
        faq_list, pushes_list = TelegramUtil._extract_google_sheets()

        TelegramUtil._telegram_api.update_faq_sheet(faq_list)
        TelegramUtil._telegram_api.update_pushes_sheet(pushes_list)

    schedule.every().day.at('00:00').do(_update_telegram_api_google_sheets)



