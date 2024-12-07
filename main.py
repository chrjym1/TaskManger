from auth import signup, login  # Import functions from auth.py
from task_queue import Queue  # Import the Queue class

# File name to store user data
auth_file = 'user_data.txt'
task_queue = Queue()

def dash_board():
    while True:
        print("\nDashboard")
        print("1. Create Task")
        print("2. View Tasks")
        print("3. Remove Task")
        print("4. Undo Task")
        print("5. Redo Task")
        print("6. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                title = input("Enter task title: ")
                priority = int(input("Enter task priority (lower number = higher priority): "))
                quadrant = int(input("Enter task quadrant (1-4): "))
                task_queue.add_task_to_queue(title, priority, quadrant)
            except ValueError as e:
                print(f"Invalid input: {e}")
        elif choice == '2':
            task_queue.display_queue()
        elif choice == '3':
            try:
                task_id = int(input("Enter the task ID to remove: "))
                quadrant = int(input("Enter the quadrant of the task: "))
                task_queue.remove_task_from_queue(task_id, quadrant)
            except ValueError as e:
                print(f"Invalid input: {e}")
        elif choice == '4':
            task_queue.undo()
        elif choice == '5':
            task_queue.redo()
        elif choice == '6':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")


def main():
    open(auth_file, 'a').close()

    while True:
        print("\n1. Signup")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            signup(auth_file)
        elif choice == '2':
            login_successful = login(auth_file)
            if login_successful:
                dash_board()
            else:
                print("Login failed. Please try again.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
