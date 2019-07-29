from google_sheets.google_sheets_api import GoogleSheetsAPI
from telegram_.telegram_api import TelegramAPI


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

    @staticmethod
    def append_person_to_people_sheet(phone_number, name):
        assert APIsUtil._google_sheets_api

        groups = ['0', '1']
        groups.extend(['0'] * (APIsUtil._telegram_api.get_number_of_groups() - 1))

        APIsUtil._google_sheets_api.append_values_to_people_sheet([phone_number, name, *groups])

    """ Get methods """

    @staticmethod
    def get_telegram_api_mapping_for_people_sheet():
        assert APIsUtil._telegram_api

        return APIsUtil._telegram_api.get_mapping_for_people_sheet()

    @staticmethod
    def get_telegram_api_classes_schedule_sheet():
        assert APIsUtil._telegram_api

        return APIsUtil._telegram_api.get_classes_schedule_sheet()
