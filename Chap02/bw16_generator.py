# 문자열에 있는 모든 단어의 인덱스를 출력하고자 한다면..

def index_work(text):
    result= []
    if text:
        result.append(0)

    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)

    return result

# 결과를 리스트로 받아오므로 값이 매우 큰 경우엔 문제가 될 수 있다
address = '서울시 양천구 신월7동 xx번지 1가'
result = index_work(address)
print(result)


# 위와 동일한 작업을 하는 함수, 제너레이터를 사용한다

def index_work_iter(text):
    if text:
        yield 0

    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1

result = index_work_iter(address)
# 캐스팅이 필요하다
print(list(result))


# 파일처리를 한다면..

def index_file(handle):
    offset = 0

    for line in handle:
        if line:
            yield offset

        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset


f = open('../Chap01/20130627085052.html', 'r')
it = index_file(f)
result = list(it)[0:5] # 제러네이터를 리스트로 바꾸고 원하는 만큼 잘라낸다
print(list(result))

# 제너레이터를 정의 후 사용할때 주의점은 반환되는 이터레이터에 상태가 있고 재사용할수 없다는 것이다. 아래의 이러테리터 참고
# http://anandology.com/python-practice-book/iterators.html





