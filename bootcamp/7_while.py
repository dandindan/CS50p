import random

rand_num = random.randrange(1, 51)

i = 1

while i != rand_num:
    i += 1
    print("i =", i)
print("The random value is :", rand_num)

i = 1

while i <= 100:
    if (i % 2) == 0:
        i += 1
        continue
    
    if i == 99:
        break
    print("Odd:", i)
    i += 1

num_branch = input("enter the number of branches: ")
y=1
x=1

while x != num_branch:
    x+=1
    for y in range(1,num_branch):
        # print(" \t")
        print("#\t")
        y=y+2



