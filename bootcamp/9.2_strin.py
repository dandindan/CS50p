string_name = input('Enter a string: ')
codex = ""
for strx in string_name:
    codex += str(ord(strx))+" "
    print(strx, " ", end='')
print()
print(codex)

converted_string = ''
for i in range(0, len(codex)-1, 2):
    char_code=codex[i]+codex[i+1]
    converted_string+=char_code
print(converted_string)
