import telegram
import telegram.ext


def create_push_notification_callback_from_push_text(push_text):
    @telegram.ext.dispatcher.run_async
    def callback(context):
        for person_info in context.job.context[0].values():
            if person_info['groups'] & context.job.context[1]:
                try:
                    context.bot.send_message(chat_id=person_info['telegram_id'], text=push_text)
                except KeyError:
                    pass

    return callback


def update_data_sheets(context):
    from util.apis_util import APIsUtil

    APIsUtil.update_telegram_api_data_sheets()
    APIsUtil.dump_telegram_api_persistence_obj()
