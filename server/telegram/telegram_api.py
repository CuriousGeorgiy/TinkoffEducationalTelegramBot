import telegram.ext

from server.telegram.callbacks import command_callbacks, message_callbacks, push_callbacks

import util.exception

import datetime


class TelegramAPI:

    def __init__(self, faq_list, pushes_list, token):
        self._updater = telegram.ext.Updater(token=token, use_context=True)
        self._faq_list = faq_list
        self._pushes_list = pushes_list

        self._updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', command_callbacks.start))
        self._updater.dispatcher.add_handler(
            telegram.ext.MessageHandler(telegram.ext.Filters.command, command_callbacks.unknown))

        self._add_faq_handlers()

        self._create_data_lists_update_job()
        self._create_push_jobs()

        self._updater.dispatcher.add_error_handler(util.exception.telegram_bot_update_error)

    def invoke(self):
        self._updater.start_polling()
        self._updater.idle()

    def _add_faq_handlers(self):
        self._faq_handlers = []
        for question, answer in self._faq_list:
            self._faq_handlers.append(telegram.ext.MessageHandler(telegram.ext.Filters.regex(question),
                                                                  message_callbacks.
                                                                  create_callback_from_answer(answer)))
            self._updater.dispatcher.add_handler(self._faq_handlers[-1])

    def _remove_all_faq_handlers(self):
        while self._faq_handlers:
            self._updater.dispatcher.remove_handler(self._faq_handlers.pop())

    def _create_data_lists_update_job(self):
        def data_lists_update_callback(context):
            from server.telegram.util.telegram_util import TelegramUtil

            TelegramUtil.update_telegram_api_data_lists()

        self._updater.job_queue.run_daily(data_lists_update_callback, datetime.time(20, 11, 50))

    def _create_push_jobs(self):
        self._push_jobs = []
        for text, groups, send_time in self._pushes_list:
            self._push_jobs.append(self._updater.job_queue.run_once(push_callbacks.
                                                                    create_callback_from_answer(text), send_time))

    def _remove_all_push_jobs(self):
        while self._push_jobs:
            self._push_jobs.pop().schedule_removal()

    def update_data_lists(self, faq_list, pushes_list):
        self._faq_list = faq_list
        self._update_faq_handlers()

        self._pushes_list = pushes_list
        self._update_push_jobs()

    def _update_faq_handlers(self):
        self._remove_all_faq_handlers()

        self._add_faq_handlers()

    def _update_push_jobs(self):
        self._remove_all_push_jobs()
        self._create_push_jobs()
