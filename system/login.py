
import csv
import time
from datetime import datetime
import os
import system.colours as c


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(CURRENT_DIR, 'credentials.csv')


def countdown(seconds):
    while seconds > 0:
        print(f"\rPlease wait {seconds} seconds...", end="")
        time.sleep(1)
        seconds -= 1


# Function to log the user's login time to a text file
def log_user_login(username):
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'login_log.txt')
    with open(log_file, mode='a') as file:  # Open in append mode to add new log entries
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
                'last_logged_in': row['Last Logged In']
            }
    return credentials

def update_last_logged_in(file_path, username):
    rows = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    # Update the 'Last Logged In' timestamp for the specific user
    for row in rows:
        if row['Username'] == username:
            row['Last Logged In'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Write back the updated data
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ['Name', 'Username', 'Password', 'Last Logged In']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def login_system():
    credentials = read_credentials(file_path)
    max_attempts = 3
    attempts = 0
    user = False
    logged_in_username = None

    while attempts < max_attempts:
        os.system("clear")
        username = input("Enter username: ")
        os.system("clear")
        password = input("Enter password: ")
        os.system("clear")

        if username in credentials and credentials[username]['password'] == password:
            user = True
            logged_in_username = username
            print(f"Login successful! Welcome {credentials[username]['name']}.")
            update_last_logged_in(file_path, username)
            log_user_login(username)  # Log the successful login
            break
        else:
            attempts += 1
            if attempts < max_attempts:
                print(f"{c.RED}Incorrect username or password. Attempt {attempts} of {max_attempts}.{c.RESET}")
                input("Press Enter to continue...")
    
    if not user:
        countdown(15)
        os.system("clear")
    
    return user, logged_in_username

