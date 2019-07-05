from telegram_interface import TelegramInterface

import logging.config

import file_processing


def main():
    logging.config.dictConfig(file_processing.load_json_from_file("logging_config.json"))
    credentials = file_processing.load_json_from_file("credentials.json")

    telegram_interface = TelegramInterface(credentials["telegram_bot_token"])
    telegram_interface.invoke()


if __name__ == "__main__":
    main()
