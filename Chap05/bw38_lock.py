# GIL 은 데이터의 원자성까지 보장해줄까? 그렇지 않다.

import logging
from pprint import pprint
from sys import stdout as STDOUT


# 전역에서 사용하기 위한 카운터
class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


def worker(sensor_index, how_many, counter):
    BARRIER.wait()
    for _ in range(how_many):
        counter.increment(1)


# 센서별로 작업 스레드를 시작하고 읽기를 모두 마칠때까지 기다린다
from threading import Barrier, Thread

BARRIER = Barrier(5)

def run_threads(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


how_many = 10**5
counter = Counter()
run_threads(worker, how_many, counter)
print('Counter should be %d, found %d' %
      (5 * how_many, counter.count))


offset = 5
counter.count += offset


value = getattr(counter, 'count')
result = value + offset
setattr(counter, 'count', result)
print(value)

# Running in Thread A
value_a = getattr(counter, 'count')
print(value)

# Context switch to Thread B
value_b = getattr(counter, 'count')
print(value_b)
result_b = value_b + 1
print(result_b)

setattr(counter, 'count', result_b)
# Context switch back to Thread A
result_a = value_a + 1
print(value_a)
print(result_a)

setattr(counter, 'count', result_a)
print(result_a)


from threading import Lock

class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        # 이제 한번에 한 스레드만 잠금을 얻을 수 있다
        with self.lock:
            self.count += offset


BARRIER = Barrier(5)
counter = LockingCounter()
run_threads(worker, how_many, counter)
print('Counter should be %d, found %d' %
      (5 * how_many, counter.count))

