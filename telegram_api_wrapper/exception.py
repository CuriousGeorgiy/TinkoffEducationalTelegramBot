from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError

from logging import getLogger


def telegram_bot_update_error(update, context):
    getLogger("main." + __name__).warning('Update "%s" caused error "%s"', update, context.error)

    try:
        raise context.error
    except Unauthorized:
        pass
    except BadRequest:
        pass
    except TimedOut:
        pass
    except NetworkError:
        pass
    except ChatMigrated as e:
        pass
    except TelegramError:
        pass
