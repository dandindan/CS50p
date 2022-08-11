def main():
    x = int(input("Enter a number: "))
    print(f"number squared is", square(x))


def square(n):
    return pow(n, 2)


main()
