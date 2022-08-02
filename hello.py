# https://www.youtube.com/watch?v=JP7ITIXGpHk&list=PLhQjrBD2T3817j24-GogXmWqO5Q5vYy0V&index=2

print("Hello World")
name = input("What is your name? ")
print("Hello " + name)
# remove the whitespace from the input
name = name.strip()
print("The length of your name is: " + str(len(name)))
print("Your name in uppercase is: " + name.upper())
print("Your name in lowercase is: " + name.lower())
print(f"Your name has {len(name)} characters")
