import server.telegram.decorators

import telegram
import telegram.ext


def create_callback_from_answer(answer):
    @telegram.ext.dispatcher.run_async
    @server.telegram.decorators.send_action(telegram.ChatAction.TYPING)
    def callback(update, context):
        if context.user_data['authorized']:
            context.bot.send_message(chat_id=update.message.chat_id, text=answer)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text='Для использования бота необходимо пройти'
                                                                          ' авторизацию с помощью команды'
                                                                          ' /authorization.')

    return callback


@server.telegram.decorators.send_action(telegram.ChatAction.TYPING)
def authorization(update, context):
    from server.telegram.telegram_util import TelegramUtil

    phone_number_to_id, id_to_person_info = TelegramUtil.get_telegram_api_mappings_for_people_list()

    if update.message.contact.phone_number in phone_number_to_id:
        context.user_data['authorized'] = True
        TelegramUtil.set_telegram_api_person_telegram_id(phone_number_to_id[update.message.contact.phone_number],
                                                         update.message.chat_id)
        context.bot.send_message(chat_id=update.message.chat_id, text=context.user_data['info'][0]+', Вы прошли ' 
                                                                                                   'авторизацию, теперь'
                                                                                                   ' вы можете' 
                                                                                                   ' пользоваться'
                                                                                                   ' ботом.',
                                 reply_markup=telegram.ReplyKeyboardRemove())
    else:
        context.user_data['authorized'] = False
        context.bot.send_message(chat_id=update.message.chat_id, text='Сожалею, но Вы не прошли авторизацию.',
                                 reply_markup=telegram.ReplyKeyboardRemove())


@telegram.ext.dispatcher.run_async
@server.telegram.decorators.send_action(telegram.ChatAction.TYPING)
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='К сожалению, я Вас не понимаю. Попробуйте'
                                                                  ' перефразировать вопрос.')
