import telegram.ext


class PrepareMessageTextForRegexFilter(telegram.ext.BaseFilter):

    def __init__(self, pattern):
        super.__init__()

        self._pattern = pattern

    def filter(self, message):
        return telegram.ext.Filters.regex(self._pattern).filter(message.text.lower())
