from logging import getLogger


def telegram_bot_update_error(update, context):
    """ Log errors caused by updates """
    
    getLogger("main." + __name__).warning('Update "%s" caused error "%s"', update, context.error)
