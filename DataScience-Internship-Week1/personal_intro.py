def main():
    # Gathering info of user using input()
    print("Welcome! Please answer a few quick questions.\n")

    #creating variables and taking input
    name = input("What is your name? \n")
    age = int(input("How old are you? \n"))
    hobby = input("What is your favorite hobby? \n")

    # Displaying welcome message using f-strings
    print("\n" f"✨ Welcome {name}! ✨")
    print(f"You are {age} years old and love {hobby}.")

main()
