import system.colours as c
import os
import time
import itertools
import threading
import sys
import platform
import shutil

# System files
import system.help as help
import system.user_acc_management as uam
import system.authentication as authentication
import system.machine_compatibility as ter
# import system.loadapps as apps

# App files
import apps.Calculator

version = "1.0.5 Stable Beta 1"
mach_type = ter.check_machine()
if mach_type == 0:
    try:
        import touchid
    except ImportError as e:
        print("To continue, you must install touchID")
        if platform.system() == "Darwin":
            os.system("pip3 install git+https://github.com/lukaskollmer/python-touch-id")
            import touchid

command = "chess"
if shutil.which(command):
    pass
else:
    print("Installing requirements")
    os.system("pip3 install cl-chess")

if platform.system() not in ["Darwin", "Linux"]:
    if platform.system() == "Windows":
        print("Windows is not compatible with this version of PyOS")
    else:
        print("Your OS is not compatible with this version of PyOS")

# Use python3 pythonOS.py
done = False
def animate():
    for c in itertools.cycle(['.', '..', '...']):
        if done:
            break
        sys.stdout.write('\rOpening ' + program + " " + c)
        sys.stdout.flush()
        time.sleep(0.5)
        ter.clear_ter(mach_type)
    sys.stdout.write('\rDone!     ')
    time.sleep(1)
    ter.clear_ter(mach_type)

is_logged_in, rows = authentication.check_last_logged_in()
retry = 0
if is_logged_in == True:
    while retry == 0:
        ter.clear_ter(mach_type)
        user_choice = input(f"{c.BLUE}user {rows[0]} is logged in.{c.RESET} \nWould you like to continue as {rows[1]}\n(y/n)\n> ")
        if user_choice == "y":
            user_password = input("Enter your pincode \n> ")
            retry2 = 0
            while retry2 == 0:
                if user_password == rows[3]:
                    username = rows[1]
                    user = True
                    retry = 1
                    retry2 = 1
                else:
                    print(f"{c.RED}Passcode is incorrect{c.RESET}")
                    time.sleep(1)
                    ter.clear_ter(mach_type)
                    user_choice = ("Would you like to try again? \n(y/n) \n> ")
                    break

        elif user_choice == "n":
            authentication.logout(rows[1])
            user = False
            retry = 1
        else:
            pass
else:
    username = ""
    user = False

admin_acc = False
runtime = 0

ter.clear_ter(mach_type)
print("PyOS vers", version)
while runtime != 1:
    userprompt = input("> ")
    userprompt = userprompt.strip()  # Remove leading and trailing spaces

    if userprompt in ["help", "?", "h"]:
        # Display general help
        if admin_acc == True:
            help.display_commands(admin=True)
        elif user == True:
            help.display_commands(user=True)
        else:
            help.display_commands()
    elif userprompt.startswith("help ") or userprompt.startswith("? ") or userprompt.startswith("h "):
        # Handle specific command help (e.g., "help -logout")
        parts = userprompt.split(" ", 1)  # Split into command and argument
        if len(parts) > 1 and parts[1].startswith("-"):
            specific_command = parts[1][1:]  # Remove the "-" prefix
            if admin_acc == True:
                help.display_commands(admin=True, specific_command=specific_command)
            elif user == True:
                help.display_commands(user=True, specific_command=specific_command)
            else:
                help.display_commands(specific_command=specific_command)
        else:
            print(f"{c.RED}Invalid argument: {parts[1]}{c.RESET}")
    elif userprompt == "login":
        if user == True:
            print("User already selected")
        else:
            # Use the login system in this program
            user_status, logged_in_user = authentication.login_system()

            if user_status:
                ter.clear_ter(mach_type)
                print(f"User '{logged_in_user}' logged in successfully!")
                username = logged_in_user
                user = True

            else:
                print("Login failed.")
                time.sleep(1)
                print("PyOS vers.", version)

    elif userprompt == "logout":
        if user == True:
            authentication.logout(username)
            print(f"User {username} has been logged out")
            user = False
            time.sleep(1)
            ter.clear_ter(mach_type)
            print("PyOS vers", version)
            username = ""
        else:
            print(f"{c.RED}You must be logged in to perform this command{c.RESET}")

    elif userprompt.startswith("print"):
        if userprompt.startswith("print[") and userprompt.endswith("]"):
            print(userprompt[6:-1])
        elif userprompt.startswith("print") and userprompt.endswith("]") or userprompt.startswith("print[") and not userprompt.endswith("]"):
            print(f"{c.RED}Missing Argument{c.RESET}")
        else:
            print(f"{c.RED}Missing Argument{c.RESET}")

    elif userprompt.startswith("exit"):
        if userprompt in ["exit -force", "exit -f"]:
            ter.clear_ter(mach_type)
            exit()
        elif userprompt == "exit":
            sure = input("Are your sure? \n> ")
            if sure in ["yes", "y", "1"]:
                print("Exiting")
                ter.clear_ter(mach_type)
                exit()
            else:
                ter.clear_ter(mach_type)
                print("PyOS vers", version)
        else:
            print(f"{c.RED} Command not found: {userprompt}{c.RESET}")

    elif userprompt.startswith("admin"):
        if userprompt == "admin -fp":
            if admin_acc == True:
                print("Admin already logged in")
            else:
                if mach_type == 0:
                    auth =ter.fingerprint_trial()
                    if auth == True:
                        admin_acc = True
                        admin_acc = True
                        ter.clear_ter(mach_type)
                        print("PyOS vers", version)
                        print("Admin account")
                        user == True
                        username = "admin"
                    else:
                        print(f"{c.RED}Error: Authenication failed{c.RESET}")
                else:
                    print(f"Machine is not compatible with fingerprint technology type {c.GREEN}\n> admin{c.RESET}")
        elif userprompt == "admin":
            if admin_acc == True:
                print("Admin already logged in")
            else:
                auth = ter.auth_sys(mach_type)
                if auth == True:
                    admin_acc = True
                    ter.clear_ter(mach_type)
                    print("PyOS vers", version)
                    print("Admin account")
                    user == True
                    username = "admin"
                else:
                    print(f"{c.RED}Error: Authenication failed{c.RESET}")
        else:
            print(f"{c.RED}Error: Invalid command{c.RESET}")

    elif userprompt in ["clear", "clr"]:
        ter.clear_ter(mach_type)
        print("PyOS vers", version)
        if admin_acc == True:
            print("Admin account")

    elif userprompt == "calc":
        if user == True or admin_acc == True:
            ter.clear_ter(mach_type)
            program = "Calculator"
            t = threading.Thread(target=animate)
            t.start()

            time.sleep(5)
            done = True
            time.sleep(2)
            apps.Calculator.calculator()
            ter.clear_ter(mach_type)
            print("PyOS vers", version)
            if admin_acc == True:
                print("Admin Account")
        else:
            print(f"{c.RED}Error: User must be logged in to use this{c.RESET}")

    elif userprompt.startswith("user"):
        if userprompt in ["user -a", "user -active"]:
            if username == "":
                print(f"{c.RED}No user{c.RESET}")
            else:
                print(username)
            print(" Is admin: \n", bool(admin_acc))

        else:
            if admin_acc == True:
                if userprompt == "user":
                    uam.uam_menu()
                elif userprompt in ["user -help"]:
                    print(f"user {c.BLUE}-arg{c.RESET}")
                    print("Available commands:")
                    print(f"{c.GREEN}-help    {c.BLUE}Shows help about user argument")
                    print(f"{c.GREEN}-add     {c.BLUE}Add another user")
                    print(f"{c.GREEN}-list    {c.BLUE}View all users")
                    print(f"{c.GREEN}-modify  {c.BLUE}Edit a user")
                    print(f"{c.GREEN}-remove  {c.BLUE}Removes a user")
                elif userprompt == "user -list":
                    show_passwords = input("Show passwords? (y/n): ")
                    if show_passwords in ["y", "1"]:
                        try:
                            verify_fp = touchid.authenticate()
                        except Exception:
                            print("Could not verify admin")
                            uam.list_users()
                        if verify_fp == True:
                            uam.list_users(show_passwords)
                        else:
                            uam.list_users()
                    else:
                        uam.list_users()
                elif userprompt == "user -add":
                    uam.add_user()
                elif userprompt == "user -remove":
                    uam.remove_user()
                elif userprompt == "user -modify":
                    uam.modify_user()
            else:
                print(f"{c.RED}Admin permissions required{c.RESET}")

    elif userprompt == "ccommand":
        if admin_acc == True:
            help.create_new_command()
        else:
            print(f"{c.RED}Admin permissions required{c.RESET}")

    elif userprompt.startswith("debug"):
        if userprompt == "debug -colour":
            y = 0
            while True:
                colours = c.ALLCOLORS

                total_colour = len(colours)
                if y == total_colour:
                    print(f"\n{c.RESET}Complete")
                    break

                print(f"{colours[y]}Hello")
                y = y + 1
        elif userprompt in ["debug", "debug "]:
            print(f"{c.RED}Error: Debug function name required{c.RESET}")
        else:
            print(f"{c.RED}Error: Function doesn't exist{c.RESET}")

    elif userprompt == "machine":
        if platform.system() == "Darwin":
            print(f"System OS: MacOS \nOS Version: {platform.release()}")
    elif userprompt == "chess":
        if user == True:
            program = "Chess"
            t = threading.Thread(target=animate)
            t.start()
            time.sleep(5)
            done = True
            time.sleep(2)

            os.system("chess")
            ter.clear_ter(mach_type)
            print("PyOS vers", version)
        else:
            print(f"{c.RED}Error: User must be logged in to use this{c.RESET}")
    elif userprompt in [""]:
        pass
    else:
        print(f"{c.RED} Command not found: {userprompt}{c.RESET}")