

class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value


# 존재하지 않는 속성에 접근
print('LazyDB')
data = LazyDB()
print('before:', data.__dict__)
print('foo:', data.foo)
print('after:', data.__dict__)


# 로깅 추가
class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)

print('\n\nLoggingLazyDB')
data = LoggingLazyDB()
print('exists:', data.exists)
print('foo:   ', data.foo)
print('foo:   ', data.foo)


# 트랜잭션 처리를 할 때 접근하려는 데이터베이스의 로우가 유효한지 확인이 필요하다. 이런 경우엔 __getattribute__ 후크를 사용한다

class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value

print('\n\nValidatingDB')
data = ValidatingDB()
print('exists:', data.exists)
print('foo:   ', data.foo)
print('foo:   ', data.foo)


# 동적 접근으로 인한 프로퍼티가 존재하지 않아야 하는 경우도 있을 것이다
import logging

try:
    class MissingPropertyDB(object):
        def __getattr__(self, name):
            if name == 'bad_name':
                raise AttributeError('%s is missing' % name)
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value

    data = MissingPropertyDB()
    data.foo  # Test this works
    data.bad_name
except:
    logging.exception('Expected')
else:
    assert False


# __getattr__ 은 한 번만 호출
print('LoggingLazyDB')
data = LoggingLazyDB()
print('Before:     ', data.__dict__)
print('foo exists: ', hasattr(data, 'foo'))
print('After:      ', data.__dict__)
print('foo exists: ', hasattr(data, 'foo'))


# _getattribute__ 는 hasattr, getattr 호출 시마다 호출
print('ValidatingDB')
data = ValidatingDB()
print('foo exists: ', hasattr(data, 'foo'))
print('foo exists: ', hasattr(data, 'foo'))



# db log 로 데이터를 남길수도 있다
class SavingDB(object):
    def __setattr__(self, name, value):
        # Save some data to the DB log
        super().__setattr__(name, value)


class LoggingSavingDB(SavingDB):
    def __setattr__(self, name, value):
        print('Called __setattr__(%s, %r)' % (name, value))
        super().__setattr__(name, value)


print('LoggingSavingDB')
data = LoggingSavingDB()
print('Before: ', data.__dict__)
data.foo = 5
print('After:  ', data.__dict__)
data.foo = 7
print('Finally:', data.__dict__)


# 이런 방식의 문제점은 객체의 속성에 접근할때마다 호출된다는 점이다.

class BrokenDictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        return self._data[name]


# 무한 루프
# try:
#     data = BrokenDictionaryDB({'foo': 3})
#     data.foo
# except:
#     logging.exception('Expected')
# else:
#     assert False


"""
문제는 __getattribute__ 가 self.data 에 접근하면 __getattribute__ 가 다시 실행되고 다시 self.data 에 접근하기 때문이다
해결책은 인스턴스에서 super().__getattribute__ 로 인스턴스 속성 딕셔너리에서 값을 읽어오는 것이다
"""

class DictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

data = DictionaryDB({'foo': 3})
print(data.foo)



