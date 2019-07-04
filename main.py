from telegram_bot import TelegramBot

import logging.config

import file_processing


def main():
    logging.config.dictConfig(file_processing.load_json_from_file("logging_config.json"))
    credentials = file_processing.load_json_from_file("credentials.json")

    bot = TelegramBot(credentials["telegram_bot_token"])
    bot.invoke()


if __name__ == "__main__":
    main()
