# 알고리즘에 따라서 파이썬 내장 자료구조의 적절히 사용해보자

# double ended queue

from collections import deque
print('deque')

fifo = deque()
print(fifo)

fifo.append(1)      # Producer
print(fifo)

fifo.append(2)
print(fifo)

fifo.append(3)
print(fifo)

x = fifo.popleft()  # Consumer
print(x)


# ordered dictionary

# 먼저 일반 사전을 테스트
print('\ndict')

a = {}
a['foo'] = 1
a['bar'] = 2
from random import randint

# Randomly populate 'b' to cause hash conflicts
while True:
    z = randint(99, 1013)
    b = {}
    for i in range(z):
        b[i] = i
    b['foo'] = 1
    b['bar'] = 2
    for i in range(z):
        del b[i]
    if str(b) != str(a):
        break

print(a)
print(b)
print('Equal?', a == b)


print('\nOrderedDict')
from collections import OrderedDict
a = OrderedDict()
a['foo'] = 1
a['bar'] = 2

b = OrderedDict()
b['foo'] = 'red'
b['bar'] = 'blue'

for value1, value2 in enumerate(zip(a.values(), b.values())):
    print(value1, value2)


# default dictionary
print('\ndefault dictionary')

from collections import defaultdict
stats = defaultdict(int)
stats['my_counter'] += 1
print(dict(stats))
print(stats)


# heap queue : 우선순위 큐를 유지하는 자료구조. 아래와 같이 무작위로 아이템을 입력하더라도 우선순위가 가장 낮은것부터 제거된다
print('\nheap queue')

from heapq import *
a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 8)
heappush(a, 1)

print(heappop(a), heappop(a), heappop(a), heappop(a))


a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 8)
heappush(a, 1)

print(a[0])
print(nsmallest(1, a)[0])
assert a[0] == nsmallest(1, a)[0] == 1

print('Before:', a)
a.sort()
print('After: ', a)



# bisection
print('\nbisection')

x = list(range(10**6))
i = x.index(991234)
print(i)


# bisect_left 를 사용하면 정렬된 아이템 시퀀스를 대상으로 효율적인 바이너리 검색을 제공한다
from bisect import bisect_left
i = bisect_left(x, 991234)
print(i)


from timeit import timeit
print(timeit(
    'a.index(len(a)-1)',
    'a = list(range(100))',
    number=1000))
print(timeit(
    'bisect_left(a, len(a)-1)',
    'from bisect import bisect_left;'
    'a = list(range(10**6))',
    number=1000))



