from google_sheets_api_wrapper.google_sheets_api_wrapper import GoogleSheetsAPIWrapper
from telegram_api_wrapper.telegram_api_wrapper import TelegramAPIWrapper


class APIWrappersUtil:
    _telegram_api_wrapper = None
    _google_sheets_api_wrapper = None

    @staticmethod
    def attach_telegram_api_wrapper(telegram_api_wrapper: TelegramAPIWrapper):
        APIWrappersUtil._telegram_api_wrapper = telegram_api_wrapper

    @staticmethod
    def attach_google_sheets_api_wrapper(google_sheets_api_wrapper: GoogleSheetsAPIWrapper):
        APIWrappersUtil._google_sheets_api_wrapper = google_sheets_api_wrapper

    @staticmethod
    def dump_telegram_api_wrapper_persistence_obj():
        assert APIWrappersUtil._telegram_api_wrapper

        APIWrappersUtil._telegram_api_wrapper.dump_persistence_obj()

    @staticmethod
    def update_telegram_api_wrapper_data_sheets():
        assert APIWrappersUtil._telegram_api_wrapper and APIWrappersUtil._google_sheets_api_wrapper

        APIWrappersUtil._telegram_api_wrapper.update_data_sheets(
            **APIWrappersUtil._google_sheets_api_wrapper.extract_all_sheets())

    @staticmethod
    def set_telegram_api_wrapper_person_telegram_id(person_id, telegram_id):
        assert APIWrappersUtil._telegram_api_wrapper

        APIWrappersUtil._telegram_api_wrapper.set_person_telegram_id(person_id, telegram_id)

    @staticmethod
    def append_person_to_people_sheet(phone_number, name):
        assert APIWrappersUtil._google_sheets_api_wrapper

        groups = ['0', '1']
        groups.extend(['0'] * (APIWrappersUtil._telegram_api_wrapper.get_number_of_groups() - 1))

        APIWrappersUtil._google_sheets_api_wrapper.append_values_to_people_sheet([phone_number, name, *groups])

    """ Get methods """

    @staticmethod
    def get_telegram_api_wrapper_mapping_for_people_sheet():
        assert APIWrappersUtil._telegram_api_wrapper

        return APIWrappersUtil._telegram_api_wrapper.get_mapping_for_people_sheet()

    @staticmethod
    def get_telegram_api_wrapper_classes_schedule_sheet():
        assert APIWrappersUtil._telegram_api_wrapper

        return APIWrappersUtil._telegram_api_wrapper.get_classes_schedule_sheet()
