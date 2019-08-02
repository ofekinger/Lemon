"""
Init plugin to test minimal framework.
"""
from lemon.plugins.base_plugin import BasePlugin


class StartPlugin(BasePlugin):
    def _execute(self):
        self._send_text_message("Hello, world!")
