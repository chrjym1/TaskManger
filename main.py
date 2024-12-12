from auth import signup, login  # Import functions from auth.py
from task_queue import Queue  # Import the Queue class
import os

# File name to store user data
auth_file = 'user_data.txt'
task_queue = Queue()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_tasks():
    print("\n" + "="*30)
    print("          Current Tasks")
    print("="*30)
    task_queue.display_queue()
    print("="*30)

def dash_board():
    while True:
        clear_screen()
        display_tasks()
        print("\n" + "="*30)
        print("          Dashboard")
        print("="*30)
        print("1. Create Task")
        print("2. View Tasks")
        print("3. Remove Task")
        print("4. Undo Task")
        print("5. Redo Task")
        print("6. Logout")
        print("="*30)
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                title = input("Enter task title: ")
                priority = int(input("Enter task priority (lower number = higher priority): "))
                quadrant = int(input("Enter task quadrant (1-4): "))
                task_queue.add_task_to_queue(title, priority, quadrant)
                input("Task added successfully! Press Enter to continue...")
            except ValueError as e:
                input(f"Invalid input: {e}. Press Enter to continue...")
        elif choice == '2':
            clear_screen()
            display_tasks()
            input("\nPress Enter to return to the dashboard...")
        elif choice == '3':
            try:
                task_id = int(input("Enter the task ID to remove: "))
                quadrant = int(input("Enter the quadrant of the task: "))
                task_queue.remove_task_from_queue(task_id, quadrant)
                input("Task removed successfully! Press Enter to continue...")
            except ValueError as e:
                input(f"Invalid input: {e}. Press Enter to continue...")
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
    open(auth_file, 'a').close()

    while True:
        clear_screen()
        print("\n" + "="*30)
        print("          Welcome")
        print("="*30)
        print("1. Signup")
        print("2. Login")
        print("3. Exit")
        print("="*30)
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
