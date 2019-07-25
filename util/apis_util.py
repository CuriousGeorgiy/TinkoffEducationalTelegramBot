from server.telegram.telegram_api import TelegramAPI
from resources.google_sheets_api import GoogleSheetsAPI


class APIsUtil:
    _telegram_api = None
    _google_sheets_api = None

    @staticmethod
    def attach_telegram_api(telegram_api: TelegramAPI):
        APIsUtil._telegram_api = telegram_api

    @staticmethod
    def attach_google_sheets_api(google_sheets_api: GoogleSheetsAPI):
        APIsUtil._google_sheets_api = google_sheets_api

    @staticmethod
    def dump_telegram_api_persistence_obj():
        assert APIsUtil._telegram_api

        APIsUtil._telegram_api.dump_persistence_obj()

    @staticmethod
    def update_telegram_api_data_sheets():
        assert APIsUtil._telegram_api and APIsUtil._google_sheets_api

        APIsUtil._telegram_api.update_data_sheets(**APIsUtil._google_sheets_api.extract_all_sheets())

    @staticmethod
    def set_telegram_api_person_telegram_id(person_id, telegram_id):
        assert APIsUtil._telegram_api

        APIsUtil._telegram_api.set_person_telegram_id(person_id, telegram_id)

    """ Get methods """

    @staticmethod
    def get_telegram_api_mapping_for_people_sheet():
        assert APIsUtil._telegram_api

        return APIsUtil._telegram_api.get_mapping_for_people_sheet()

    @staticmethod
    def get_telegram_api_classes_schedule_sheet():
        assert APIsUtil._telegram_api

        return APIsUtil._telegram_api.get_classes_schedule_sheet()
