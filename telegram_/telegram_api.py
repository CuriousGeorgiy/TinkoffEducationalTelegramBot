import datetime

from telegram.ext import DictPersistence, Filters, ConversationHandler, CommandHandler, MessageHandler, Updater

from telegram_.callbacks import command_callbacks, message_callbacks, job_callbacks
from telegram_ import filters, exception
import util.file_processing


class TelegramAPI:

    def __init__(self, people_sheet, push_notifications_sheet, faq_sheet, classes_schedule_sheet, config,
                 user_data_json_path, use_user_data_json=True, use_proxy=False):
        self._persistence_path = user_data_json_path
        self._persistence = DictPersistence(store_chat_data=True,
                                            user_data_json=util.file_processing.load_json_string_from_file(
                                                             self._persistence_path)) if use_user_data_json \
            else DictPersistence(store_chat_data=True)
        self._updater = Updater(token=config['bot_token'], use_context=True,
                                request_kwargs={'proxy_url': config['proxy_url']}, persistence=self._persistence) \
            if use_proxy else Updater(token=config['bot_token'], use_context=True, persistence=self._persistence)

        self._dispatcher = self._updater.dispatcher

        self._create_mapping_from_people_sheet(people_sheet)
        self._push_notifications_sheet = push_notifications_sheet
        self._faq_sheet = faq_sheet
        self._classes_schedule_sheet = classes_schedule_sheet

        self._dispatcher.add_handler(CommandHandler('start', command_callbacks.start))
        self._dispatcher.add_handler(CommandHandler('authorization', command_callbacks.authorization))
        self._dispatcher.add_handler(MessageHandler(Filters.command, command_callbacks.unknown))

        self._dispatcher.add_handler(ConversationHandler(
            [MessageHandler(Filters.contact, message_callbacks.authorization)],
            {'pending_answer': [MessageHandler(Filters.regex('Хочу'), message_callbacks.ask_for_name),
                                MessageHandler(Filters.regex('Не хочу'), message_callbacks.end_conversation)],
             'pending_name': [MessageHandler(Filters.text, message_callbacks.push_personal_info_to_people_sheet)]},
            [MessageHandler(Filters.command | Filters.text, message_callbacks.request_continuation_of_conversation)]))

        self._create_update_data_job()
        self._create_push_notification_jobs()

        self._faq_handlers = []
        self._create_faq_handlers()

        self._dispatcher.add_error_handler(exception.telegram_bot_update_error)

    def invoke(self):
        self._updater.start_polling()
        self._updater.idle()

    def dump_persistence_obj(self):
        util.file_processing.dump_json_string_to_file(self._persistence.user_data_json, self._persistence_path)

    """ Create methods """

    def _create_update_data_job(self):
        self._updater.job_queue.run_repeating(job_callbacks.update_data_sheets, datetime.timedelta(seconds=30))

    def _create_mapping_from_people_sheet(self, people_sheet):
        self._phone_number_to_person_info_dict = {}
        self._number_of_groups = len(people_sheet[0]) - 3

        for i in range(1, len(people_sheet)):
            self._phone_number_to_person_info_dict[people_sheet[i][0]] = {'name': people_sheet[i][1],
                                                                          'authorization_status': people_sheet[i][2],
                                                                          'groups': set()}
            for j in range(3, len(people_sheet[0])):
                if int(people_sheet[i][j]):
                    self._phone_number_to_person_info_dict[people_sheet[i][0]]['groups'].add(people_sheet[0][j])

        for telegram_id, user_data in self._updater.dispatcher.user_data.items():
            try:
                if user_data['authorized']:
                    self._phone_number_to_person_info_dict[user_data['phone_number']]['telegram_id'] = telegram_id
            except KeyError:
                pass

    def _create_push_notification_jobs(self):
        self._push_notification_jobs = []
        for text, groups, send_time in self._push_notifications_sheet:
            groups = set(groups.split(','))

            if send_time.timestamp() > datetime.datetime.today().timestamp():
                self._push_notification_jobs.append(self._updater.job_queue.run_once(
                    job_callbacks.create_push_notification_callback_from_push_text(text), send_time,
                    context=(self._phone_number_to_person_info_dict, groups)))

    def _create_faq_handlers(self):
        for question, answer in self._faq_sheet:
            if answer[0] == '#':
                self._faq_handlers.append(MessageHandler(filters.PrepareMessageTextForRegexFilter(
                    question), message_callbacks.personalized_callbacks_dict[answer[1:]]))
            else:
                self._faq_handlers.append(MessageHandler(filters.PrepareMessageTextForRegexFilter(
                    question), message_callbacks.create_callback_from_answer(answer)))

            self._dispatcher.add_handler(self._faq_handlers[-1])

        self._faq_handlers.append(MessageHandler(Filters.text,
                                                 message_callbacks.create_callback_from_answer(
                                                     'К сожалению, я Вас не понимаю. Попробуйте перефразировать'
                                                     ' вопрос.')))
        self._updater.dispatcher.add_handler(self._faq_handlers[-1])

    """ Remove methods """

    def _remove_mapping_for_people_sheet(self):
        self._phone_number_to_person_info_dict.clear()

    def _remove_prev_push_notification_jobs(self, prev_push_notification_jobs_sheet_length):
        push_notification_jobs_to_be_deleted = self._push_notification_jobs[:prev_push_notification_jobs_sheet_length]

        for push_notification_job in push_notification_jobs_to_be_deleted:
            self._push_notification_jobs.pop(self._push_notification_jobs.index(push_notification_job)).\
                schedule_removal()

    def _remove_prev_faq_handlers(self, prev_faq_handlers_sheet_length):
        faq_handlers_to_be_deleted = self._faq_handlers[:prev_faq_handlers_sheet_length]

        for faq_handler in faq_handlers_to_be_deleted:
            self._dispatcher.remove_handler(self._faq_handlers.pop(self._faq_handlers.index(faq_handler)))

    """ Update methods """

    def _update_mapping_for_people_sheet(self, people_sheet):
        self._remove_mapping_for_people_sheet()
        self._create_mapping_from_people_sheet(people_sheet)

    def _update_push_notification_jobs(self):
        push_notification_jobs_sheet_length = len(self._push_notification_jobs)
        self._create_push_notification_jobs()
        self._remove_prev_push_notification_jobs(push_notification_jobs_sheet_length)

    def _update_faq_handlers(self):
        faq_handlers_sheet_length = len(self._faq_handlers)
        self._create_faq_handlers()
        self._remove_prev_faq_handlers(faq_handlers_sheet_length)

    def update_data_sheets(self, people_sheet, push_notifications_sheet, faq_sheet, classes_schedule_sheet):
        self._update_mapping_for_people_sheet(people_sheet)

        self._push_notifications_sheet = push_notifications_sheet
        self._update_push_notification_jobs()

        self._faq_sheet = faq_sheet
        self._update_faq_handlers()

        self._classes_schedule_sheet = classes_schedule_sheet

    """ Set methods """

    def set_person_telegram_id(self, phone_number, telegram_id):
        self._phone_number_to_person_info_dict[phone_number]['telegram_id'] = telegram_id

    """ Get methods """

    def get_mapping_for_people_sheet(self):
        return self._phone_number_to_person_info_dict

    def get_classes_schedule_sheet(self):
        return self._classes_schedule_sheet

    def get_number_of_groups(self):
        return self._number_of_groups
