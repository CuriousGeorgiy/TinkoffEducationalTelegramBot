def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Приветствую вас!")


def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Сожалею, но я не понимаю эту команду.")