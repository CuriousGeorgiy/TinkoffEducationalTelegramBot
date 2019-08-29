from telegram.ext import run_async


def create_push_notification_callback_from_push_text(push_text):
    @run_async
    def callback(context):
        for person_info in context.job.context[0].values():
            if person_info['groups'] & context.job.context[1]:
                try:
                    context.bot.send_message(chat_id=person_info['telegram_id'], text=push_text)
                except KeyError:
                    pass

    return callback


def update_data_sheets(context):
    from util.api_wrappers_util import APIWrappersUtil

    APIWrappersUtil.update_telegram_api_wrapper_data_sheets()
    APIWrappersUtil.dump_telegram_api_wrapper_persistence_obj()
