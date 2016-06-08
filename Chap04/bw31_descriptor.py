# 파이썬 @property 의 가장 큰 단점은 재사용성이다. 즉, @property 로 데코레이흐나느 메서드를 같은 클래스에 속한 여러 속성에 사용하지 못한다

class Homework(object):
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._grade = value


galileo = Homework()
galileo.grade = 95
print(galileo.grade)


# 과목이 여러개라고 해보자

class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')

    # 항목이 늘어날 때마다 코드가 추가된다
    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value


galileo = Exam()
galileo.writing_grade = 85
galileo.math_grade = 99
print('Writing: %5r' % galileo.writing_grade)
print('Math:    %5r' % galileo.math_grade)



# 이제 디스크립터를 사용해보자. 이를 통해 클래스의 서로 다른 속성에 같은 로직을 재사용할 수 있다

class Grade(object):
    def __get__(*args, **kwargs):
        print('Grade.__get__')
        pass

    def __set__(*args, **kwargs):
        print('Grade.__set__')
        pass

class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

# 프로퍼티 할당
exam = Exam()
exam.writing_grade = 40


# 위의 동작을 바탕으로 Grade descriptor 를 구현해보자

class Grade(object):
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value


class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


print('Grade descriptor')
first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('Writing', first_exam.writing_grade)
print('Science', first_exam.science_grade)

second_exam = Exam()
second_exam.writing_grade = 75
print('Second', second_exam.writing_grade, 'is right')
print('First ', first_exam.writing_grade, 'is wrong')

# 문제가 발생했다. 하나의 Grade 인스턴스가 모든 Exam 인스턴스의 writing_grade 클래스 속성으로 공유된다

class Grade(object):
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value

"""
위의 딕셔너리로 구현한 코드는 잘 동작하지만 문제가 있다.
_value 딕셔너리는 __set__ 에 전달된 모든 exam 인스턴스의 참조를 저장한다. 결국 참조개수가 0이 되지 않아 가비지 컬렉터가 정리하지 못하게 된다
내장모듈 weakref 를 사용하자

장점은 아래와 같다.

Entries in the dictionary will be discarded when there is no
longer a strong reference to the key. This can be used to
associate additional data with an object owned by other parts of
an application without adding attributes to those objects. This
can be especially useful with objects that override attribute
accesses.
"""

from weakref import WeakKeyDictionary


class Grade(object):
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None: return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value


class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


print('WeakKeyDictionary use')
first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print('First ', first_exam.writing_grade, 'is right')
print('Second', second_exam.writing_grade, 'is right')




