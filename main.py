from server.telegram.telegram_api import TelegramAPI

from server.telegram.util.telegram_util import TelegramUtil

import logging.config

import util.file_processing

import resources.google_sheets_api


def main():
    google_sheets_ids = util.file_processing.load_json_from_file('misc/google_sheets_ids.json')
    logging.config.dictConfig(util.file_processing.load_json_from_file('misc/logging_config.json'))
    authorization_tokens = util.file_processing.load_json_from_file('misc/authorization_tokens.json')

    google_sheets_api = resources.google_sheets_api.GoogleSheetsAPI(google_sheets_ids)

    telegram_api = TelegramAPI(*google_sheets_api.extract_all_sheets(), authorization_tokens['telegram_bot_token'])

    TelegramUtil.attach_telegram_api(telegram_api)
    TelegramUtil.attach_google_sheets_api(google_sheets_api)

    telegram_api.invoke()


if __name__ == "__main__":
    main()
