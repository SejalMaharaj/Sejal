
num1 = int(input("Enter the first integer number: "))

#Check if the first number is greater than 0
if num1 > 0:

    num2 = int(input("Enter the second integer number: "))

    #Check if the second number is greater than 1
    if num2 > 1:
        #Calculate num1 raised to the power of num2 
        result = 1
        for i in range(num2):
            result *= num1

        #Display the result
        print(f"{num1} to the power of {num2} is {result}")
    else:
        print("The second number must be greater than 1.")
else:
    print("The first number must be greater than 0.")
