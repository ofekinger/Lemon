#!/usr/bin/python
from lemon.communication import TelegramCommunicator
from lemon.logger import Logger
from lemon.plugins.start_plugin import StartPlugin


def main():
    Logger.initialize()
    communicator = TelegramCommunicator()
    communicator.register_plugin("start", StartPlugin())
    communicator.start()


if __name__ == "__main__":
    main()
