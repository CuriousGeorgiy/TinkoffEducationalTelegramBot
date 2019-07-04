import telegram.ext

import logging

import command_handlers
import exception
import message_handlers


class TelegramBot:

    def __init__(self, token):
        self.updater = telegram.ext.Updater(token=token, use_context=True)

        self.updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', command_handlers.start))
        self.updater.dispatcher.add_handler(
            telegram.ext.MessageHandler(telegram.ext.Filters.command, command_handlers.unknown))

        self.updater.dispatcher.add_handler(
            telegram.ext.MessageHandler(telegram.ext.Filters.text, message_handlers.idunno))

        self.updater.dispatcher.add_error_handler(exception.telegram_bot_update_error)

    def invoke(self):
        logging.getLogger("main." + __name__).warning('hahaha')
        self.updater.start_polling()
        self.updater.idle()
