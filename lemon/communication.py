from telegram.ext import Updater, MessageHandler, Filters

TOKEN = '905653274:AAHrZ0mPd2LnZ2joBDtHMEnsIbrdueTYRiU'


class TelegramCommunicator:
    def __init__(self):
        self.__updater = Updater(TOKEN)
        self.__plugins = []
        self.__updater.dispatcher.add_handler(MessageHandler(filters=Filters.text,
                                                             callback=lambda bot, update:
                                                             [plugin.execute(bot, update)
                                                              for plugin in self.__plugins]))

    def register_plugin(self, plugin):
        """
        Adds a plugin to the dispatcher.
        :param name: The name of the plugin
        :param plugin: The plugin object
        :type plugin: BasePlugin
        """
        self.__plugins.append(plugin)

    def start(self):
        """
        Starts the communication aspect of the service.
        """
        self.__updater.start_polling()
