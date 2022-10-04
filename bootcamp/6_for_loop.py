for i in range(1, 21):
    if (i % 2) != 0:
        print("i=", i)

your_float = input("Enter your float: ")
your_float = float(your_float)
print("Rounded to 2 Decimals : {:.2f}".format(your_float))

invesment, intererst_rate = input("Enter your invesment and your intrest rate:").split()
# the .split() function slits user input based on white spaces
invesment = int(invesment)
intererst_rate = float(intererst_rate) *.01
for i in range(1, 11):
    invesment += invesment*intererst_rate
    print("the invesmet after {} years is".format(i), invesment)

