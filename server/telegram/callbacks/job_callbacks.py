import server.telegram.decorators

import telegram
import telegram.ext


def create_push_notification_callback_from_push_text(push_text):
    @telegram.ext.dispatcher.run_async
    @server.telegram.decorators.send_action(telegram.ChatAction.TYPING)
    def callback(context):
        for person in context.job.context[0].values():
            if person['groups'] & context.job.context[1]:
                context.bot.send_message(chat_id=person['telegram_id'], text=push_text)

    return callback


def update_data(context):
    from server.telegram.telegram_util import TelegramUtil

    TelegramUtil.update_telegram_api_data()