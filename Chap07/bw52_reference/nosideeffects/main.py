import logging
from pprint import pprint
from sys import stdout as STDOUT


# 임포트, 설정, 액티비티의 구성의 세 단계로 이루어 짐
import app
import dialog

app.configure()
dialog.configure()

dialog.show()
