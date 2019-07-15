import server.telegram.util.decorators

from telegram.chataction import ChatAction


def create_callback_from_answer(answer):
    @server.telegram.util.decorators.send_action(ChatAction.TYPING)
    def callback(update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text=answer)

    return callback
