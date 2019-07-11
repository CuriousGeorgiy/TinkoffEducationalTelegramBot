import telegram.ext

from server.telegram import callbacks

import util.exception


class TelegramAPI:

    def __init__(self, faq_list, pushes_list, token):
        self._updater = telegram.ext.Updater(token=token, use_context=True)
        self._faq_list = faq_list
        self._pushes_list = pushes_list

        self._updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', callbacks.command_callbacks.start))
        self._updater.dispatcher.add_handler(
            telegram.ext.MessageHandler(telegram.ext.Filters.command, callbacks.command_callbacks.unknown))

        self._add_faq_handlers()
        self._create_push_jobs()

        self._updater.dispatcher.add_error_handler(util.exception.telegram_bot_update_error)

    def invoke(self):
        self._updater.start_polling()
        self._updater.idle()

    def _add_faq_handlers(self):
        for question, answer in self._faq_list:
            self._updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.regex(question),
                                                                             callbacks.message_callbacks.
                                                                             create_callback_from_answer(answer)))

    def _create_push_jobs(self):
        for text, groups, send_time in self._pushes_list:
            self._updater.job_queue.run_once(callbacks.push_callbacks.create_callback_from_answer(text), send_time)

    def update_faq_list(self, faq_list):
        self._faq_list = faq_list

    def update_pushes_list(self, pushes_list):
        self._pushes_list = pushes_list
