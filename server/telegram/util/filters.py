import telegram.ext


class PrepareMessageTextForRegexFilter(telegram.ext.BaseFilter):

    def __init__(self, pattern):
        self._pattern = pattern

    def filter(self, message):
        message.text = message.text.lower()

        return telegram.ext.Filters.regex(self._pattern).filter(message)
