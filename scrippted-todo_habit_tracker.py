import json
import os
from datetime import datetime

# File to store data
DATA_FILE = 'data.json'

# Colors
OCEAN_BLUE = '\033[94m'
TREE_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

# Cute cat ASCII art (fixed escape sequence)
CAT_ART = r"""
  /\_/\
 ( o.o )
  > ^ <
"""

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    # Ensure 'archive' key is always present
    return {"todos": [], "habits": [], "archive": []}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def get_today():
    return datetime.now().strftime("%Y-%m-%d %A")

def add_todo(data):
    task = input("Enter the task: ")
    data["todos"].append({"task": task, "done": False, "date_added": get_today()})
    save_data(data)
    print("Task added!")

def list_todos(data):
    print(f"\n{OCEAN_BLUE}TinyToDo{RESET_COLOR}")
    print(f"{OCEAN_BLUE}Date: {get_today()}{RESET_COLOR}")
    print(f"\n{OCEAN_BLUE}To-Do List:{RESET_COLOR}")
    if data["todos"]:
        for i, todo in enumerate(data["todos"], 1):
            status = "✓" if todo["done"] else "0"
            print(f"{i}. [{status}] {todo['task']}")
    else:
        print("No to-dos available.")
    # Show number of archived to-dos
    archived_count = len(data.get("archive", []))
    print(f"\nNumber of Archived To-Dos: {archived_count}")

def mark_todo_done(data):
    list_todos(data)
    if data["todos"]:
        index = int(input("Enter the task number to mark as done: ")) - 1
        if 0 <= index < len(data["todos"]):
            data["todos"][index]["done"] = True
            save_data(data)
            print("Task marked as done!")
        else:
            print("Invalid task number!")

def archive_completed_todos(data):
    now = datetime.now()
    to_archive = [todo for todo in data["todos"] if todo["done"] and 
                  (now - datetime.strptime(todo["date_added"], "%Y-%m-%d %A")).days >= 1]
    if to_archive:
        data["archive"].extend(to_archive)
        data["todos"] = [todo for todo in data["todos"] if not todo["done"]]
        save_data(data)
        print("Archived completed to-dos older than 1 day.")
    # No message if no to-dos to archive

def delete_todo_options(data):
    list_todos(data)
    if data["todos"]:
        print("\nOptions:")
        print(f"{OCEAN_BLUE}1. Delete Selected To-Do{RESET_COLOR}")
        print(f"{OCEAN_BLUE}2. Delete All To-Dos{RESET_COLOR}")
        print(f"{OCEAN_BLUE}3. Archive Completed To-Dos{RESET_COLOR}")
        print(f"{OCEAN_BLUE}4. Return to Main Menu{RESET_COLOR}")
        choice = input("Choose an option: ")

        if choice == '1':
            delete_todo(data)
        elif choice == '2':
            delete_all_todos(data)
        elif choice == '3':
            archive_completed_todos(data)
        elif choice == '4':
            return
        else:
            print("Invalid choice! Returning to main menu.")
    else:
        print("No to-dos available to delete.")

def delete_todo(data):
    index = int(input("Enter the task number to delete: ")) - 1
    if 0 <= index < len(data["todos"]):
        del data["todos"][index]
        save_data(data)
        print("Task deleted!")
    else:
        print("Invalid task number!")

def delete_all_todos(data):
    confirm = input("Are you sure you want to delete all to-dos? (y/n): ").strip().lower()
    if confirm == 'y':
        data["todos"] = []
        save_data(data)
        print("All to-dos deleted!")
    else:
        print("Deletion canceled.")

def add_habit(data):
    habit = input("Enter the habit: ")
    data["habits"].append({"habit": habit, "completed_days": 0})
    save_data(data)
    print("Habit added!")

def list_habits(data):
    print(f"\n{TREE_GREEN}Habits ({get_today()}):{RESET_COLOR}")
    if data["habits"]:
        for i, habit in enumerate(data["habits"], 1):
            print(f"{i}. {habit['habit']} (Days Completed: {habit['completed_days']})")
    else:
        print("No habits available.")

def complete_habit(data):
    list_habits(data)
    if data["habits"]:
        index = int(input("Enter the habit number to mark as completed: ")) - 1
        if 0 <= index < len(data["habits"]):
            print(f"Current Days Completed: {data['habits'][index]['completed_days']}")
            new_days = input("Enter the number of days completed (or leave blank to keep current): ")
            if new_days.strip() == '':
                new_days = data['habits'][index]['completed_days']
            else:
                try:
                    new_days = int(new_days)
                except ValueError:
                    print("Invalid input! Keeping current number of days.")
                    new_days = data['habits'][index]['completed_days']
            data['habits'][index]['completed_days'] = new_days
            save_data(data)
            print("Habit updated!")
        else:
            print("Invalid habit number!")

def delete_habit_options(data):
    list_habits(data)
    if data["habits"]:
        print("\nOptions:")
        print(f"{TREE_GREEN}4. Delete Selected Habit{RESET_COLOR}")
        print(f"{TREE_GREEN}5. Delete All Habits{RESET_COLOR}")
        print(f"{TREE_GREEN}6. Return to Main Menu{RESET_COLOR}")
        choice = input("Choose an option: ")

        if choice == '4':
            delete_habit(data)
        elif choice == '5':
            delete_all_habits(data)
        elif choice == '6':
            return
        else:
            print("Invalid choice! Returning to main menu.")
    else:
        print("No habits available to delete.")

def delete_habit(data):
    index = int(input("Enter the habit number to delete: ")) - 1
    if 0 <= index < len(data["habits"]):
        del data["habits"][index]
        save_data(data)
        print("Habit deleted!")
    else:
        print("Invalid habit number!")

def delete_all_habits(data):
    confirm = input("Are you sure you want to delete all habits? (y/n): ").strip().lower()
    if confirm == 'y':
        data["habits"] = []
        save_data(data)
        print("All habits deleted!")
    else:
        print("Deletion canceled.")

def main():
    data = load_data()
    while True:
        # Archive completed to-dos older than 1 day
        archive_completed_todos(data)

        # Display the date and day, and lists
        list_todos(data)
        list_habits(data)

        # Display the options with the cat art
        print(CAT_ART)
        print("\nOptions:")
        print(f"{OCEAN_BLUE}1. Add To-Do{RESET_COLOR}")
        print(f"{OCEAN_BLUE}2. Mark To-Do as Done{RESET_COLOR}")
        print(f"{OCEAN_BLUE}3. Delete To-Do{RESET_COLOR}")
        print(f"{TREE_GREEN}4. Add Habit{RESET_COLOR}")
        print(f"{TREE_GREEN}5. Complete Habit{RESET_COLOR}")
        print(f"{TREE_GREEN}6. Delete Habit{RESET_COLOR}")
        print(f"{TREE_GREEN}7. Exit{RESET_COLOR}")

        choice = input("Choose an option: ")

        if choice == '1':
            add_todo(data)
        elif choice == '2':
            if data["todos"]:
                mark_todo_done(data)
            else:
                print("No to-dos available to mark as done.")
        elif choice == '3':
            delete_todo_options(data)
        elif choice == '4':
            add_habit(data)
        elif choice == '5':
            if data["habits"]:
                complete_habit(data)
            else:
                print("No habits available to mark as completed.")
        elif choice == '6':
            delete_habit_options(data)
        elif choice == '7':
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
