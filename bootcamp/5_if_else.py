age = int(input("Enter your Age: "))

if age < 5:
    print("too young")

elif age == 5:
    print("go to kindergarten")    
   
elif (age > 6) and (age < 17):
    print(" go to grade {}".format(age))
    print(f'go to grade {age} or {age+2}')#f string

else  :
    print ("goto college") 

can_vote = True if age >= 18 else False

print("you can vote:",can_vote)
