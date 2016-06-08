# 클로저 테스트를 위한 함수

def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)

# group 순서는 결과에 상관없다
group1 = {2, 5, 7, 3}
sort_priority(numbers, group1)
print(numbers)


# 우선순위에 속하는 값을 찾았는지 여부를 반환하는 코드를 추가해보자

def sort_priority2(values, group):
    found = False
    def helper(x):
        if x in group:
            found = True # 동작할까?
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found

found = sort_priority2(numbers, group)
print('found:', found)
print(numbers)


"""
foudn = False 인 이유는 스코프 때문이다

파이썬의 스포크 참조 순서는..

1. 현재 함수의 스코프
2. 현재 함수를 감싸고 있는 스코프. 위에서는 sort_priority2
3. 코드를 포함하는 모듈 전체. 여기선 bw15_closure
4. 내장 스코프

파이썬3 에는 nonlocal 문법이 있는데 2번까지의 탐색을 지원한다

"""

def sort_priority3(values, group):
    found = False
    def helper(x):
        nonlocal found
        if x in group:
            found = True # 동작할까?
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found

found = sort_priority3(numbers, group)
print('found:', found)
print(numbers)


# 위의 방법보다는 아래의 방법을 더 추천한다. 이해하기 더 쉽다

class Sorter(object):
    def __init__(self, gorup):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

sorter = Sorter(group)
numbers.sort(key=sorter)
print(numbers)
print(sorter.found)
assert sorter.found is True








