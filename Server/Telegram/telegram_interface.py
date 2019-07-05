import telegram.ext

import logging

import command_handlers
import exception
import message_handlers


class TelegramInterface:

    def __init__(self, token):
        self._updater = telegram.ext.Updater(token=token, use_context=True)

        self._updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', command_handlers.start))
        self._updater.dispatcher.add_handler(
            telegram.ext.MessageHandler(telegram.ext.Filters.command, command_handlers.unknown))

        self._updater.dispatcher.add_handler(
            telegram.ext.MessageHandler(telegram.ext.Filters.text, message_handlers.idunno))

        self._updater.dispatcher.add_error_handler(exception.telegram_bot_update_error)

    def invoke(self):
        self._updater.start_polling()
        self._updater.idle()
