#학생 집단의 성적 기록 클래스
class SimpleGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)

    def print_grade(self, name):
        grades = self._grades[name]
        print(grades)

book = SimpleGradebook()
book.add_student('ian kim')
book.report_grade('ian kim', 80)
book.report_grade('ian kim', 85)
book.report_grade('ian kim', 92)

print(book.average_grade('ian kim'))


# 과목을 추가해보자

class BySubjectGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = {}

    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count

book = BySubjectGradebook()
book.add_student('ian kim')
book.report_grade('ian kim', 'Math', 80)
book.report_grade('ian kim', 'Math', 80)
book.report_grade('ian kim', 'Math', 70)
book.report_grade('ian kim', 'Gym', 100)
book.report_grade('ian kim', 'Gym', 85)

print(book.average_grade('ian kim'))


# 요구사항이 변경되었다. 특정 시험의 비중을 높이 평가해야한다

class WeightedGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = {}

    # 시험의 가중치를 입력받는다
    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append((score, weight))

    def average_grade(self, name):
        by_subject = self._grades[name]
        score_sum, score_count = 0, 0
        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0

            # 시험의 가중치를 계산에 적용한다
            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight
            score_sum += subject_avg / total_weight
            score_count += 1
        return score_sum / score_count

book = WeightedGradebook()
book.add_student('ian kim')
book.report_grade('ian kim', 'Math', 80, 0.10)
book.report_grade('ian kim', 'Math', 80, 0.10)
book.report_grade('ian kim', 'Math', 70, 0.80)
book.report_grade('ian kim', 'Gym', 100, 0.40)
book.report_grade('ian kim', 'Gym', 85, 0.60)

print(book.average_grade('ian kim'))


# 결과를 구할수는 있지만 성적 입력의 항목들이 직관적이지 않다
# 관리가 복잡해지는 즉시 클래스로 옮겨가야 한다. 이를 통해 데이터를 더 잘 정의된 인터페이스를 통해 제공할 수 있게 된다
# 인터페이스와 실제 구현 사이에 추상화 계층도 만들 수 있다

# 성적 기록은 score, weight 튜플을 이용
print("*** 클래스 리팩토링 1 ***")

grades = []
grades.append((95, 0.45))
grades.append((85, 0.55))

total = sum(score * weight for score, weight in grades)
total_weight = sum(weight for _, weight in grades)
average_grade = total / total_weight
print(average_grade)


# 각 시험별 의견을 입력해야 한다면..
print("*** 클래스 리팩토링 2 ***")

grades = []
grades.append((95, 0.45, '참잘했어요'))
grades.append((85, 0.55, '다음에 더 잘할거에요'))

total = sum(score * weight for score, weight, _ in grades)
total_weight = sum(weight for _, weight, _ in grades)
average_grade = total / total_weight
print(average_grade)


# 튜플을 길게 확장하는 패턴은 이전에 딕셔너리의 패턴과 비슷하다.
# collections 모듈의 namedtuple 타입을 사용해보자
# 단, 기본인수 값을 설정해야 하는 경우, 외부 API 에 노출되는 경우 나중에 변경이 어려울 수 있으니 이런 경우엔 클래스 정의가 더 나은 선택이다

print("*** 클래스 리팩토링 3 ***")

import collections
Grade = collections.namedtuple('Grade', ('score', 'weight'))


class Subject(object):
    def __init__(self):
        self._grade = []

    def report_grade(self, score, weight):
        self._grade.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grade:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student(object):
    def __init__(self):
        self._subjects = {}

    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


class Gradebook(object):
    def __init__(self):
        self._students = {}

    def student(self, name):
        if name not in self._students:
            self._students[name] = Student()
        return self._students[name]


book = Gradebook()
albert = book.student('ian kim')
math = albert.subject('Math')
math.report_grade(80, 0.10)
math.report_grade(80, 0.10)
math.report_grade(70, 0.80)
gym = albert.subject('Gym')
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)

print(albert.average_grade())


