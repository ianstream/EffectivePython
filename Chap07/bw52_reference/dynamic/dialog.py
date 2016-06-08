import logging
from pprint import pprint
from sys import stdout as STDOUT


# Example 11
# Reenabling this will break things.
# import app

class Dialog(object):
    def __init__(self):
        pass

# Using this instead will break things
# save_dialog = Dialog(app.prefs.get('save_dir'))
save_dialog = Dialog()

def show():
    """
    아래 방법을 이용하면 모듈을 정의하고 임포트하는 방식을 구조적으로 변경하지 않아도 된다
    이런 방법은 import 비용이 비싼 관계로 추천하지 않는다.
    루프가 복잡한 곳에 사용 시 문제가 있고 런타임 시에 실패를 가져올 수 있다.
    그러나, 전체 프로그램을 재구성하는 것 보다는 낮기 때문에 꼭 사용해야 한다면 주의해서 사용하자
    """
    import app  # Dynamic import.
    save_dialog.save_dir = app.prefs.get('save_dir')
    print('Showing the dialog!')
