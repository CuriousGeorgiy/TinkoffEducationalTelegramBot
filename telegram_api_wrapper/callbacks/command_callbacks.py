from telegram import ChatAction, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import run_async

from telegram_api_wrapper.decorators import send_action


@run_async  # May cause problems, needs to be tested.
@send_action(ChatAction.TYPING)
def start(update, context):
    try:
        if context.user_data['authorized']:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text='Приветствую Вас! Вы уже авторизованы и можете пользоваться всеми функциями'
                                          ' бота.')
    except KeyError:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Приветствую Вас! Для доступа к некоторым функциям бота необходимо пройти'
                                      ' авторизацию с помощью команды /authorization.')


@run_async  # May cause problems, needs to be tested.
@send_action(ChatAction.TYPING)
def authorization(update, context):
    try:
        if context.user_data['authorized']:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text='Вы уже авторизованы и можете пользоваться всеми функциями бота.')
    except KeyError:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Авторизация проходит по номеру Вашего телефона.',
                                 reply_markup=ReplyKeyboardMarkup([[KeyboardButton(
                                     text='Отправить контакты', request_contact=True)]], one_time_keyboard=True))


@run_async
@send_action(ChatAction.TYPING)
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Такой команды у меня нет.')
