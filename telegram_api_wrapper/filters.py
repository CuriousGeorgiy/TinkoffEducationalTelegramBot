from telegram.ext import BaseFilter, Filters


class PrepareMessageTextForRegexFilter(BaseFilter):

    def __init__(self, pattern):
        self._pattern = pattern

    def filter(self, message):
        message.text = message.text.lower()

        return Filters.regex(self._pattern).filter(message)
