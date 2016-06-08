# 부모 클래스를 초기화하는 방법 : __init__ 사용할 때
class MyBaseClass(object):
    def __init__(self, value):
        self.value = value


class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)

    def times_two(self):
        return self.value * 2

foo = MyChildClass()
print(foo.times_two())


# 클래스가 다중상속의 영향을 받는다면 위의 방법은 오동작을 일으킬 수 있다

# 1. __init__ 의 호출 순서가 모든 서브클래스에 걸쳐 명시되어 있지 않다는 것
class TimeTwo(object):
    def __init__(self):
        self.value *= 2


class PlusFive(object):
    def __init__(self):
        self.value += 5


class OneWay(MyBaseClass, TimeTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimeTwo.__init__(self)
        PlusFive.__init__(self)


foo = OneWay(5)
print('(5 * 2) + 5 = ', foo.value)


# 다른 순서로 정의, 그러나 호출은 이전 클래스와 같음. 디버그 모드로 확인
class AnotherWay(MyBaseClass, PlusFive, TimeTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimeTwo.__init__(self)
        PlusFive.__init__(self)


# Example 6
bar = AnotherWay(5)
print('AnotherWay ', bar.value)


# 이 두 클래스 모두에서 상속받는 자식 클래스

class TimesFive(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5


class PlusTwo(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2


class ThisWay(TimesFive, PlusTwo):
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value)

foo = ThisWay(5)
print('Should be (5 * 5) + 2 = 27 but is', foo.value)


"""
기대한 값과 다른 이유는 self.value 로 다시 5로 초기화되기 때문이다
파이썬 3에서는 super 를 인수없이 호출하면 __class__ 와 self 를 인수로 넘겨서 호출되므로 위의 문제가 해결된다
"""


class Explict(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value * 2)


class Implict(MyBaseClass):
    def __init__(self, value):
        super().__init__(value * 2)

assert Explict(10).value == Implict(10).value
