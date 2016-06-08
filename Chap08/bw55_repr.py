# 일반적으로 문자열은 아래와 같이 한다
print('foo bar')
print('%s' % 'foo bar')


# 그러나 아래와 같다면 어떨까?
print(5)
print('5')


# 내장함수 repr 은 객체의 출력 가능한 표현을 반환한다. 아래를 참고해보자
a = '\x07'
print(repr(a))


# 위의 갓을 eval 에 전달하녀 원래 파이썬 객체와 동일하게 나와야 한다
b = eval(repr(a))
assert a == b


# repr 을 사용하면 타입의 차이를 확인할 수 있다
print(repr(5))
print(repr('5'))


print('%r' % 5)
print('%r' % '5')


# 클래스의 출력 결과는 eval 함수로 넘기지 못한다
class OpaqueClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj = OpaqueClass(1, 2)
print(obj)


# 클래스용으로 __repr__ 을 정의해서 사용해보자
class BetterClass(object):
    def __init__(self, x, y):
        self.x = 1
        self.y = 2
    def __repr__(self):
        return 'BetterClass(%d, %d)' % (self.x, self.y)


obj = BetterClass(1, 2)
print(obj)


# 위와 같이 클래스를 제어할 수 없을 경우에는 __dict__ 를 사용하면 된다
obj = OpaqueClass(4, 5)
print(obj.__dict__)