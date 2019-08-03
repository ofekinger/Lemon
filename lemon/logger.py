import logging


class Logger(object):
    @staticmethod
    def initialize():
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
