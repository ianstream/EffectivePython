from random import randint

random_bits = 0

f = open('rand.txt', 'w')

for i in range(1000):
    rand = randint(1, 100)
    # print(rand)
    f.write(str(rand) + '\n')

f.close()