# https://docs.python.org/3.4/library/concurrent.futures.html


def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i

from time import time

numbers = [(1963309, 2265973), (2030677, 3814172),
           (1551645, 2229620), (2039045, 2020802)]

# 순서대로 실행하면 시간이 선형적으로 증가한다
start = time()
results = list(map(gcd, numbers))
end = time()
print('Took %.3f seconds. result=%s' % (end - start, results))


# 스레드풀을 시작하고 통신하는 오버헤드가 크가
from concurrent.futures import ThreadPoolExecutor

start = time()
pool = ThreadPoolExecutor(max_workers=2)
results = list(pool.map(gcd, numbers))
end = time()
print('Took %.3f seconds. result=%s' % (end - start, results))


# ProcessPoolExecutor 를 사용하자
from concurrent.futures import ProcessPoolExecutor

start = time()
pool = ProcessPoolExecutor(max_workers=2)
results = list(pool.map(gcd, numbers))
end = time()
print('Took %.3f seconds. result=%s' % (end - start, results))

"""
ProcessPoolExecutor 의 실제 작업

1. numbers 입력 데이터에서 map 으로 각 아이템을 가져옴
2. pickle 모듈을 사용하여 바이너르 데이터로 직렬화
3. 주 인터프리터 프로세스에서 직렬화한 데이터를 지역 소켓을 통해 자식 인터프리터 프로세스로 복사
4. 자식 프로세스에서 pickle 을 이용하여 데이터를 파이썬 객체로 역직렬화
5. gcd 함수가 들어있는 파이썬 모듈을 임포트
6. 다른 자식 프로세스를 사용하여 병렬로 입력 데이터에 함수를 실행한다
7. 결과를 다시 바이트로 직렬화
8. 소켓을 통해 바이트를 복사
9. 바이트를 부모 프로세스에 있는 파이썬 객체로 역직렬화
10. 마지막으로 여러 자식에 있는 결과를 반환용 리스트로 병합
"""


