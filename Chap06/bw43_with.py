# 파이썬의 with 는 코드를 특별한 컨텍스트에서 실행함을 나타내는데 사용한다

from threading import Lock

lock = Lock()

"""
아래 코드는 다음과 동일하다

lock.acquire()
try:
    print('lock is held')
finally:
    lock.release()
"""
with lock:
    print('lock is held')


# 코드의 특정 영역에 더 많은 디버깅 로그를 넣고 싶다고 가정하자. 아래와 같은 함수엔 로그레벨이 섞인 로그가 있다

import logging
import time

logging.getLogger().setLevel(logging.WARNING)

def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('More debug data')

my_function()


# 이제 컨텍스트 매니저를 정의해 로그 수준을 임시로 높이자
from contextlib import contextmanager

@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield # http://haerakai.tistory.com/34
    finally:
        logger.setLevel(old_level)

print('\n\n')
with debug_logging(logging.DEBUG):
    print('Inside:')
    my_function()
    time.sleep(0.5)

print('After:')
time.sleep(0.5)
my_function()


# file open 시에도 with 를 사용하면 블록이 종료될 때 핸들을 닫아준다
with open('test.txt', 'w') as handle:
    handle.write('This is some data!')


