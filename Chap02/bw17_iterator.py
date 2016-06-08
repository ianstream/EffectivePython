# 다음과 같은 정규화 함수가 있다고 해보자
def normalize(numbers):
    total = sum(numbers)
    result = []

    for value in numbers:
        percent = 100 * value / total
        result.append(percent)

    return result

visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)


# 파일에서 읽어야 한다고 하면..
def read_visits(file_path):
    with open(file_path) as f:
        for line in f:
            yield int(line)

it = read_visits('rand.txt')
percentages = normalize(it)
# 놀랍다! 아무것도 안나옴
print(percentages)


it = read_visits('rand.txt')
print(list(it))
# iterator 가 소진되기 대문
print(list(it))



# 입력 이터레이터를 방어적으로 복사해보자

def normalize_copy(numbers):
    numbers = list(numbers)
    total = sum(numbers)
    result = []

    for value in numbers:
        percent = 100 * value / total
        result.append(percent)

    return result

it = read_visits('rand.txt')
percentages = normalize_copy(it)
print(percentages)

# 역시 다른 예제와 동일한 문제가 있다. 입력값이 메모리 공간보다 크다면 어떻게 할 것인가?
# 호출될 때마다 새로운 이터레이터를 반환해보자

def normalize_func(numbers):
    total = sum(numbers())
    result = []

    for value in numbers():
        percent = 100 * value / total
        result.append(percent)

    return result

percentages = normalize_func(lambda: read_visits('rand.txt'))
print(percentages)

# 이보다 더 좋은 방법은 이터레이터 프로토콜을 구현한 새 컨테이너 클래스를 만드는 것이다

class ReadVisits(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def __iter__(self):
        with open(self.file_path) as f:
            for line in f:
                yield int(line)

visits = ReadVisits('rand.txt')
percentages = normalize(visits)
print(percentages)

# 이 코드가 동작하는 이유 : normalize 의 sum 이 ReadVisits 의 __iter__ 를 호출한다. debug 모드로 확인해보자
# 단점은? 호출되는 횟수만큼 읽어들인다


# 마지막으로 이터레이터 프로토콜을 다르는 컨테이너를 허용하는 함수를 만드자.
# 이 함수는 입력데이터를 여러번 순회시 좋다

def normalize_defensive(numbers):
    if iter(numbers) is iter(numbers):
        raise TypeError('컨테이너만 지원합니다')

    total = sum(numbers)
    result = []

    for value in numbers:
        percent = 100 * value / total
        result.append(percent)

    return result

visits = [15, 35, 80]
percentages = normalize_defensive(visits)
print(percentages)

visits = ReadVisits('rand.txt')
percentages = normalize_defensive(visits)
print(percentages)

it = iter(visits)
percentages = normalize_defensive(it) # 예외처리됨
print(percentages)

