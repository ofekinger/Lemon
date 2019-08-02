from lemon.plugins.base_plugin import BasePlugin
from lemon.plugins.enforce_types import EnforceTypes


class CopycatPlugin(BasePlugin):
    NAME = "copycat"
    ENFORCE_TYPE = EnforceTypes.START

    def _execute(self):
        if self.arguments:
            self._send_text_message(self.arguments)
            self._send_photo("https://theawesomedaily.com/wp-content/uploads/2018/04/why-do-cats-stick-their-tongue-out-feat-1-1-620x350.jpg")
