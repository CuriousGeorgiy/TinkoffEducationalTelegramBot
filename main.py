from server.telegram.telegram_api import TelegramAPI

import logging.config

import util.file_processing

import resources.google_sheets_api

import schedule


def main():
    google_sheets_ids = util.file_processing.load_json_from_file('misc/google_sheets_ids.json')
    logging.config.dictConfig(util.file_processing.load_json_from_file('misc/logging_config.json'))
    authorization_tokens = util.file_processing.load_json_from_file('misc/authorization_tokens.json')

    google_sheets_api = resources.google_sheets_api.GoogleSheetsAPI(google_sheets_ids)

    telegram_api = TelegramAPI(google_sheets_api.extract_faq_table(), google_sheets_api.extract_pushes_table(),
                               authorization_tokens['telegram_bot_token'])
    telegram_api.invoke()

    schedule.run_pending()


if __name__ == "__main__":
    main()
