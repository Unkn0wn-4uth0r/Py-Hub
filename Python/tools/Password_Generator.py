import random

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'!@#$%^&*(){}[]:;.,~_-+/<>"

def generate():
    while True:
        length_input = input("What do you want the length of the password to be: ")
        if not length_input.isdigit():
            print(f"{length_input} is not a valid input. Please try again.")
        else:
            length = int(length_input)
            if length <= 0 or type(length) == float:
                print(f"{length} is not valid. Please enter a positive integer.")
            else:
                break #Exit the loop if valid input is entered.
    password = "".join(random.choice(chars) for _ in range(length))
    return password

if __name__ == "__main__":
    print("Your generated password is:", generate())
