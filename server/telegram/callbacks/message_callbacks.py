import datetime

import telegram
import telegram.ext

import server.telegram.decorators


def create_callback_from_answer(answer):
    @telegram.ext.dispatcher.run_async
    @server.telegram.decorators.send_action(telegram.ChatAction.TYPING)
    def callback(update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text=answer)

    return callback


@server.telegram.decorators.send_action(telegram.ChatAction.TYPING)
def authorization(update, context):
    from util.apis_util import APIsUtil

    phone_number_to_id, _ = APIsUtil.get_telegram_api_mappings_for_people_sheet()
    if update.message.contact.phone_number[0].isdigit():
        update.message.contact.phone_number = '+' + update.message.contact.phone_number

    if update.message.contact.phone_number in phone_number_to_id:
        context.user_data['authorized'] = True
        context.user_data['id_in_telegram_api'] = phone_number_to_id[update.message.contact.phone_number]
        APIsUtil.set_telegram_api_person_telegram_id(phone_number_to_id[update.message.contact.phone_number],
                                                     update.message.chat_id)
        context.bot.send_message(chat_id=update.message.chat_id, text='Вы прошли авторизацию, теперь Вы можете' 
                                                                      ' пользоваться ботом.',
                                 reply_markup=telegram.ReplyKeyboardRemove())

        APIsUtil.dump_telegram_api_persistence_obj()
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='Сожалею, но Вы не прошли авторизацию.',
                                 reply_markup=telegram.ReplyKeyboardRemove())


@telegram.ext.dispatcher.run_async # May cause problems, needs to be tested.
@server.telegram.decorators.send_action(telegram.ChatAction.TYPING)
def nearest_class(update, context):
    from util.apis_util import APIsUtil

    try:
        if context.user_data['authorized']:
            _, id_to_person_info = APIsUtil.get_telegram_api_mappings_for_people_sheet()

            groups = id_to_person_info[context.user_data['id_in_telegram_api']]['groups']
            classes_schedule = APIsUtil.get_telegram_api_classes_schedule_sheet()
            message_text = ''

            for group, class_type, class_date in classes_schedule:
                if (group in groups) and (class_date.timestamp() > datetime.datetime.today().timestamp()):
                    message_text += 'Ближайшее по расписанию занятие у направления {0} {1}. Тип занятия: {2}.\n'.\
                        format(group, class_date.strftime('%d.%m.%Y %H:%M'), class_type)
                    groups.remove(group)

            context.bot.send_message(chat_id=update.message.chat_id, text=message_text)

    except KeyError:
        context.bot.send_message(chat_id=update.message.chat_id, text='Для использования бота необходимо пройти'
                                                                      ' авторизацию с помощью команды'
                                                                      ' /authorization.')


personalized_callbacks_dict = {'nearest_class': nearest_class}
