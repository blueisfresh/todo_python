import json
from pynput.keyboard import Key, Listener

quitProgram = False
key_strokes_should_be_logged = False
username = None

def main():
    global username

    if username:
        read_todos(username)

def signup():
    global username

    print("Hello, welcome to your todo App")
    username = input("What is your username? ")


def on_press(key):
    global quitProgram
    if key_strokes_should_be_logged:
        print('{0} pressed'.format(key))

        # TODO: if command esc then quit Program

        # quit program on ESC
        if key == Key.esc:
            quitProgram = True
            return False  # stop listener

def on_release(key):
    if key_strokes_should_be_logged:
        print('{0} release'.format(key))

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
        else :
            # Transform python object back into json & Show the json
            print(json.dumps(output_dict))


# prevent python main script to be run when its being imported as a module
if __name__ == "__main__":
    # Start the listener in the background
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

    signup()

    while not quitProgram:
        print("\nMenu:")
        print("1. Show todos")
        print("2. Add todo")
        print("3. Quit")
        choice = input("Select an option: ")

        if choice == "1":
            main()  # show todos
        elif choice == "2":
            print("TODO: implement add_todo()")
        elif choice == "3":
            quitProgram = True
        else:
            print("Invalid option")

    listener.join()