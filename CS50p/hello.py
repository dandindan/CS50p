# https://www.youtube.com/watch?v=JP7ITIXGpHk&list=PLhQjrBD2T3817j24-GogXmWqO5Q5vYy0V&index=2

print("Hello World")
name = input("What is your name? ").strip().title()
print("Hello " + name)
# remove the whitespace from the input
name = name.strip()
first, last = name.split(" ")
print("The length of your name is: " + str(len(name)))
print("Your name in uppercase is: " + name.upper())
print("Your name in lowercase is: " + name.lower())
print(f"Your name has {len(name)} characters")
print(f"Your first name is: {first}")
print(f"Your last name is: {last}")
print(f"Your name in reverse is: {last[::-1]} + {first[::-1]}")


def hello():
    print("Hello World")
