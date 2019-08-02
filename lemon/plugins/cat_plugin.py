"""
Plugin that sends a random cat photo.
"""
from lemon.plugins.base_plugin import BasePlugin
from lemon.plugins.enforce_types import EnforceTypes


class CatPlugin(BasePlugin):
    NAME = "cat"
    ENFORCE_TYPE = EnforceTypes.ANY

    def _execute(self):
        self._send_photo(url="https://data.whicdn.com/images/298844185/large.jpg?t=1507433077",
                         caption="Meow")
