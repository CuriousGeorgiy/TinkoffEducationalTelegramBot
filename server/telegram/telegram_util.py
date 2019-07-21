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
    def update_telegram_api_data():
        if TelegramUtil._telegram_api and TelegramUtil._google_sheets_api:
            TelegramUtil._telegram_api.update_data_lists(*TelegramUtil._google_sheets_api.extract_all_sheets())
            TelegramUtil._telegram_api.dump_persistence_obj()

    @staticmethod
    def get_telegram_api_mappings_for_people_list():
        return TelegramUtil._telegram_api.get_mappings_for_people_list()

    @staticmethod
    def set_telegram_api_person_telegram_id(person_id, telegram_id):
        TelegramUtil._telegram_api.set_person_telegram_id(person_id, telegram_id)
