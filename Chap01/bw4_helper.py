from urllib.parse import parse_qs



def print_value(my_value=None):
    # 복잡한 표현식은 헬퍼 함수로 분리한다. 파이썬 문법을 사용해 None 데이터를 효율적으로 변환해준다
    print(repr(my_value))

    print('source:' , my_value.get('source', [''])[0] or '')
    print('target:' , my_value.get('target', [''])[0] or '')
    print('comment:' , my_value.get('comment', [''])[0] or '')

    print('\n')


def print_value_improved(my_value=None):
    # 삼항식을 사용
    print(repr(my_value))

    source = my_value.get('source', [''])
    target = my_value.get('target', [''])
    comment = my_value.get('comment', [''])
    print('source:' , source[0] if source[0] else '')
    print('target:' , target[0] if target[0] else '')
    print('comment:' , comment[0] if comment[0] else '')

    print('\n')


my_value = parse_qs('source=naver&target=loan_people_category_1&comment=\'당신에게 더 나은 대출 상품을 추천합니다\'')
print_value(my_value)

my_value2 = parse_qs('source=&target=loan_people_category_1&comment=\'당신에게 더 나은 대출 상품을 추천합니다\'')
print_value_improved(my_value2)
