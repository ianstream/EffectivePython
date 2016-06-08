# 정밀도가 중요한 경우는 decimal type 으로 연산을 한다

rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print('일반연산:', cost)


print('일반연산 round:', round(cost, 2))


rate = 0.05
seconds = 5
cost = rate * seconds / 60
print('일반연산:', cost)


print('일반연산 round:', round(cost, 2))


from decimal import Decimal
from decimal import ROUND_UP
rate = Decimal('1.45')
seconds = Decimal(3*60 + 42)  # 3*60 + 42
cost = rate * seconds / Decimal('60')
print(cost)


rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)


rate = Decimal('0.05')
seconds = Decimal('5')
cost = rate * seconds / Decimal('60')
print(cost)


rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)
