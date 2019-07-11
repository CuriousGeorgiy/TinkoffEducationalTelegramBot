def create_callback_from_answer(answer):
    def callback(context):
        context.bot.send_message(chat_id=533875319, text=answer)

    return callback
