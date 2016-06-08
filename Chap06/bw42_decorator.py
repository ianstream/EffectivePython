# 함수를 호출할 떄 인수와 반환값을 출력하는 데코레이터를 만든다고 해보자


def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' % (func.__name__, args, kwargs, result))
        return result
    return wrapper


@trace
def fibonacci(n):
    if n in (0, 1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))


# 결과가 잘 나오지만 반환값의 이름이 fibonacci 가 아니다
fibonacci(3)

print(fibonacci)

help(fibonacci)


"""
trace 함수는 그 안에 정의된 wrapper 를 반환한다. 이 함수가 데코레이터를 호출한 후 해당 호출을 담고 있는 모듈의 fibonacci 라는 이름에 할당이 된다
관련 동작은 57번 참고

해결책은 내장 모듈 functools 의 wraps 헬퍼 함수를 사용하는 것이다. 이를 사용하면 내부 함수에 있는 중요한 메타데이터가 모두 외부함수로 복사된다
"""

from functools import wraps

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' %
              (func.__name__, args, kwargs, result))
        return result
    return wrapper

@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) +
            fibonacci(n - 1))

print('\n\n')
fibonacci(3)

print(fibonacci)

help(fibonacci)

# 파이썬 함수에는 여러 표준 속성들이 있다. 함수들의 인터페이스를 유지하려면 이 속성들을 보호해야하며 wrap 을 사용하면 올바른 동작을 얻을 수 있다

