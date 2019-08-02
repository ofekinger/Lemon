"""
Any plugin can do the following:
1. Send a text message
2. Send a sticker
3. Send an image (with caption [optional])
"""


class BasePlugin:
    def __init__(self):
        self.__bot = None
        self.__update = None

    def execute(self, bot, update):
        self.__bot = bot
        self.__update = update
        self._execute()

    def _execute(self):
        raise NotImplementedError()

    def _send_text_message(self, message, chat_id=None):
        self.__bot.send_message(chat_id=chat_id or self.__update.chat_id,
                                text=message)
