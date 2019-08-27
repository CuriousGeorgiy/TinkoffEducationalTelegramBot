import datetime

from telegram import ChatAction, ReplyKeyboardMarkup
from telegram.ext import run_async, ConversationHandler

from telegram_api_wrapper.decorators import send_action


def create_callback_from_answer(answer):
    @run_async
    @send_action(ChatAction.TYPING)
    def callback(update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text=answer)

    return callback


@send_action(ChatAction.TYPING)
def authorization(update, context):
    from util.api_wrappers_util import APIsUtil

    phone_number_to_person_info_dict = APIsUtil.get_telegram_api_mapping_for_people_sheet()

    if update.message.contact.phone_number[0].isdigit():
        update.message.contact.phone_number = '+' + update.message.contact.phone_number

    context.user_data['phone_number'] = update.message.contact.phone_number

    if context.user_data['phone_number'] in phone_number_to_person_info_dict and \
            phone_number_to_person_info_dict[context.user_data['phone_number']]['authorization_status'] == '1':

        context.user_data['authorized'] = True
        APIsUtil.set_telegram_api_person_telegram_id(update.message.contact.phone_number, update.message.chat_id)

        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Вы прошли авторизацию и теперь можете пользоваться всеми функциями бота.')

        APIsUtil.dump_telegram_api_persistence_obj()
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='Сожалею, но Вы не прошли авторизацию.')
        if context.user_data['phone_number'] in phone_number_to_person_info_dict:
            context.bot.send_message(chat_id=update.message.chat_id, text='Вы уже есть в моей ведомости. В случае'
                                                                          ' успешного прохождения отбора я Вас'
                                                                          ' авторизую.')
        if not (context.user_data['phone_number'] in phone_number_to_person_info_dict):
            context.bot.send_message(chat_id=update.message.chat_id, text='Если Вы планируете ходить на курсы Tinkoff'
                                                                          ' Generation, я могу добавить Вас в свою'
                                                                          ' ведомость и в случае успешного прохождения'
                                                                          ' отбора авторизовать.',
                                     reply_markup=ReplyKeyboardMarkup([['Планирую', 'Не планирую']],
                                                                      one_time_keyboard=True))

            return 'pending_answer'


@run_async
@send_action(ChatAction.TYPING)
def request_continuation_of_conversation(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Требуется закончить диалог.')


@run_async
@send_action(ChatAction.TYPING)
def ask_for_name(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Как Вас зовут (имя фамилия)?')

    return 'pending_name'


@run_async
@send_action(ChatAction.TYPING)
def end_conversation(update, context):
    return ConversationHandler.END


@run_async
@send_action(ChatAction.TYPING)
def push_personal_info_to_people_sheet(update, context):
    from util.api_wrappers_util import APIsUtil

    APIsUtil.append_person_to_people_sheet('\'' + context.user_data['phone_number'], update.message.text)

    context.bot.send_message(chat_id=update.message.chat_id, text='Отлично, я добавил Вас в свою ведомость.')

    return ConversationHandler.END


@run_async  # May cause problems, needs to be tested.
@send_action(ChatAction.TYPING)
def nearest_class(update, context):
    from util.api_wrappers_util import APIsUtil

    try:
        if context.user_data['authorized']:
            phone_number_to_person_info_dict = APIsUtil.get_telegram_api_mapping_for_people_sheet()

            groups = phone_number_to_person_info_dict[context.user_data['phone_number']]['groups']
            classes_schedule = APIsUtil.get_telegram_api_classes_schedule_sheet()
            message_text = ''

            for group, class_type, class_date in classes_schedule:
                if (group in groups) and (class_date.timestamp() > datetime.datetime.today().timestamp()):
                    message_text += 'Ближайшее по расписанию занятие у направления {0} {1} . Тип занятия: {2}.\n'.\
                        format(group, class_date.strftime('%d.%m.%Y в %H:%M'), class_type)
                    groups.remove(group)

            context.bot.send_message(chat_id=update.message.chat_id, text=message_text)

    except KeyError:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Для использования некоторых фукнций бота необходимо пройти авторизацию с помощью'
                                      ' команды /authorization .')


personalized_callbacks_dict = {'nearest_class': nearest_class}
