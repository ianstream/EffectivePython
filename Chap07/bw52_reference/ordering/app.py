import logging
from pprint import pprint
from sys import stdout as STDOUT


# Example 6
class Prefs(object):
    def get(self, name):
        pass

prefs = Prefs()

import dialog  # Moved. 그러나 PEP8 가이드에 맞지 않는다
dialog.show()