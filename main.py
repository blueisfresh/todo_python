import json
import datetime

from simple_term_menu import TerminalMenu

username = None


# TODO: Global todo dictionary filtered based on username


def main(username):
    menu_options = ["Show todos", "Add Todo", "Edit Todo", "Delete Todo", "Quit"]
    terminal_menu = TerminalMenu(menu_options)
    # index of what you currently have selected
    menu_entry_index = terminal_menu.show()

    # using the index getting the menu_options
    choice = menu_options[menu_entry_index]

    # Depending on Choice - calling the right method
    if choice == "Show todos":
        read_todos(username)
    elif choice == "Add Todo":
        create_todo()
    elif choice == "Edit Todo":
        edit_todo()
    elif choice == "Delete Todo":
        delete_todo()
    elif choice == "Quit":
        return False  # quit the outer while loop

    print(f"\nYou have selected {choice}!\n")
    return True  # keep the program running


def signup():
    print("Hello, welcome to your todo App")
    return prompt_required("Choose a username (no spaces): ", allow_spaces=False)


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


def delete_todo():
    # Load existing Todos
    with open("todo.json", "r") as json_file:
        data = json.load(json_file)
        todos = data["todos"]  # or just data if you're using raw list JSON

    print("\n--- Delete Todo ---")
    id = prompt_required("Please enter the ID of the todo to delete: ", allow_spaces=False)

    # Find the todo by ID
    matches = [todo for todo in todos if str(todo["id"]) == id]
    if not matches:
        print("❌ No todo found with that ID.")
        return

    todo = matches[0]

    # TODO: Use edit confirmation
    # Optional confirm step before deleting
    print(f"⚠️  Are you sure you want to delete Todo #{id}: '{todo['title']}'?")
    confirm = input("Type 'yes' to confirm: ").lower()

    if confirm == "yes":
        todos.remove(todo)

        # Save back
        with open("todo.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        print("\n✅ Todo deleted successfully!\n")
    else:
        print("\n🚫 Delete cancelled.\n")


def edit_todo():
    # TODO: Automatically display the todo list when editing

    # Load existing Todos
    with open("todo.json", "r") as json_file:
        data = json.load(json_file)
        todos = data["todos"]

    # Ask user for details
    print("\n--- Edit Todo ---")
    id = prompt_required("Please enter your ID (no spaces): ", allow_spaces=False)

    # Find the todo by ID
    matches = [todo for todo in todos if str(todo["id"]) == id]
    if not matches:
        print("❌ No todo found with that ID.")
        return

    todo = matches[0]

    # Title
    new_title = input(f"Title (leave blank to keep '{todo['title']}'): ").strip()
    if new_title:
        todo["title"] = new_title

    # Due date
    while True:
        new_due = input(f"Due date (YYYY-MM-DD, leave blank to keep {todo['due_date']}): ").strip()
        if not new_due:
            break
        try:
            datetime.date.fromisoformat(new_due)
            todo["due_date"] = new_due
            break
        except ValueError:
            print("❌ Incorrect format. Expected YYYY-MM-DD.")

    # Completed toggle
    options_completed = ["Yes", "No"]
    terminal_menu = TerminalMenu(options_completed, title="Mark as completed?")
    answer_index = terminal_menu.show()
    todo["completed"] = (options_completed[answer_index] == "Yes")

    # Save back
    with open("todo.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("\n✅ Todo updated successfully!\n")


def create_todo():
    # Load existing Todos
    with open("todo.json", "r") as json_file:
        data = json.load(json_file)
        todos = data["todos"]

    # Generate next ID
    next_id = max([todo["id"] for todo in todos], default=0) + 1

    # Ask user for details
    print("\n--- Create a New Todo ---")
    title = prompt_required("Title: ", allow_spaces=True)
    due_date = prompt_due_date()

    # Build todo dict
    new_todo = {
        "id": next_id,
        "title": title,
        "completed": False,
        "due_date": due_date,
        "user": username,
    }

    # Append new todo
    todos.append(new_todo)

    # Save back
    with open("todo.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("\n✅ Todo created successfully!\n")


def validate(date_text):
    try:
        datetime.date.fromisoformat(date_text)
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def prompt_required(prompt_text, allow_spaces=True):
    """Prompt the user until they provide a valid non-empty string.
    If allow_spaces=False, disallow spaces in the input."""
    while True:
        value = input(prompt_text).strip()
        if not value:
            print("❌ Value cannot be empty. Try again.")
            continue
        if not allow_spaces and " " in value:
            print("❌ Value cannot contain spaces. Try again.")
            continue
        return value


def prompt_due_date():
    """Prompt the user until a valid date in YYYY-MM-DD format is entered."""
    while True:
        date_str = input("Due date (YYYY-MM-DD): ").strip()
        if not date_str:
            print("❌ Due Date cannot be empty. Try again.")
            continue
        try:
            # Use ISO format parsing
            datetime.date.fromisoformat(date_str)
            return date_str
        except ValueError:
            print("❌ Incorrect format. Expected YYYY-MM-DD.")


# prevent python main script to be run when its being imported as a module
if __name__ == "__main__":
    # Asking for Username
    username = signup()

    running = True;
    while running:
        running = main(username)
