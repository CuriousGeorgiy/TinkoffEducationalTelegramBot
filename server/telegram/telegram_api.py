import telegram.ext

import server.telegram.command_callbacks
import server.telegram.message_callbacks
import server.telegram.push_callbacks

import util.exception


class TelegramAPI:

    def __init__(self, faq_list, pushes_list, token):
        self._updater = telegram.ext.Updater(token=token, use_context=True)
        self._faq_list = faq_list
        self._pushes_list = pushes_list

        self._updater.dispatcher.add_handler(telegram.ext.CommandHandler('start',
                                                                         server.telegram.command_callbacks.start))
        self._updater.dispatcher.add_handler(
            telegram.ext.MessageHandler(telegram.ext.Filters.command, server.telegram.command_callbacks.unknown))

        self._add_faq_handlers()
        self._create_push_jobs()

        self._updater.dispatcher.add_error_handler(util.exception.telegram_bot_update_error)

    def invoke(self):
        self._updater.start_polling()
        self._updater.idle()

    def _add_faq_handlers(self):
        for question, answer in self._faq_list:
            self._updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.regex(question),
                                                                             server.telegram.message_callbacks.
                                                                             create_callback_from_answer(answer)))

    def _create_push_jobs(self):
        for text, groups, send_time in self._pushes_list:
            self._updater.job_queue.run_once(server.telegram.push_callbacks.create_callback_from_answer(text),
                                             send_time)
