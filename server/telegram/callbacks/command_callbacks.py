import server.telegram.util.decorators

from telegram.chataction import ChatAction

import telegram


@server.telegram.util.decorators.send_action(ChatAction.TYPING)
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Приветствую вас! Для использования бота необходимо "
                                                                  "авторизоваться по номеру телефона.", reply_markup=
                             telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton(text="Отправить контакты",
                                                                                    request_contact=True)]]))


@server.telegram.util.decorators.send_action(ChatAction.TYPING)
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Сожалею, но я не понимаю эту команду.")
