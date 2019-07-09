from server.telegram.telegram_api import TelegramAPI

import googleapiclient.discovery

import logging.config

import util.file_processing

import resources.google_sheets_api


def main():
    google_sheets_service = googleapiclient.discovery.build('sheets', 'v4',
                                                            credentials=resources.google_sheets_api.authorization())

    table_ids = util.file_processing.load_json_from_file('misc/table_ids.json')
    logging.config.dictConfig(util.file_processing.load_json_from_file('misc/logging_config.json'))
    authorization_tokens = util.file_processing.load_json_from_file('misc/authorization_tokens.json')

    telegram_interface = TelegramAPI(resources.google_sheets_api.extract_faq_table(google_sheets_service,
                                                                                   table_ids['FAQ']),
                                     resources.google_sheets_api.extract_pushes_table(google_sheets_service,
                                                                                      table_ids['PUSHES']),
                                     authorization_tokens['telegram_bot_token'])
    telegram_interface.invoke()

    print(resources.google_sheets_api.extract_pushes_table(google_sheets_service, table_ids['PUSHES']))


if __name__ == "__main__":
    main()
