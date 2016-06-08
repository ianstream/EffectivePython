import json
from datetime import datetime
from time import sleep

# 로그 메세지를 출력한다고 해보자
def log(message, when=datetime.now()):
    print('%s %s' % (when, message))

# test
log('hello world!')
sleep(0.5)
log('hello again!')

# 동적 기본인수를 위해 기본값을 None 으로 하고 docstring(문서화 문자열)을 추가해준다
def log(message, when=None):
    """
    시간과 문자열을 출력해준다
    :param message: 메세지내용
    :param when: 시간정보
    :return: 표준 화면 로깅
    """
    when = datetime.now() if when is None else when
    print('%s %s' % (when, message))

# test
log('hello world!')
sleep(0.5)
log('hello again!')





def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default

foo = decode('bad data')
foo['stuff'] = 5

bar = decode('also bad')
bar['meep'] = 1

print('foo:', foo)
print('bar:', bar)

# 다르게 나올거라 기대했겠지만, 결과는 같다. 키워드 인수의 기본값을 None 으로 설정하고 동작을 문서화하자

def decode(data, default=None):
    """Load json data from a string

    args:
        data: json data to decode
        default: value to return if decofing fails
            defaults to am empty dictionary
    """
    if default is None:
        default = {}

    try:
        return json.loads(data)
    except ValueError:
        return default


foo = decode('bad data')
foo['stuff'] = 5

bar = decode('also bad')
bar['meep'] = 1

print('foo:', foo)
print('bar:', bar)

# 기본인수는 모듈 로드 시점에 함수 정의과정에서 한번만 평가된다. 그러므로 동적으로 값을 넘길때는 None 을 사용해야 한다


