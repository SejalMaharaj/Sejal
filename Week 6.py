import bcrypt
password ="Letmein"
password_bytes = password.encode("utf-8")

salt = bcrypt.gensalt(rounds=10) #waiting time in seconds
print (salt)

hashed_password = bcrypt.hashpw(password_bytes, salt)

print("plaintext: ", password)
print("hashed: ", hashed_password)

user_input = input("Enter a password").encode("utf-8")

if bcrypt.checkpw(user_input, hashed_password):
    print("Access is granted")
else:
    print("Access is denied")

