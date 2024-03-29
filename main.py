#!/usr/bin/python
from lemon.communication import TelegramCommunicator
from lemon.database_operations import DatabaseCommunication
from lemon.logger import Logger
from lemon.plugins.cat_plugin import CatPlugin
from lemon.plugins.copycat_plugin import CopycatPlugin
from lemon.plugins.movie_finder_plugin import MovieFinderPlugin
from lemon.plugins.random_picker_plugin import RandomPickerPlugin
from lemon.plugins.start_plugin import StartPlugin


def main():
    Logger.initialize()
    comms = DatabaseCommunication()

    # comms.add_plugin("start", ["Hello", "Lemon"])
    # comms.add_plugin("cat", ["cat", "meow"])
    # comms.add_plugin("copycat", ["copy", "copycat"])

    communicator = TelegramCommunicator()
    communicator.register_plugin(StartPlugin(comms))
    communicator.register_plugin(CatPlugin(comms))
    communicator.register_plugin(CopycatPlugin(comms))
    communicator.register_plugin(RandomPickerPlugin(comms))
    communicator.register_plugin(MovieFinderPlugin(comms))
    communicator.start()


if __name__ == "__main__":
    main()
