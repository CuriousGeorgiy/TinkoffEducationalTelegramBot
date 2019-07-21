import telegram.ext

from server.telegram.callbacks import command_callbacks, message_callbacks, job_callbacks
from server.telegram import filters
import server.telegram.exception

import util.file_processing

import datetime


class TelegramAPI:

    def __init__(self, people_list, push_notifications_list, faq_list, config, user_data_json_path,
                 user_data_json_empty):
        self._persistence_path = user_data_json_path
        self._persistence = telegram.ext.DictPersistence(store_chat_data=True) if user_data_json_empty \
            else telegram.ext.DictPersistence(store_chat_data=True,
                                              user_data_json=util.file_processing.load_json_string_from_file(
                                                  self._persistence_path))
        self._updater = telegram.ext.Updater(token=config['bot_token'], use_context=True,
                                             request_kwargs={'proxy_url': config['proxy_url']}, persistence=
                                             self._persistence)
        self._create_mappings_from_people_list(people_list)
        self._push_notifications_list = push_notifications_list
        self._faq_list = faq_list

        self._updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', command_callbacks.start))
        self._updater.dispatcher.add_handler(telegram.ext.CommandHandler('authorization',
                                                                         command_callbacks.authorization))
        self._updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.command,
                                                                         command_callbacks.unknown))

        self._updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.contact,
                                                                         message_callbacks.authorization))

        self._create_update_data_job()
        self._create_push_notification_jobs()

        self._add_faq_handlers()
        self._updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text,
                                                                         message_callbacks.unknown))

        self._updater.dispatcher.add_error_handler(server.telegram.exception.telegram_bot_update_error)

    def invoke(self):
        self._updater.start_polling()
        self._updater.idle()

    def dump_persistence_obj(self):
        util.file_processing.dump_json_string_to_file(self._persistence.user_data_json, self._persistence_path)

    def _create_update_data_job(self):
        # TODO: lock application while updating data lists

        self._updater.job_queue.run_repeating(job_callbacks.update_data, datetime.timedelta(minutes=5))

    def _create_mappings_from_people_list(self, people_list):
        self._phone_number_to_id = {}
        self._id_to_person_info = {}

        for i in range(1, len(people_list)):
            self._phone_number_to_id[people_list[i][0]] = i
            self._id_to_person_info[i] = {'name': people_list[i][1], 'groups': set()}
            for j in range(2, len(people_list[0])):
                if int(people_list[i][j]):
                    self._id_to_person_info[i]['groups'].add(people_list[0][j])

        for telegram_id, user_data in self._updater.dispatcher.user_data.items():
            if user_data['authorized']:
                self._id_to_person_info[user_data['id_in_telegram_api']]['telegram_id'] = telegram_id

    def set_person_telegram_id(self, person_id, telegram_id):
        self._id_to_person_info[person_id]['telegram_id'] = telegram_id

    def _delete_mappings_for_people_list(self):
        self._phone_number_to_id.clear()
        self._id_to_person_info.clear()

    def _update_mappings_for_people_list(self, people_list):
        self._delete_mappings_for_people_list()
        self._create_mappings_from_people_list(people_list)

    def get_mappings_for_people_list(self):
        return self._phone_number_to_id, self._id_to_person_info

    def _create_push_notification_jobs(self):
        self._push_notification_jobs = []
        for text, groups, send_time in self._push_notifications_list:
            groups = set(groups.split(','))
            self._push_notification_jobs.append(self._updater.job_queue.run_once(
                job_callbacks.create_push_notification_callback_from_push_text(text), send_time,
                context=(self._id_to_person_info, groups)))

    def _remove_all_push_notificaiton_jobs(self):
        while self._push_notification_jobs:
            self._push_notification_jobs.pop().schedule_removal()

    def _update_push_notification_jobs(self):
        self._remove_all_push_notificaiton_jobs()
        self._create_push_notification_jobs()

    def _add_faq_handlers(self):
        self._faq_handlers = []
        for question, answer in self._faq_list:
            self._faq_handlers.append(telegram.ext.MessageHandler(filters.PrepareMessageTextForRegexFilter(question),
                                                                  message_callbacks.create_callback_from_answer(
                                                                      answer)))
            self._updater.dispatcher.add_handler(self._faq_handlers[-1])

    def _remove_all_faq_handlers(self):
        while self._faq_handlers:
            self._updater.dispatcher.remove_handler(self._faq_handlers.pop())

    def _update_faq_handlers(self):
        self._remove_all_faq_handlers()

        self._add_faq_handlers()

    def update_data_lists(self, people_list, push_notifications_list, faq_list):
        self._update_mappings_for_people_list(people_list)

        self._push_notifications_list = push_notifications_list
        self._update_push_notification_jobs()

        self._faq_list = faq_list
        self._update_faq_handlers()
