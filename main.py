import json
from pynput.keyboard import Key, Listener
from simple_term_menu import TerminalMenu

quitProgram = False
key_strokes_should_be_logged = False
username = None


def main():
    global username
    global quitProgram

    options = ["Show todos", "Add Todo", "Quit"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    if username:
        choice = options[menu_entry_index]

        if choice == "Show todos":
            read_todos(username)
        elif choice == "Add Todo":
            print("TODO: implement add_todo()")
        elif choice == "Quit":
            quitProgram = True

    print(f"\nYou have selected {options[menu_entry_index]}!\n")


def signup():
    global username

    print("Hello, welcome to your todo App")
    username = input("What is your username? ")


def print_todo(data):
    print("\nThese are all of your todos:\n")

    # define column width explicitly
    col_id = 5
    col_title = 30
    col_status = 6
    col_due = 12

    # header
    print(f"{'ID':<{col_id}} {'Title':<{col_title}} {'Status':<{col_status}} {'Due Date':<{col_due}}")
    print("-" * (col_id + col_title + col_status + col_due + 3))  # +3 for spaces

    # rows
    for todo in data:
        status = "✓" if todo["completed"] else "✗"
        print(
            f"{todo['id']:<{col_id}} {todo['title']:<{col_title}} {status:<{col_status}} {todo['due_date']:<{col_due}}"
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
            # print data from json
            print_todo(output_dict)
        else:
            # Transform python object back into json & Show the json
            print(json.dumps(output_dict))


# prevent python main script to be run when its being imported as a module
if __name__ == "__main__":
    # Asking for Username
    signup()

    while not quitProgram:
        main()
