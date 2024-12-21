from auth import signup, login  # Import functions from auth.py
from task_queue import Queue  # Import the Queue class
import os
import logging
import json

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# File name to store user data
auth_file = 'user_data.txt'
task_queue = Queue()

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def signup(auth_file):
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")

    try:
        with open(auth_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) != 2:
                    continue
                stored_username, _ = parts
                if stored_username == username:
                    print("Username already exists. Please choose a different username.")
                    return
    except FileNotFoundError:
        pass

    with open(auth_file, 'a') as file:
        file.write(f"{username},{password}\n")
    print("Signup successful! You can now log in.")
    clear_screen()

    # Create an individual tasks JSON file for the user
    with open(f"{username}_tasks.json", 'w') as task_file:
        json.dump({"tasks": []}, task_file, indent=4)

def login(auth_file):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        with open(auth_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) != 2:
                    continue
                stored_username, stored_password = parts
                if stored_username == username and stored_password == password:
                    print("Login successful! Welcome back!")
                    clear_screen()
                    return username
    except FileNotFoundError:
        pass

    print("Invalid username or password. Please try again.")
    return None

def save_tasks(username):
    """Saves tasks to a user's JSON file."""
    tasks = task_queue.get_all_tasks()
    with open(f"{username}_tasks.json", 'w') as file:
        json.dump({"tasks": tasks}, file, indent=4)

def load_tasks(username):
    """Loads tasks from a user's JSON file."""
    try:
        with open(f"{username}_tasks.json", 'r') as file:
            data = json.load(file)
            task_queue.set_all_tasks(data["tasks"])
    except FileNotFoundError:
        logging.warning(f"No task file found for user: {username}. Starting with an empty queue.")

def display_header(title):
    """Displays a formatted header."""
    clear_screen()
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60)

def display_tasks():
    """Displays the current tasks and history."""
    print("\n" + "=" * 30)
    print("          Current Tasks")
    print("=" * 30)
    task_queue.display_queue()
    print("=" * 30)
    print("\nHistory:")
    task_queue.display_history()

def input_with_validation(prompt, validation_func, error_message):
    """Prompts for input and validates it."""
    while True:
        try:
            value = validation_func(input(prompt))
            return value
        except Exception as e:
            print(f"{error_message}: {e}")

def dash_board(username):
    """Displays the dashboard and handles user interactions."""
    load_tasks(username)
    while True:
        display_header("Dashboard")
        display_tasks()
        
        print("\n" + "=" * 60)
        print("1. Create Task")
        print("2. View Tasks")
        print("3. Remove Task")
        print("4. Undo Task")
        print("5. Redo Task")
        print("6. Logout")
        print("=" * 60)

        choice = input("Enter your choice: ")
        if choice == '1':
            title = input("Enter task title: ")
            priority = input_with_validation(
                "Enter task priority (lower number = higher priority): ",
                lambda x: int(x) if int(x) > 0 else ValueError("Priority must be positive"),
                "Invalid priority"
            )
            quadrant = input_with_validation(
                "Enter task quadrant (1-4): ",
                lambda x: int(x) if 1 <= int(x) <= 4 else ValueError("Quadrant must be between 1 and 4"),
                "Invalid quadrant"
            )
            task_queue.add_task_to_queue(title, priority, quadrant)
            save_tasks(username)
            input("Task added successfully! Press Enter to continue...")
        elif choice == '2':
            display_header("Current Tasks")
            display_tasks()
            input("\nPress Enter to return to the dashboard...")
        elif choice == '3':
            task_id = input_with_validation(
                "Enter the task ID to remove: ",
                int, 
                "Invalid task ID"
            )
            quadrant = input_with_validation(
                "Enter the quadrant of the task: ",
                lambda x: int(x) if 1 <= int(x) <= 4 else ValueError("Quadrant must be between 1 and 4"),
                "Invalid quadrant"
            )
            task_queue.remove_task_from_queue(task_id, quadrant)
            save_tasks(username)
            input("Task removed successfully! Press Enter to continue...")
        elif choice == '4':
            task_queue.undo()
            save_tasks(username)
            input("Undo successful! Press Enter to continue...")
        elif choice == '5':
            task_queue.redo()
            save_tasks(username)
            input("Redo successful! Press Enter to continue...")
        elif choice == '6':
            print("Logging out...")
            break
        else:
            input("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6. Press Enter to continue...")

def main():
    """Main function to handle user authentication and navigation."""
    try:
        open(auth_file, 'a').close()
    except IOError as e:
        print(f"Error initializing authentication file: {e}")
        return

    while True:
        display_header("Welcome")
        print("1. Signup")
        print("2. Login")
        print("3. Exit")
        print("=" * 60)

        choice = input("Enter your choice: ")
        if choice == '1':
            signup(auth_file)
            input("Signup successful! Press Enter to continue...")
        elif choice == '2':
            username = login(auth_file)
            if username:
                dash_board(username)
            else:
                input("Login failed. Please try again. Press Enter to continue...")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            input("Invalid choice. Please enter 1, 2, or 3. Press Enter to continue...")

if __name__ == "__main__":
    main()
