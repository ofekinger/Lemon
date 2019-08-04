import telegram
import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from lemon.plugins.enforce_types import EnforceTypes


class MenuOption:
    def __init__(self, text, url=None):
        self.text = text
        self.url = url


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

    def _send_video(self, url, caption=None, chat_id=None):
        self.__bot.send_video(video=url,
                              caption=caption,
                              chat_id=chat_id or self.__update.message.chat_id)

    def _send_youtube_video(self, url, chat_id=None):
        self._send_text_message(message="@youtube {}".format(url),
                                chat_id=chat_id or self.__update.message.chat_id)

    @staticmethod
    def __build_menu(buttons,
                     n_cols,
                     header_buttons=None,
                     footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, [header_buttons])
        if footer_buttons:
            menu.append([footer_buttons])
        return menu

    @staticmethod
    def __chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def _build_menu(self, options, text, reply_prefix=None):
        """
        Builds an interactive menu that sends a callback as soon as the user chooses an option.
        :param text: Text that will be sent before the options.
        :param options: List of options to build the menu from.
        """
        buttons = [InlineKeyboardButton(option.text,
                                        url=option.url,
                                        switch_inline_query_current_chat=" ".join([reply_prefix, option.text])
                                        if reply_prefix else option.text)
                   for option in options]

        number_of_columns = 1
        try:
            reply_markup = InlineKeyboardMarkup(self.__build_menu(buttons, number_of_columns))
            logging.debug("Trying to send {} options: {}".format(len(options), options))
            self.__bot.send_message(reply_markup=reply_markup,
                                    chat_id=self.__update.message.chat_id,
                                    text=text)
        except telegram.error.BadRequest:
            logging.debug("Could not send all options at once")
            for chunk in self.__chunks(options, 10):
                self._build_menu(chunk, text, reply_prefix)
