import logging
from pprint import pprint
from sys import stdout as STDOUT


# 속도 측정을 위한 삽입 정렬 정의
def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result


# 비효율 적인 insert_value 함수. 입력 배열을 순차적으로 스캔
def insert_value(array, value):
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)


# 위의 두 함수를 프로파일 하기 위해 난수 데이터를 생성
from random import randint

max_size = 10**4
data = [randint(0, max_size) for _ in range(max_size)]
test = lambda: insertion_sort(data)


# CProfile : 순수 python 프로파일보다 성능이 좋다. 프로그램에 미치는 영향을 최소화해준다.
from cProfile import Profile

profiler = Profile()
profiler.runcall(test)


# 테스트 실행
import sys
from pstats import Stats

stats = Stats(profiler)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
print('First Test')
stats.print_stats()

"""
항목의 의미
ncalls : 프로파일링을 수행하는 동안 함수 호출 횟수
tottime : 함수가 실행되는데 걸린 시간(초). 다른 함수를 호출하는데 걸린 시간은 제외
tottime percall : 함수를 호출하는데 걸린 평균 시간(초)
cumtime : 함수를 실행하는데 걸린 누적 시간(초). 다른 함수를 호출하는데 걸린 시간 포함
cumtime perclal : 함수를 실행하는데 걸린 평균 시간(초)
"""

# 46 내장 알고리즘 파트 참고
from bisect import bisect_left

def insert_value(array, value):
    i = bisect_left(array, value)
    array.insert(i, value)

profiler = Profile()
profiler.runcall(test)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
print('\nImproved Test')
stats.print_stats()


# 테스트용 함수 및 다른 두 함수에서 반복적으로 호출되는 함수를 정의
def my_utility(a, b):
    c = 1
    for i in range(100):
        c += a * b

def first_func():
    for _ in range(1000):
        my_utility(4, 5)

def second_func():
    for _ in range(10):
        my_utility(1, 3)

def my_program():
    for _ in range(20):
        first_func()
        second_func()


profiler = Profile()
profiler.runcall(my_program)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
print('함수 테스트')
stats.print_stats()


stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_callers() # 호출된 함수를 왼쪽에 보여주고, 누가 호출하는지를 오른쪽에 보여준다
