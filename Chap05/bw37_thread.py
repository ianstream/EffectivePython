# 파이썬 표준구현인 CPython 은 GIL 이라고 불리는 전역 인터프리터 잠금 이라는 매커니즘으로 동작한다
# http://egloos.zum.com/mcchae/v/11099578, http://www.slideshare.net/yongho/2011-h3


import logging
from pprint import pprint
from sys import stdout as STDOUT


# 인수분해
def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

from time import time

numbers = [2139079, 1214759, 1516637, 1852285]
start = time()

for number in numbers:
    list(factorize(number))
end = time()

print('Took %.3f seconds' % (end - start))


# 멀티 스레드로 돌려보자

from threading import Thread

# 파이썬 스레드로 정의
class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


start = time()
threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
end = time()

print('Thread Took %.3f seconds' % (end - start))


import select, socket

def slow_systemcall():
    # 0.1 초간 블로킹
    select.select([socket.socket()], [], [], 0.1)


start = time()
threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)


def compute_helicopter_location(index):
    pass

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time()
print('slow_systemcall Took %.3f seconds' % (end - start))

# 여러 시스템 호출을 병렬로 수행하려면 파이썬 스레드를 사용하자. 이렇게 하면 계산을 하면서도 블로킹 I/O 를 수행할 수 있다
