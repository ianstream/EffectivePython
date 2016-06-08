
import logging
from pprint import pprint
from sys import stdout as STDOUT


# 함수에 올바르지 않은 파라미터가 온 경우 아래와 같이 에외처리를 한다고 해보자
try:
    def determine_weight(volume, density):
        if density <= 0:
            raise ValueError('Density must be positive')

    determine_weight(1, 0)
except:
    logging.exception('Expected')
    print('Expected')
else:
    assert False

# api 용을 위해서는 자신만의 예외를 선언하는 것이 더 강력하다. 이를 위해 모듈 내에서 루트 exception 을 정의한다

# my_module.py
class Error(Exception):
    """Base-class for all exceptions raised by this module."""

class InvalidDensityError(Error):
    """There was a problem with a provided density value."""


class my_module(object):
    Error = Error
    InvalidDensityError = InvalidDensityError

    @staticmethod
    def determine_weight(volume, density):
        if density <= 0:
            raise InvalidDensityError('Density must be positive')


# api 사용자가 아래와 같이 호출할 수 있다

try:
    weight = my_module.determine_weight(1, -1)
    assert False
except my_module.Error as e:
    logging.error('Unexpected error: %s', e)
    print('Unexpected error: %s', e)

# 그러나 위와 같은 코드는 api 자체의 에러를 특징지어 잡지는 못한다
weight = 5
try:
    weight = my_module.determine_weight(1, -1)
    assert False
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error as e:
    logging.error('Bug in the calling code: %s', e)
    print('Bug in the calling code: %s', e)

assert weight == 0


# 루트 예외가 있어서 호출자가 api 사용 시 발생 가능한 문제점을 인지할 수 있다
# 또한 api 내부의 버그를 찾는데 도우이 된다.
weight = 5
try:
    weight = my_module.determine_weight(1, -1)
    assert False
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error as e:
    logging.error('Bug in the calling code: %s', e)
    print('Bug in the calling code: %s', e)
except Exception as e:
    logging.error('Bug in the API code: %s', e)
    print('Bug in the API code: %s', e)
    raise

assert weight == 0


# my_module.py
class NegativeDensityError(InvalidDensityError):
    """A provided density value was negative."""

def determine_weight(volume, density):
    if density < 0:
        raise NegativeDensityError


# 위와 같이 예외가 추가된 이후에도 사용자가 새 예외를 특별한 경우로 별도 처리할수도 있다
try:
    my_module.NegativeDensityError = NegativeDensityError
    my_module.determine_weight = determine_weight
    try:
        weight = my_module.determine_weight(1, -1)
        assert False
    except my_module.NegativeDensityError as e:
        raise ValueError('Must supply non-negative density') from e
    except my_module.InvalidDensityError:
        weight = 0
    except my_module.Error as e:
        logging.error('Bug in the calling code: %s', e)
        print('Bug in the calling code: %s', e)
    except Exception as e:
        logging.error('Bug in the API code: %s', e)
        print('Bug in the API code: %s', e)
        raise
except:
    logging.exception('Expected')
else:
    assert False


# my_module.py
class WeightError(Error):
    """Base-class for weight calculation errors."""

class VolumeError(Error):
    """Base-class for volume calculation errors."""

class DensityError(Error):
    """Base-class for density calculation errors."""

