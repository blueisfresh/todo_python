import json
import datetime
from datetime import datetime
from simple_term_menu import TerminalMenu


class TodoApp:
    # Constructor
    def __init__(self, username, filename="Todo.json"):
        self.username = username
        self.filename = filename

    # Core File operations
    def load_all_todos(self):
        """Return Todos Dictionary from self.filename."""
        with open(self.filename, "r") as todo_json:
            todos = json.load(todo_json)["todos"]

        if not todos:
            print("\n❌ No todos found.\n")
            return
        else:
            return todos

    def save_all_todos(self, todos):
        """Save Todos Dictionary to self.filename."""
        with open(self.filename, "w") as todo_json:
            json.dump({"todos": todos}, todo_json, indent=4)

    def load_user_todos(self):
        """Return Todos Dictionary from self.filename with the correct username."""
        todos = self.load_all_todos()
        user_todos = [todo for todo in todos if todo["user"] == self.username]

        if not user_todos:
            print("\n❌ No todos found for your user.\n")
            return
        else:
            return user_todos

    # UI Helpers
    def print_todo(todos):
        """Print passed in todos Dictionary."""
        print("\n" + "=" * 60)
        print("📋 YOUR TODOS")
        print("=" * 60)

        today = datetime.today().strftime('%Y-%m-%d')

        # define column width explicitly
        col_id, col_title, col_status, col_due = 5, 30, 6, 12

        # header
        print(
            f"{'ID':<{col_id}} {'Title':<{col_title}} "
            f"{'Status':<{col_status}} {'Due Date':<{col_due}}"
        )
        print("-" * (col_id + col_title + col_status + col_due + 3))

        # rows
        for todo in todos:
            status = "✓" if todo["completed"] else "✗"
            if todo["due_date"]:
                due_date_obj = datetime.fromisoformat(todo["due_date"]).date()
                if due_date_obj < datetime.today().date() and not todo["completed"]:
                    due = f"{todo['due_date']} ⚠️"
                else:
                    due = todo["due_date"]
            else:
                due = "-"

            print(
                f"{todo['id']:<{col_id}} {todo['title']:<{col_title}} "
                f"{status:<{col_status}} {due:<{col_due}}"
            )

        print("=" * 60 + "\n")

    @staticmethod
    def prompt_required(prompt_text, allow_spaces=True):
        """Generalized Method to take care of empty user input."""
        while True:
            value = input(prompt_text).strip()
            if not value:
                print("❌ Value cannot be empty. Try again.\n")
                continue
            if not allow_spaces and " " in value:
                print("❌ Value cannot contain spaces. Try again.\n")
                continue
            return value

    @staticmethod
    def prompt_due_date():
        """Generalized Method to take care of Due Date user input & validation."""
        while True:
            date_str = input("Due date (YYYY-MM-DD, leave blank for none): ").strip()
            if not date_str:  # optional → None
                return None
            try:
                # Use ISO format parsing
                datetime.date.fromisoformat(date_str)
                return date_str
            except ValueError:
                print("❌ Incorrect format. Expected YYYY-MM-DD.\n")

    # Menu Actions
    def display_todos(self):
        """Method to display Todos Dictionary."""
        print("\n" + "=" * 60)
        print("📋 DISPLAYING YOUR TODOS")
        print("=" * 60)

        # Get User specific todos
        todos = self.load_user_todos()
        # Print Todos if they were fetched correctly
        if todos:
            self.print_todo(todos)
        else:
            print("\n🔍 You don't have any todos yet!")
            print("💡 Try creating one with 'Add Todo'.\n")

    def create_todo(self):
        """Method to create Todos Dictionary."""
        print("\n" + "=" * 60)
        print("➕ CREATE NEW TODO")
        print("=" * 60)

        # Load all Todos
        all_todos = self.load_all_todos()
        # Generate next ID
        next_id = max([todo["id"] for todo in all_todos], default=0) + 1

        # Ask user for details
        print("\nPlease provide the following information:\n")
        title = self.prompt_required("📝 Title: ", allow_spaces=True)
        print()  # spacing
        due_date = self.prompt_due_date()

        # Build new todo
        new_todo = {
            "id": next_id,
            "title": title,
            "completed": False,
            "due_date": due_date,
            "user": self.username,
        }

        # Append new todo to all_todos dictionary
        all_todos.append(new_todo)

        # Save it using custom utils method
        self.save_all_todos(all_todos)

        print("\n✅ Todo created successfully!")
        print(f"📋 Created: '{title}' (ID: {next_id})")
        print("=" * 60 + "\n")

    def edit_todo(self):
        """Method to edit Todos Dictionary."""
        print("\n" + "=" * 60)
        print("\n" + "=" * 60)
        print("✏️  EDIT TODO")
        print("=" * 60)

        all_todos = self.load_all_todos()
        user_todos = self.load_user_todos()

        if not user_todos:
            return

        self.print_todo(user_todos)

        # Ask user for details
        print("\n--- Edit Todo ---")
        id = self.prompt_required("Please enter your ID (no spaces): ", allow_spaces=False)

        # Find the todo by ID
        match = [todo for todo in all_todos if todo["user"] == self.username and str(todo["id"]) == id]
        if not match:
            print("❌ No todo found with that ID.")
            return

        todo = match[0]
        print(f"✏️  Editing Todo: '{todo['title']}'")
        print("-" * 40)

        # Title
        new_title = input(f"\n📝 Title (leave blank to keep '{todo['title']}'): ").strip()
        if new_title:
            todo["title"] = new_title

        # Due date
        while True:
            new_due = input(f"📅 Due date (YYYY-MM-DD, leave blank to keep '{todo['due_date']}'): ").strip()
            if not new_due:
                break
            try:
                datetime.date.fromisoformat(new_due)
                todo["due_date"] = new_due
                break
            except ValueError:
                print("❌ Incorrect format. Expected YYYY-MM-DD.\n")

        print()
        # Completed toggle
        complete_menu = TerminalMenu(["Yes", "No"], title="✅ Mark as completed?")
        todo["completed"] = (complete_menu.show() == 0)

        # Confirm step before saving
        print(f"\n⚠️  Save changes to Todo #{id}: '{todo['title']}'?")
        confirm_menu = TerminalMenu(["Yes", "No"], title="💾 Confirm Changes?")

        if confirm_menu.show() == 0:
            self.save_all_todos(all_todos)
            print("\n✅ Todo updated successfully!")
            print("=" * 60 + "\n")
        else:
            print("\n🚫 Update cancelled.")
            print("=" * 60 + "\n")

    def delete_todo(self):
        """Method to delete Todos Dictionary."""
        print("\n" + "=" * 60)
        print("🗑️  DELETE TODO")
        print("=" * 60)

        all_todos = self.load_all_todos()
        user_todos = self.load_user_todos()

        if not user_todos:
            return

        self.print_todo(user_todos)

        id = self.prompt_required("Please enter the ID of the todo to delete: ", allow_spaces=False)
        print()

        # Find the todo by ID
        match = [todo for todo in all_todos if todo["user"] == self.username and str(todo["id"]) == id]
        if not match:
            print("❌ No todo found with that ID.\n")
            return

        todo = match[0]

        # Confirm step before deleting
        print(f"⚠️  Delete Todo #{id}: '{todo['title']}'?")
        print("⚠️  This action cannot be undone!")
        confirm_menu = TerminalMenu(["Yes, Delete", "No, Cancel"], title="🗑️  Confirm Deletion?")

        if confirm_menu.show() == 0:
            all_todos.remove(todo)
            self.save_all_todos(all_todos)
            print("\n✅ Todo deleted successfully!")
            print(f"🗑️  Deleted: '{todo['title']}'")
            print("=" * 60 + "\n")
        else:
            print("\n🚫 Delete cancelled.")
            print("=" * 60 + "\n")

    def run(self):
        """Main function that prints menu and redirects you to your selected action."""
        print("\n🚀 Todo App is running...\n")

        running = True
        while running:
            menu_options = [
                "📋 Show todos",
                "➕ Add Todo",
                "✏️  Edit Todo",
                "🗑️  Delete Todo",
                "👋 Quit",
            ]
            print("=" * 40)
            print(f"👤 Welcome back, {self.username}!")
            print("=" * 40)

            terminal_menu = TerminalMenu(menu_options)
            choice_index = terminal_menu.show()
            choice = menu_options[choice_index]

            if choice == "Show todos":
                self.display_todos()
            elif choice == "Add Todo":
                self.create_todo()
            elif choice == "Edit Todo":
                self.edit_todo()
            elif choice == "Delete Todo":
                self.delete_todo()
            elif choice.endswith("Quit"):
                print("\n👋 Thanks for using Todo App!")
                print("🎯 Stay productive! See you next time.\n")
                running = False
                break

            if running:  # Don't show this message when quitting
                input("Press Enter to continue...")
                print()


# App Entry Point
def signup():
    """Method that asks for user information."""
    print("\n" + "=" * 60)
    print("🎉 WELCOME TO YOUR TODO APP")
    print("=" * 60)
    print("📝 Organize your tasks and boost your productivity!")
    print()

    return TodoApp.prompt_required("👤 Choose a username (no spaces): ", allow_spaces=False)


# prevent python main script to be run when its being imported as a module
if __name__ == "__main__":
    # Asking for Username
    username = signup()
    print(f"\n🎯 Welcome, {username}! Let's get organized.\n")

    app = TodoApp(username)
    app.run()
