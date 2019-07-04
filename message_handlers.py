def idunno(update, context):
    context.bot.send_message(update.message.chat_id,
                             text="К сожалению, разработчик успел лишь научить меня повторять за вами :(")
    context.bot.send_message(update.message.chat_id, text=update.message.text)