import server.telegram.util.decorators

from telegram.chataction import ChatAction

import telegram


def create_callback_from_answer(answer):
    @server.telegram.util.decorators.send_action(ChatAction.TYPING)
    def callback(update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text=answer)

    return callback


@server.telegram.util.decorators.send_action(ChatAction.TYPING)
def authorization(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Ваш номер телефона: ' +
                                                                  update.message.contact.phone_number,
                             reply_markup=telegram.ReplyKeyboardRemove())
