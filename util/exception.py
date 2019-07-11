import telegram.error

import logging


def telegram_bot_update_error(update, context):
    logging.getLogger("main." + __name__).warning('Update "%s" caused error "%s"', update, context.error)

    try:
        raise context.error
    except telegram.error.Unauthorized:
        pass
    except telegram.error.BadRequest:
        pass
    except telegram.error.TimedOut:
        pass
    except telegram.error.NetworkError:
        pass
    except telegram.error.ChatMigrated as e:
        pass
    except telegram.error.TelegramError:
        pass
