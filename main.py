from server.telegram.telegram_api import TelegramAPI
from server.telegram.telegram_util import TelegramUtil

import logging.config

import util.file_processing

import resources.google_sheets_api

import os.path


def main():
    google_sheets_ids = util.file_processing.load_json_from_file('misc/google_sheets_ids.json')
    logging.config.dictConfig(util.file_processing.load_json_from_file('misc/logging_config.json'))
    telegram_api_config = util.file_processing.load_json_from_file('misc/telegram_api_config.json')

    google_sheets_api = resources.google_sheets_api.GoogleSheetsAPI(google_sheets_ids)

    if os.path.exists('misc/telegram_api_user_data.json'):
        telegram_api = TelegramAPI(*google_sheets_api.extract_all_sheets(), telegram_api_config,
                                   'misc/telegram_api_user_data.json', False)
    else:
        open('misc/telegram_api_user_data.json', 'w').close()
        telegram_api = TelegramAPI(*google_sheets_api.extract_all_sheets(), telegram_api_config,
                                   'misc/telegram_api_user_data.json', True)

    TelegramUtil.attach_telegram_api(telegram_api)
    TelegramUtil.attach_google_sheets_api(google_sheets_api)

    telegram_api.invoke()


if __name__ == "__main__":
    main()
