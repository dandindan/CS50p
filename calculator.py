x = float(input("Enter a number: "))
y = float(input("Enter another number: "))
z = round(x+y)  # round() rounds to the nearest integer

print(f"{x} + {y} = {x + y}")  # f-string
print(f"{z:,}")  # comma formatting
print(f"{z: ,.2f}")  # comma formatting with 2 decimal places
