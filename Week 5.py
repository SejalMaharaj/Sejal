with open("diary.txt.", "w") as f:
    f.write("Dear Diary, Python ate my homework.\n")


#Activity 1 create a movies.txt file with top 3 films
movies = ["star wars", "Gossip girl", "The notebook"]
with open("movies.txt", "w") as f:
    for movies in movies:
        f.write(movies + "\n")

#Activity 2
with open("secret.txt", "r") as f:
    for line in f.readlines():
        message = line.split("-")
        secret_line = ""
        for code in message:
            secret_line = secret_line + chr(int(code))
        print(secret_line)

#Activity 3
student = {
    "name": "Bob",
    "age": 21,
}
student["age"] = 100
print(student["age"])

#3.1
student = {
    "name": "Bob",
    "age": 21,
}
print(student.values())

import pandas as pd

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [21, 30, 35],
    "City":["NY", "LA", "Chicago"]
}
df = pd.DataFrame(data)
print(df[["Name", "Age"]])

print("Activity 4.2")
df["Under_30"] = df["Age"] > 30
print(df)

print("Activity 4.3")
print(df.iloc[1])

print("Activity 5")
data = {
    "Name": [ "Alice", "Bob", "Charlie", "David", "Eva"],
    "Age": [25, 32, 45, 28, 35],
    "Country": ["USA", "Canada", "UK", "Australia", "Germany"]
}
df = pd.DataFrame(data)
print(df[["Name", "Age", "Country"]])

print("Add a column")
df["Salary"] = [50000, 600000, 200000, 100000, 450000]
print(df)
print()

print("Rows where Age > 30")
print(df[df"Age"]>30])

print(df["Salary"])

