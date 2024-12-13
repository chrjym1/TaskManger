from auth import signup, login  # Import functions from auth.py
from task_queue import Queue  # Import the Queue class
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# File name to store user data
auth_file = 'user_data.txt'
task_queue = Queue()

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

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

def dash_board():
    """Displays the dashboard and handles user interactions."""
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
            input("Task removed successfully! Press Enter to continue...")
        elif choice == '4':
            task_queue.undo()
            input("Undo successful! Press Enter to continue...")
        elif choice == '5':
            task_queue.redo()
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
            login_successful = login(auth_file)
            if login_successful:
                dash_board()
            else:
                input("Login failed. Please try again. Press Enter to continue...")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            input("Invalid choice. Please enter 1, 2, or 3. Press Enter to continue...")

if __name__ == "__main__":
    main()
