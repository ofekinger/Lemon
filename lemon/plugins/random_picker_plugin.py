"""
Plugin that picks a random choice from given options.
"""
import random

from lemon.plugins.base_plugin import BasePlugin
from lemon.plugins.enforce_types import EnforceTypes


class RandomPickerPlugin(BasePlugin):
    NAME = "random"
    ENFORCE_TYPE = EnforceTypes.START

    def _execute(self):
        self._send_text_message("My choice is: {}".format(random.choice(self.arguments.split())))
