from random import randint
# range 를 사용한 iterate

random_bits = 0

for i in range(100):
    if randint(0, 1):
        random_bits |= 1 << i
        # print(random_bits)

# 문자열 테스트
flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
for flavor in flavor_list:
    print('%s is delicivous' % flavor)
print()

# 좋아하는 순위 출력은..
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print('%d: %s is delicivous' % (i+1, flavor))
print()

# enumerate 를 사용하면 좀 더 단순해진다
for i, flavor in enumerate(flavor_list, 1):
    print('%d: %s is delicivous' % (i, flavor))

