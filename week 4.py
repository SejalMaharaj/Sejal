#first task
def is_valid_password(password):
    if len(password) < 8:
        return False
    else:
        has_upper = False
        has_lower = False
        has_number = False
        has_symbol = False

        for char in password:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_number = True
            elif is_symbol(char):
                has_symbol = True

    return has_upper and has_lower and has_number and has_symbol

def is_symbol(char):
    code = ord(char)

    if (65 <= code <= 90) or (97 <= code <= 122):
        return False
    else:
        return True

print(is_valid_password("P@sSW123Ords"))

#2nd task
try:
  number = int(input("Enter a number: "))
  print(10/number)
except ZeroDivisionError:
    print("Enter > 0")
except:
    print("ERROR")

#3rd task
while True:
  try:
    num = int(input("Enter a number: "))
    print(f"Thank you? You entered {num}.")
    break
  except ValueError:
    print("Enter a number")



