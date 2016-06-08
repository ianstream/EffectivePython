# 다음과 같이 서로 연관있는 두개의 리스트가 있다고하자
names = ['ian Kim', 'minji', 'eunji', 'chanil']
letters = [len(n) for n in names]

# 두 리스트를 병렬로 순회하면서 가장 긴 이름을 찾으려면..
longest_name = None
max_letters = 0

for i in range(len(names)):
    count = letters[i]
    if count > max_letters:
        longest_name = names[i]
        max_letters = count

print('가장 긴 이름 : %s, 글자수 : %s' % (longest_name, max_letters))


# enumerate 를 사용한 예제
for i, name in enumerate(names):
    count = letters[i]
    if count > max_letters:
        longest_name = name
        max_letters = count

print('가장 긴 이름 : %s, 글자수 : %s' % (longest_name, max_letters))


# zip
for name, count in zip(names, letters):
    if count > max_letters:
        longest_name = name
        max_letters = count

print('가장 긴 이름 : %s, 글자수 : %s' % (longest_name, max_letters))

"""
이 방법이 문제가 아예 없는것은 아니다.
먼저 zip 은 모든 튜플을 반환한다. 메모리를 많이 사용하게 되는 경우에는 문제가 될 수 있다
입력된 이터레이터들의 길이가 다르면 이상하게 동작한다
"""

names.append('Ryuichi Sakamoto')

for name, count in zip(names, letters):
    print(name)

# 아래 라이브러리를 사용하면 이를 회피할 수 있다
from itertools import zip_longest

for name, count in zip_longest(names, letters):
    print(name, count)
