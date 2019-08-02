from lemon.plugins.enforce_types import EnforceTypes


class BasePlugin:
    NAME = ""
    ENFORCE_TYPE = EnforceTypes.ANY

    def __init__(self, database_communication):
        self.__bot = None
        self.__update = None
        self.__keywords = None
        self.__database_communication = database_communication

    def execute(self, bot, update):
        """
        Wrapper function for internal plugin.
        Invoked by the communication object.
        """
        message = update.message.text
        if self.ENFORCE_TYPE == EnforceTypes.ANY:
            found = False
            for word in message.split():
                if word in self.keywords:
                    found = True
                    break
            if not found:
                return
        elif self.ENFORCE_TYPE == EnforceTypes.ALL:
            for keyword in self.keywords:
                if keyword not in message:
                    return
        elif self.ENFORCE_TYPE == EnforceTypes.START:
            found = False
            for keyword in self.keywords:
                if message.startswith(keyword):
                    found = True
                    break
            if not found:
                return

        self.__bot = bot
        self.__update = update
        self._execute()

    def _execute(self):
        """
        The internal function that each Plugin should implement.
        Executes the plugin's purpose.
        """
        raise NotImplementedError()

    @property
    def arguments(self):
        return " ".join(self.__update.message.text.split()[1:]) if self.__update else None

    @property
    def keywords(self):
        if self.__keywords:
            return self.__keywords

        self.__keywords = self.__database_communication.get_plugin(self.NAME).keywords
        return self.__keywords

    def _send_text_message(self, message, chat_id=None):
        """
        Sends a basic text message to the given chat_id
        :param message: The text message to send
        :param chat_id: The chat ID to send the message to. Defaults to the chat the message was sent from.
        """
        self.__bot.send_message(chat_id=chat_id or self.__update.message.chat_id,
                                text=message)

    def _send_sticker(self, sticker_id, chat_id=None):
        """
        Sends a sticker to the user
        :param sticker_id: The ID of the sticker
        :param chat_id: The chat ID to send the sticker to. Defaults to the chat the message was sent from.
        """
        self.__bot.send_sticker(chat_id=chat_id or self.__update.message.chat_id,
                                sticker=sticker_id)

    def _send_photo(self, url, caption=None, chat_id=None):
        """
        Sends a photo to the user
        :param url: The URL of the photo.
        :param caption: Optional caption for the photo.
        :param chat_id: The chat ID to send the sticker to. Defaults to the chat the message was sent from.
        """
        self.__bot.send_photo(photo=url,
                              caption=caption,
                              chat_id=chat_id or self.__update.message.chat_id)
