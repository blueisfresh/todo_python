import json

def main():
    print("Hello, welcome to your todo App")
    username = input("What is your username? ")
    password = input("What is your password? ")
    if(username != "" or password != ""):
        read_todos()

def print_todo(data):
    # Print all todos
    for todo in data["todos"]:
        status = "✓" if todo["completed"] else "✗"
        print(f"{todo['id']}: {todo['title']} ({status}) - Due {todo['due_date']}")

def read_todos():
    # Reading Json Data from a file
    with open("todo.json", "r") as json_file:
        data = json.load(json_file)
        # print(data)
        print_todo(data)



# prevent python main script to be run when its being imported as a module
if __name__ == "__main__":
    main()