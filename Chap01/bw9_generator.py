# 컴프리헨션을 사용해서 파일의 내용과 각 라인의 길이를 읽어온다
len_value = [len(x) for x in open('20130627085052.html')]
value = [x for x in open('20130627085052.html')]

print(len_value)
print(value)

# 위의 방식은 파일을 한번에 다 읽어오기 때문에 네트워 장애, 파일오류, 메모리 부족 등에 취약하다
# 제너레이터를 사용해보자. 단, 제너레이터 표현식에서 반환된 이터레이터는 한번넘게 사용하지 않도로 주의하자

def print_data(value_it):
    while True:
        try:
            print(next(value_it))
        except StopIteration:
            break

len_it = (len(x) for x in open('20130627085052.html'))
data_it = (x for x in open('20130627085052.html'))
# 제너레이터 오브젝트가 출력됨
print(len_it)
print(data_it)

print_data(len_it)
print_data(data_it)


# 다시 사용은 안된다!
print(next(len_it))

