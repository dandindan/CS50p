
num_branch = int(input("enter the number of branches: "))
spaces = num_branch-1
hashes = 1
stump_spaces = num_branch -1


while  num_branch != 0:
    for i in range(spaces):
        print(' ', end='')
    for i in range(hashes):
        print('#', end='')
    print()
    spaces -=1
    hashes +=2
    num_branch -=1
for i in range(stump_spaces):
    print(" ",end='')
print("#")


