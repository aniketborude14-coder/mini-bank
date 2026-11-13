dict={
    "username": "aniket",
    "password": 1234,
    }
attempts = 0
while attempts < 3:
    username = input("Enter your username: ")
    password = int(input("Enter your password: "))
    if password == dict["password"] and username == dict["username"]:
        print("login successful")
        

    else:
         attempts += 1
         print(f"login failed try again, {3-attempts} attempts remaining")

else:
    print("Too many failed attempts. Access denied.")
    