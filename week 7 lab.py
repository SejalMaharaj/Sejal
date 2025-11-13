#ex 5
print("ex 5:")
number = input("Enter a five-digit number: ")

#Check if the input has exactly 5 digits
if len(number) == 5 and number.isdigit():
    add_sum = 0
    subtract_sum = 0

    #Loop through each digit using its index
    for i in range(len(number)):
        digit = int(number[i])


        if i == 0 or i == 2 or i == 4:
            add_sum += digit
        # If index is 1 or 3 (2nd, 4th digits), subtract them
        elif i == 1 or i == 3:
            subtract_sum += digit

    #Calculate the final result
    result = add_sum - subtract_sum

    #output
    print(f"The final total is = {result}")

else:
    print("Please enter exactly five digits.")



