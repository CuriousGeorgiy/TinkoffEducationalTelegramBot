from telegram.ext import BaseFilter, Filters
from telegram import Message


class PrepareMessageTextForRegexFilter(BaseFilter):

    def __init__(self, pattern: str):
        self._pattern = pattern

    def filter(self, message: Message) -> bool:
        message.text = message.text.lower()

        return Filters.regex(self._pattern).filter(message)
