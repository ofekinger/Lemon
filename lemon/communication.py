from telegram.ext import Updater, CommandHandler

TOKEN = '905653274:AAHrZ0mPd2LnZ2joBDtHMEnsIbrdueTYRiU'


class TelegramCommunicator:
    def __init__(self):
        self.__updater = Updater(TOKEN)

    def register_plugin(self, name, plugin):
        self.__updater.dispatcher.add_handler(CommandHandler(name, plugin.execute))

    def start(self):
        self.__updater.start_polling()
