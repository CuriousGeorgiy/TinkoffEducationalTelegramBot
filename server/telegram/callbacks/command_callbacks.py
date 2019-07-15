import server.telegram.util.decorators

from telegram.chataction import ChatAction


@server.telegram.util.decorators.send_action(ChatAction.TYPING)
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Приветствую вас!")


@server.telegram.util.decorators.send_action(ChatAction.TYPING)
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Сожалею, но я не понимаю эту команду.")