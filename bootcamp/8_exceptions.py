

while True:
    try:
    
        number =int(input("please enter a number from 1 to 10: "))
        break
        
    except ValueError:
        number =int(input("please enter a number from 1 to 10: "))
    except  :
        print ('EROR!')    

print('Thanks!')


while True:
    number =int(input("please enter a number from 1 to 10: "))
    if number ==7:
        print('corect')
        break

    


