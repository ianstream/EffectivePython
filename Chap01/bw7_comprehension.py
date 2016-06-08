# 리스트 컴프리헨션은 추가적인 람다 표현식이 필요어서 맵이나 필터를 사용하는 것 보다 명확하다
a = [1,2,3,4,5,6,7,8,9,10]
print(a)

squares = [x**2 for x in a]
print(squares)

squares_lamda = list(map(lambda x: x**2, a))
print(squares_lamda)

# 값을 걸러내는 예제
odd_square = [(x,x**2) for x in a if x % 2 == 1]
print(odd_square)

# 이걸 람다를 사용하면..
odd_square_lambda = list(map(lambda x: (x,x**2), filter(lambda x: x%2 == 1, a)))
print(odd_square_lambda)

#dict, set

chile_ranks = {'ghost': 1, 'habanero': 2, 'cayenne': 3}
rank_dict = {rank: name for name, rank in chile_ranks.items()}
chile_len_set = {len(name) for name in rank_dict.values()}
print(rank_dict)
print(chile_len_set)
