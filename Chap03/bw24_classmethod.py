#  파이썬은 클랙스도 다형성을 지원한다


# 입력을 표현할 공통 클래스
class InputData(object):
    def read(self):
        raise NotImplementedError


# 데이터를 읽어오도록 구현한 InputData 의 서브 클래스
class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()


# 입력 데이터 처리를 위한 맵리듀스 작업 추상 클래스
class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


# 맵리듀스 서브클래스
class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


# 연결은 어떻게?
# 디렉토리의 내용을 나열하고 각파일로 PathInputData 인스턴스를 생성

import os


def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


from threading import Thread

# 결과를 하나로 합치자
def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


# 맵리듀스 함수에서 모두 연결
def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)


# 동작 확인
from tempfile import TemporaryDirectory
import random

def write_test_files(tmpdir):
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(0, 100))

with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    result = mapreduce(tmpdir)

print('There are', result, 'lines')


# 문제는 맵리듀스 함수가 범용적이지 않다는 것

class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    """
    다른 언어에서는 범용성을 생성자 다형성으로 해결한다
    파이썬에서는 단일 생성자 메서드 __init__ 만 지원하므로 InputData 서브 클래스가 호환이 되는 생성자를 갖춰야한다는 결론이 나오는데..
    이를 해결하는 좋은 방법은 @classmethod 다형성을 사용하는 것이다
    http://egloos.zum.com/mcchae/v/11031012
    https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods
    """
    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData(GenericInputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


# 맵리듀스 함수의 범용성 적용 작성
def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    config = {'data_dir': tmpdir}
    result = mapreduce(LineCountWorker, PathInputData, config)
print('There are', result, 'lines')



