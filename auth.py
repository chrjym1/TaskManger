import os

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
                # Safely parse each line
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                parts = line.split(',')
                if len(parts) != 2:
                    continue  # Skip malformed lines
                stored_username, _ = parts
                if stored_username == username:
                    print("Username already exists. Please choose a different username.")
                    return
    except FileNotFoundError:
        pass  # If the file doesn't exist, proceed to create a new user

    with open(auth_file, 'a') as file:
        file.write(f"{username},{password}\n")
    print("Signup successful! You can now log in.")
    clear_screen()

def login(auth_file):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        with open(auth_file, 'r') as file:
            for line in file:
                # Safely parse each line
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                parts = line.split(',')
                if len(parts) != 2:
                    continue  # Skip malformed lines
                stored_username, stored_password = parts
                if stored_username == username and stored_password == password:
                    print("Login successful! Welcome back!")
                    clear_screen()
                    return True
    except FileNotFoundError:
        pass  # If the file doesn't exist, login cannot proceed

    print("Invalid username or password. Please try again.")
    return False
