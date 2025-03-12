import csv
import os
import time
import getpass
from datetime import datetime
import system.colours as c
import system.machine_compatibility as verify
import system.machine_compatibility as ter

# Get the absolute path to the current directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_DIR, 'credentials.csv')



def countdown(seconds):
    while seconds > 0:
        print(f"\rPlease wait {seconds} seconds...", end="")
        time.sleep(1)
        seconds -= 1

def update_last_logged_in(file_path, username):
    rows = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    # Update the 'Last Logged In' timestamp for the specific user
    for row in rows:
        if row['Username'] == username:
            row['Last Logged In'] = "True"

    # Write back the updated data
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ['Name', 'Username', 'Password','Pincode', 'Last Logged In','Admin Perms']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def auth():
    authentication = verify.auth_sys()
    if authentication:
        print("Authentication successful!")
        return True
    else:
        print(f"{c.RED}Error: Authentication unsuccessful{c.RESET}")
        return False

def username_exists(username):
    """Check if a username already exists in the file."""
    with open(FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        try:
            next(reader)  # Skip header
        except StopIteration:
            return False
        
        return any(row[1] == username for row in reader)


def add_user():
    name = input("Enter name: ").strip()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    pincode = input("Enter a pincode: ").strip()
    
    while True:
        admin_perm = input("Should this user have administrative privileges (y/n): ")
        if admin_perm == "y":
            admin_perm = "1"
            break
        elif admin_perm == "n":
            admin_perm = "0"
            break
        else:
            print(f"{c.RED}Error: Invalid input{c.RESET}")
            continue
    
    if username_exists(username):
        print(f"{c.RED}Error: Username '{username}' is already in use.{c.RESET}")
        return
    
    with open(FILE_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, username, password, pincode, "False", admin_perm])
    print(f'User {username} added.')

def remove_user():
    username = input("Enter username to remove: ").strip()
    
    with open(FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    user_found = False
    
    new_rows = []
    for row in rows:
        if row[1] == username:
            user_found = True
        else:
            new_rows.append(row)
    
    if not user_found:
        print(f'User {username} not found.')
        return
    
    if row[5] == "2":
        print(f"{c.RED}Error: Cannot remove Owner account{c.RESET}")
        return

    
    with open(FILE_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)
    
    print(f'User {username} removed.')

def list_users(show_passwords=False):
    with open(FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        print(f"{'Name':<15}{'Username':<15}" if not show_passwords else f"{'Name':<15} {'Username':<15} {'Password':<25} {'Pincode':<12} {'User Type':<11}")
        print('-' * 100)
        for row in reader:
            if row[5] == "2":
                admin_type = "Owner"
            elif row[5] == "1":
                admin_type = "Admin"
            elif row[5] == "0":
                admin_type = "User"
            print(f"{row[0]:<15}{row[1]:<15}" if not show_passwords else f"{row[0]:<15} {row[1]:<15} {row[2]:<25} {row[3]:<12} {admin_type:11}")


def modify_user(active_user):
    username = input("Enter username to modify: ").strip()

    # Check if the user exists
    if not username_exists(username):
        print(f"Error: Username '{username}' does not exist.")
        return
    elif username == active_user:
        print(f"{c.RED}Error: Cannot modify own username{c.RESET}")
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
                if row[5] == "2":
                    print(f"{c.RED}Cannot modify Owner account{c.RESET}")
                    return

                password = input("Enter new password (or press Enter to keep current): ").strip()
                pincode = input("Enter new pincode (or press Enter to keep current): ").strip()
                while True:
                    admin_bool = input("Enter (y/n) whether this user should have admin privaliges (or press Enter to keep current: )").strip()
                    if admin_bool == "y":
                        break
                    elif admin_bool == "n":
                        break
                    elif admin_bool == "":
                        break
                    else:
                        print("Try again")
                        continue
                
                # Update the user details if inputs are given
                if name:
                    row[0] = name
                if new_username:
                    row[1] = new_username
                if password:
                    row[2] = password
                if pincode:
                    row[3] = pincode
                if admin_bool == "y":
                    row[5] = "1"
                elif admin_bool == "n":
                    row[5] = "0"
                
                print(f'User {username} modified.')
            writer.writerow(row)  # Write back all rows, including the modified user
    
    if not user_found:
        print(f'User {username} not found.')


def load_credentials():
    """Load user credentials from a CSV file."""
    with open(FILE_PATH, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_credentials(data):
    """Save updated credentials back to CSV."""
    with open(FILE_PATH, "w", newline='', encoding='utf-8') as file:
        fieldnames = ["Name", "Username", "Password", "Pincode", "Last Logged In", "Admin Perms"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def transfer_ownership():
    """Transfer ownership to a new user by typing their username."""
    global users  # Ensure changes reflect within the program

    users = load_credentials()  # Load current credentials

    # Find current owner
    owner = next((user for user in users if user["Admin Perms"] == "2"), None)
    
    if not owner:
        print("⚠️ No current owner found!")
        return
    
    print(f"⚠️ Warning: Transferring ownership means you lose fingerprint login and can be removed.")
    confirmation = input('Are you sure you want to continue?\nType "YES" to continue: ')
    
    if confirmation != "YES":
        print("❌ Ownership transfer canceled.")
        return

    # List all users except the current owner
    print("\nAvailable users to transfer ownership to:")
    for user in users:
        if user["Username"] != owner["Username"]:  # Exclude the current owner
            print(f"- {user['Name']} ({user['Username']})")

    while True:
        new_owner_username = input("\nEnter the username of the new owner Or type \"exit\": ").strip()
        if new_owner_username != "exit":
        # Find the new owner by username
            new_owner = next((user for user in users if user["Username"] == new_owner_username), None)

            if not new_owner:
                print("❌ Invalid username. Please enter a valid username from the list above.")
            elif new_owner["Username"] == owner["Username"]:
                print("❌ You cannot transfer ownership to yourself. Choose another user.")
            else:
                # Update permissions
                owner["Admin Perms"] = "1"  # Old owner becomes admin
                new_owner["Admin Perms"] = "2"  # New owner gets ownership

                save_credentials(users)  # Save changes to file
                users = load_credentials()  # Reload data to reflect changes immediately

                print(f"✅ Ownership transferred to {new_owner['Name']} ({new_owner['Username']})")
                print("Program will shutdown now to review changes!")
                quit()
        else:
            print("Exiting...")
            break


def last_boot_logged_in():
    rows = check_last_logged_in()
    if rows != None:
        user_choice = input(f"{c.BLUE}User {rows[0]} is logged in.{c.RESET} \nWould you like to continue as {rows[1]}\n(y/n)\n> ")
        while True:
            if user_choice == "y":
                if rows[5] == 2:
                    admin_auth
                user_password = getpass.getpass("Enter your pincode (Pin has been hidden for security reasons)\n> ")
                if user_password == rows[3]:
                    username = rows[1]
                    pin = rows[3]

                    # Check if the user is an admin
                    admin_int = int(rows[5])

                    if admin_int == 1:
                        print(f"{c.GREEN}Welcome, Admin {rows[1]}!{c.RESET}")
                        return 1, username, pin
                        # You can add more admin-specific functionality here, like admin menus or actions.
                    elif admin_int == 2:
                        print(f"{c.GREEN}Welcome, Owner {rows[1]}!{c.RESET}")
                        return 2, username, pin
                    else:
                        print(f"{c.GREEN}Welcome, User {rows[1]}!{c.RESET}")
                        return 3, username, pin
                        # Non-admin users get basic access.
                else:
                    print(f"{c.RED}Passcode is incorrect{c.RESET}")
                    time.sleep(1)
                    ter.clear_ter()
                    user_choice = input("Would you like to try again? \n(y/n) \n> ")
                    if user_choice == "n":
                        break
                    elif user_choice == "y":
                        continue
                    else:
                        continue
            elif user_choice == "n":
                logout(rows[1])
                return 0, None, None
            else:
                break
    else:
        return 0, None, None




def log_user_login(username):
    log_file = os.path.join(CURRENT_DIR, 'login_log.txt')
    with open(log_file, mode='a') as file:
        log_entry = f"User '{username}' logged in at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        file.write(log_entry)
        
def read_credentials(file_path):
    credentials = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            credentials[row['Username']] = {
                'name': row['Name'],
                'password': row['Password'],
                'pincode': row['Pincode'],
                'last_logged_in': row['Last Logged In'],
                'admin_perms': int(row['Admin Perms'])
            }
    return credentials



def login_system():
    credentials = read_credentials(FILE_PATH)
    max_attempts = 3
    attempts = 0
    user = False
    logged_in_username = None
    admin_level = 0  # Default to regular user
    user_pincode = None  # Store the pincode

    while attempts < max_attempts:
        ter.clear_ter()
        username = input("Enter username: ").strip()
        if username in credentials:
            admin_level = credentials[username].get('admin_perms', 0)
            pin = credentials[username].get('pincode', 0)
            if admin_level == 2:
                verification = verify.auth_sys(pin)
                if verification:
                    print("Verified successfully")
                    update_last_logged_in(FILE_PATH, username)
                    log_user_login(username)
                    return username, admin_level, pin
        ter.clear_ter()
        password_or_pin = getpass.getpass("Enter your pincode or password (Authentication values has been hidden for security reasons: ").strip()
        ter.clear_ter()

        if username in credentials:
            stored_password = credentials[username]['password']
            stored_pincode = credentials[username].get('pincode', None)  # Get pincode, default None

            if password_or_pin == stored_password or password_or_pin == stored_pincode:

                logged_in_username = username
                admin_level = credentials[username].get('admin_perms', 0)
                user_pincode = stored_pincode



                user = True
                print(f"Login successful! Welcome {credentials[username]['name']}.")

                update_last_logged_in(FILE_PATH, username)
                log_user_login(username)
                
                break  # Exit loop after successful login

        attempts += 1
        if attempts < max_attempts:
            print(f"{c.RED}Incorrect username or password/pincode. Attempt {attempts} of {max_attempts}.{c.RESET}")
            input("Press Enter to continue...")

    if not user:
        countdown(15)
        os.system("clear")
        logged_in_username = ""

    return logged_in_username, admin_level, user_pincode






def logout(username):
    rows = []
    with open(FILE_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    for row in rows:
        if row['Username'] == username:
            row['Last Logged In'] = "False"

    # Write back the updated data
    with open(FILE_PATH, mode='w', newline='') as file:
        fieldnames = ['Name', 'Username', 'Password','Pincode', 'Last Logged In','Admin Perms']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        log_user_logout(username)

def log_user_logout(username):
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'login_log.txt')
    with open(log_file, mode='a') as file:  # Open in append mode to add new log entries
        log_entry = f"User '{username}' logged out at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        file.write(log_entry)


def uam_menu(active_user,admin_type,pin):
    while True:
        print("\nCommands:")
        print("1. Add user")
        print("2. Remove user")
        print("3. List users")
        print("4. Modify user")
        if admin_type == 2:
            print("5. Give ownership to a different user")
        if admin_type == 2:    
            print("6. Exit")
        else:
            print("5. Exit")
        if admin_type == 2:
            command = input("\nChoose an option (1-6): ").strip()
        else:
            command = input("\nChoose an option (1-5): ").strip()

        if command == "1":
            add_user()
        elif command == "2":
            remove_user()
        elif command == "3":
            show_passwords = input("Show passwords? (y/n): ")
            if show_passwords == "y":
                authentic = admin_auth(admin_type,pin)
                if authentic == True:
                    list_users(show_passwords.lower() == "y")
                else:
                    list_users(False)
        elif command == "4":
            print(active_user)
            modify_user(active_user)
        elif command == "5" and admin_type == 2:
            auth_ = admin_auth(2,pin)
            if auth_:
                transfer_ownership()
        
        elif command == "5" and admin_type != 2:
            print("Exiting")
            break
        elif command == "6" and admin_type == 2:
            print("Exiting")
            break
        else:
            print("Invalid command. Please try again.")

def log_user_logout(username):
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'login_log.txt')
    with open(log_file, mode='a') as file:  # Open in append mode to add new log entries
        log_entry = f"User '{username}' logged out at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        file.write(log_entry)

def check_last_logged_in():
    """
    This function checks if any row in a CSV file contains 'True' in the 'Last Logged In' column (index 4),
    and returns a tuple with a boolean value and the first row where this condition is met.

    Args:
    csv_file (str): The path to the CSV file.

    Returns:
    tuple: (True, row) if a row contains 'True' in 'Last Logged In', otherwise (False, None).
    """
    with open(FILE_PATH, mode='r', newline='') as file:
        reader = csv.reader(file)
        # Read the header row
        header = next(reader)
        
        # Ensure we check for the exact header name (case-sensitive and trimmed)
        header = [h.strip() for h in header]  # Remove any leading/trailing spaces from the header columns
        
        # Check if the 'Last Logged In' column is at index 4 (case-sensitive)
        if len(header) <= 4 or header[4] != "Last Logged In":
            raise ValueError("Expected 'Last Logged In' column at index 4.")
        
        # Iterate over each row in the CSV
        for row in reader:
            # Ensure the row has at least 5 columns (Name, Username, Password, Pincode, Last Logged In, Admin Perms)
            if len(row) > 4:
                # Check if the value at index 4 (Last Logged In) is 'True'
                if row[4].strip().lower() == 'true':  # CSV data is read as strings, hence 'true'
                    return (row)  # Return True and the first matching row

    # Return False and None if no 'Last Logged In' is True
    return (None)


def admin_auth(admin_level,pin):
    if admin_level == 2:
        verification = verify.auth_sys(pin)
        if verification:
            print("Authorisation successful")
            return True
        else:
            return False
    elif admin_level == 1:
        admin_pin = getpass.getpass("Enter your pincode (Pin has been hidden for security reasons)\n> ")
        if admin_pin == pin:
            print("Authorisation successful")
        else:
            return False
    else:
        print(f"{c.RED}Error{c.RESET}")