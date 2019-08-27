from argparse import ArgumentParser
import logging.config
from os.path import exists

from google_sheets_api_wrapper.google_sheets_api_wrapper import GoogleSheetsAPIWrapper
from telegram_api_wrapper.telegram_api_wrapper import TelegramAPIWrapper
from util.api_wrappers_util import APIWrappersUtil
from util import file_processing


def create_argument_parser():
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--proxy', dest='proxy', action='store_true', help='use proxy for the telegram api')
    argument_parser.add_argument('--no-user-data-json', dest='use_user_data_json', action='store_false',
                                 help='by setting this option you won\'t use the existing user data json and will'
                                      ' overwrite it')
    argument_parser.set_defaults(proxy=False, use_user_data_json=True)

    return argument_parser


def main(proxy, use_user_data_json):
    google_sheets_api_wrapper_config = file_processing.load_json_from_file('google_sheets_api_wrapper/misc/config.json')
    logging.config.dictConfig(file_processing.load_json_from_file('logging/config.json'))
    telegram_api_wrapper_config = file_processing.load_json_from_file('telegram_api_wrapper/misc/config.json')

    google_sheets_api_wrapper = GoogleSheetsAPIWrapper(google_sheets_api_wrapper_config)

    if not exists('telegram_api_wrapper/misc/user_data.json'):
        with open('telegram_api_wrapper/misc/user_data.json', 'w') as file:
            file.write('{}')

    telegram_api_wrapper = TelegramAPIWrapper(**google_sheets_api_wrapper.extract_all_sheets(),
                                              config=telegram_api_wrapper_config,
                                              user_data_json_path='telegram_api_wrapper/misc/user_data.json',
                                              use_user_data_json=use_user_data_json, use_proxy=proxy)

    APIWrappersUtil.attach_telegram_api_wrapper(telegram_api_wrapper)
    APIWrappersUtil.attach_google_sheets_api_wrapper(google_sheets_api_wrapper)

    telegram_api_wrapper.invoke()


if __name__ == "__main__":
    main(**create_argument_parser().parse_args().__dict__)
