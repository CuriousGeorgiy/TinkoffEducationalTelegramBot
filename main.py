import argparse
import logging.config
import os.path

from server.telegram.telegram_api import TelegramAPI
from util.apis_util import APIsUtil
import util.file_processing
import resources.google_sheets_api


def create_argument_parser():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--proxy', dest='proxy', action='store_true', help='use proxy for the telegram api')
    argument_parser.add_argument('--no-user-data-json', dest='use_user_data_json', action='store_false',
                                 help='by setting this option you won\'t use the existing user data json and will'
                                      'overwrite it')
    argument_parser.set_defaults(proxy=False, use_user_data_json=True)

    return argument_parser


def main(proxy, use_user_data_json):
    google_sheets_ids = util.file_processing.load_json_from_file('misc/google_sheets_ids.json')
    logging.config.dictConfig(util.file_processing.load_json_from_file('misc/logging_config.json'))
    telegram_api_config = util.file_processing.load_json_from_file('misc/telegram_api_config.json')

    google_sheets_api = resources.google_sheets_api.GoogleSheetsAPI(google_sheets_ids)

    if not os.path.exists('misc/telegram_api_user_data.json'):
        with open('misc/telegram_api_user_data.json', 'w') as file:
            file.write('{}')

    if use_user_data_json:
        telegram_api = TelegramAPI(**google_sheets_api.extract_all_sheets(), config=telegram_api_config,
                                   user_data_json_path='misc/telegram_api_user_data.json',
                                   use_user_data_json=True, use_proxy=True) if proxy \
            else TelegramAPI(**google_sheets_api.extract_all_sheets(), config=telegram_api_config,
                             user_data_json_path='misc/telegram_api_user_data.json')
    else:
        telegram_api = TelegramAPI(**google_sheets_api.extract_all_sheets(), config=telegram_api_config,
                                   user_data_json_path='misc/telegram_api_user_data.json',
                                   use_user_data_json=False, use_proxy=True) if proxy \
            else TelegramAPI(**google_sheets_api.extract_all_sheets(), config=telegram_api_config,
                             user_data_json_path='misc/telegram_api_user_data.json', use_user_data_json=False)

    APIsUtil.attach_telegram_api(telegram_api)
    APIsUtil.attach_google_sheets_api(google_sheets_api)
    telegram_api.invoke()


if __name__ == "__main__":
    main(**create_argument_parser().parse_args().__dict__)
