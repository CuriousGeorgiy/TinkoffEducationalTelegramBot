import telegram
import telegram.ext

import telegram_.decorators


@telegram.ext.run_async  # May cause problems, needs to be tested.
@telegram_.decorators.send_action(telegram.ChatAction.TYPING)
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Приветствую Вас! Для использования бота необходимо'
                                                                  ' пройти авторизацию по номеру телефона.',
                             reply_markup=telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton(text='Отправить'
                                                                                                      ' контакты',
                                                                        request_contact=True)]]))


@telegram.ext.run_async  # May cause problems, needs to be tested.
@telegram_.decorators.send_action(telegram.ChatAction.TYPING)
def authorization(update, context):
    try:
        if context.user_data['authorized']:
            context.bot.send_message(chat_id=update.message.chat_id, text='Вы уже прошли авторизацию и можете' 
                                                                          'пользоваться ботом.')
    except KeyError:
        context.bot.send_message(chat_id=update.message.chat_id, text='Авторизация проходит по номеру Вашего'
                                                                      ' телефона.',
                                 reply_markup=telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton(
                                     text='Отправить'' контакты', request_contact=True)]]))


@telegram.ext.run_async
@telegram_.decorators.send_action(telegram.ChatAction.TYPING)
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Такой команды у меня нет.')
