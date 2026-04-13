def main():
    # Gather user information using input()
    print("Welcome! Please answer a few quick questions.\n")
    
    name = input("What is your name? ")
    age = input("How old are you? ")
    hobby = input("What is your favorite hobby? ")

    # Display the personalized, friendly welcome message using f-strings
    print("\n" + "="*30)
    print(f"🎉 Welcome {name}! 🎉")
    print(f"You are {age} years old and love {hobby}.")
    print("="*30 + "\n")

if __name__ == "__main__":
    main()
