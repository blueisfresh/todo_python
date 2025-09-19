import json

def main():
    print("Hello, welcome to your todo App")
    username = input("What is your username?")
    if(username):
        read_todos(username)

def print_todo(data):
    print("\nThese are all of your todos:\n")
    print(f"{'ID':<5} {'Title':<20} {'Status':<8} {'Due Date'}") # left-align text into columns of fixed width.
    print("-" * 50)

    for todo in data:
        status = "✓" if todo["completed"] else "✗"
        print(
            f"{todo['id']:<5} {todo['title']:<20} ({status:<8}) {todo['due_date']}"
        )

def read_todos(arg_username):
    # Reading Json Data from a file
    with open("todo.json", "r") as json_file:
        # Transform json input to python objects
        input_dict = json.load(json_file)

        # Grab the todos list first
        todos = input_dict["todos"]

        # Filter the todos for the given username
        output_dict = [todo for todo in todos if str(todo["user"]) == arg_username]

        if output_dict:
            data = output_dict

            # print(data)
            print_todo(data)
        else :
            # Transform python object back into json
            output_json = json.dumps(output_dict)

            # Show json
            print(output_json)


# prevent python main script to be run when its being imported as a module
if __name__ == "__main__":
    main()