# 0으로 나누는 경우에 대한 예외처리가 된 메소드. 목표하는 바는 0 으로 나누는 경우에 대한 예외처리이다
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(divide(10, 0))

# 분자가 0 인경우는..? 0 으로 출력
print(divide(0, 10))

# 반환값을 두개롤 나눠서 튜플에 담아보내자. 작업의 성공여부와 실제 결과가 그것이다
def divide_1(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None

success, result = divide_1(10, 0)
if not success:
    print('invalid input')

# 뭔가 코드가 더 복잡해진다. 더 좋은 방법은 호출하는 쪽에 예외를 일으키는 것이다
def divide_2(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('invalid input') from e

result = divide_2(0, 10)
print(result)

result = divide_2(10, 0)
print(result)



