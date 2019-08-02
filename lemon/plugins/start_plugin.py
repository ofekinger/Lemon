"""
Init plugin to test minimal framework.
"""
from lemon.plugins.base_plugin import BasePlugin
from lemon.plugins.enforce_types import EnforceTypes


class StartPlugin(BasePlugin):
    NAME = "start"
    ENFORCE_TYPE = EnforceTypes.ALL

    def _execute(self):
        """
        Sends a friendly hello.
        """
        self._send_text_message("Hello, world!")
        self._send_sticker("CAADBAADlQADQKqxCB_B7ATNGePNAg")
