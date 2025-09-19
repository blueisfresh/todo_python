import json

def main():
    print("Hello, welcome to your todo App")
    username = input("What is your username? ")
    password = input("What is your password? ")

# prevent python main script to be run when its being imported as a module
if __name__ == "__main__":
    main()