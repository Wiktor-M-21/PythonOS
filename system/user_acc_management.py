import csv
import os
import system.colours as c
import touchid

# Get the absolute path to the current directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_DIR, 'credentials.csv')

# Check if the file exists, if not create it with headers
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Username', 'Password'])  # Create headers

def username_exists(username):
    """Check if a username already exists in the file."""
    with open(FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)  # Skip header
        except StopIteration:
            # If the file is empty or only contains the header, return False
            return False
        
        # Check if any row has the given username
        for row in reader:
            if row[1] == username:
                return True
    return False


def add_user():
    name = input("Enter name: ").strip()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    # Check if username already exists
    if username_exists(username):
        print(f"{c.RED}Error: Username '{username}' is already in use.{c.RESET}")
        return

    with open(FILE_PATH, 'a', newline='') as f:  # Open in append mode
        writer = csv.writer(f)
        writer.writerow([name, username, password])
    print(f'User {username} added.')

def remove_user():
    username = input("Enter username to remove: ").strip()
    rows = []
    user_found = False
    with open(FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)  # Read all rows
    try:
        verify_rem = touchid.authenticate()
    except:
        verify_rem = False
    if verify_rem == True:
        with open(FILE_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                if row[1] != username:
                    writer.writerow(row)  # Write back all other users
                else:
                    user_found = True
        
        if user_found:
            print(f'User {username} removed.')
        else:
            print(f'User {username} not found.')
    # Reopen the file in write mode to overwrite

def modify_user():
    username = input("Enter username to modify: ").strip()

    # Check if the user exists
    if not username_exists(username):
        print(f"Error: Username '{username}' does not exist.")
        return

    rows = []
    user_found = False
    with open(FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Open the file in write mode to overwrite only after modifications
    with open(FILE_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            if row[1] == username:
                user_found = True
                print("Leave blank if you don't want to change the value.")
                name = input("Enter new name (or press Enter to keep current): ").strip()
                new_username = input("Enter new username (or press Enter to keep current): ").strip()

                # Check if the new username already exists
                if new_username and new_username != username and username_exists(new_username):
                    print(f"Error: Username '{new_username}' is already in use. Please choose a different username.")
                    return

                password = input("Enter new password (or press Enter to keep current): ").strip()
                
                # Update the user details if inputs are given
                if name:
                    row[0] = name
                if new_username:
                    row[1] = new_username
                if password:
                    row[2] = password
                
                print(f'User {username} modified.')
            writer.writerow(row)  # Write back all rows, including the modified user
    
    if not user_found:
        print(f'User {username} not found.')

def list_users(show_passwords=False):
    with open(FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(f"{'Name':<15} {'Username':<15} {'Password':<15}" if show_passwords else f"{'Username':<15}")
        print('-' * 45)
        for row in reader:
            if show_passwords:
                print(f"{row[0]:<15} {row[1]:<15} {row[2]:<15}")
            else:
                print(f"{row[1]:<15}")

# Command handler
def uam_menu():
    while True:
        print("\nCommands:")
        print("1. Add user")
        print("2. Remove user")
        print("3. Modify user")
        print("4. List users")
        print("5. Exit")
        command = input("\nChoose an option (1-5): ").strip()

        if command == "1":
            add_user()
        elif command == "2":
            remove_user()
        elif command == "3":
            modify_user()
        elif command == "4":
            show_passwords = input("Show passwords? (y/n): ")
            if show_passwords == "y":
                try:
                    verify = touchid.authenticate()
                except Exception:
                    print("Could not verify admin")
                    list_users()
                if verify == True:
                    list_users(show_passwords)
                else:
                    list_users()
            else:
                list_users()
        elif command == "5":
            print("Exiting.")
            break
        else:
            print("Invalid command. Please try again.")