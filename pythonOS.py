import system.colours as c
import os
import time
import itertools
import threading
import sys
import platform
import shutil
import getpass

# System files
import system.help as help
import system.user_acc_management as uam
import system.machine_compatibility as ter
import system.updates as update
# import system.loadapps as apps

# App files
import apps.Calculator

version = "1.3"


username_str = ""
admin_int = 0


mach_type = ter.check_machine()
if platform.system() not in ["Darwin", "Linux"]:
    if platform.system() == "Windows":
        print("Windows is not compatible with this version of PyOS")
        quit()
    else:
        print("Your OS is not compatible with this version of PyOS")
# Use python3 pythonOS.py
if mach_type == 0:
    try:
        import touchid
    except ImportError as e:
        print("To continue, you must install touchID")
        if platform.system() == "Darwin":
            os.system("pip3 install git+https://github.com/lukaskollmer/python-touch-id")
            import touchid

try:
    import rsa
except ImportError as e:
    print("To continue, you must install rsa")
    os.system("pip3 install rsa")
    import rsa


command = "chess"
if shutil.which(command):
    pass
else:
    print("Installing requirements")
    os.system("pip3 install cl-chess")

done = False
def animate():
    for c in itertools.cycle(['.', '..', '...']):
        if done:
            break
        sys.stdout.write('\rOpening ' + program + " " + c)
        sys.stdout.flush()
        time.sleep(0.5)
        ter.clear_ter()
    sys.stdout.write('\rDone!     ')
    time.sleep(1)
    ter.clear_ter()

ter.clear_ter()
acc_type_int, username_str, pin = uam.last_boot_logged_in()

if acc_type_int == 1:
    user_bool = True
    admin_int = 1
elif acc_type_int == 2:
    user_bool = True
    admin_int = 2
elif acc_type_int == 3:
    user_bool = True
else:
    user_bool = False



update.check_for_updates()
ter.clear_ter()
print("PyOS vers", version)
if update.check_for_updates == False:
    print("A newer version is available type version command to find out more")
while True:
    userprompt = input("> ")
    userprompt = userprompt.strip()  # Remove leading and trailing spaces

    if userprompt in ["help", "?", "h"]:
        # Display general help
        if admin_int >= 1:
            help.display_commands(admin=True)
        elif user_bool == True:
            help.display_commands(user=True)
        else:
            help.display_commands()
    elif userprompt.startswith("help ") or userprompt.startswith("? ") or userprompt.startswith("h "):
        # Handle specific command help (e.g., "help -logout")
        parts = userprompt.split(" ", 1)  # Split into command and argument
        if len(parts) > 1 and parts[1].startswith("-"):
            specific_command = parts[1][1:]  # Remove the "-" prefix
            if admin_int >= 1:
                help.display_commands(admin=True, specific_command=specific_command)
            elif user_bool == True:
                help.display_commands(user_bool=True, specific_command=specific_command)
            else:
                help.display_commands(specific_command=specific_command)
        else:
            print(f"{c.RED}Invalid argument: {parts[1]}{c.RESET}")
            
    elif userprompt.startswith("log"):
        if userprompt == "log -i":
            if user_bool == True:
                print("User already selected")
            else:
                # Use the login system in this program
                username_str, admin_int, pin = uam.login_system()
                if username_str != "":
                    username_bool = True
                else:
                    username_bool = False

                if username_bool:
                    ter.clear_ter()
                    print(f"User '{username_str}' logged in successfully!")
                    time.sleep(3)
                    user_bool = True
                if admin_int >= 1:
                    print("PyOS vers", version)
                    print(f"Admin account: {username_str}")
                elif admin_int == 2:
                    print("PyOS vers", version)
                    print(f"Owner account: {username_str}")


        elif userprompt == "log -o":
            if user_bool == True:
                uam.logout(username_str)
                print(f"User {username_str} has been logged out")
                user_bool = False
                admin_int = 0
                time.sleep(1)
                ter.clear_ter()
                print("PyOS vers", version)
                username_str = ""
            else:
                print(f"{c.RED}Error: You must be logged in to perform this command{c.RESET}")
        elif userprompt == "login":
            print("Use log -i to log in")

        elif userprompt == "logout":
            if user_bool == True:
                print("Use log -o to log out")
            else:
                print(f"{c.RED}Error: You must be logged in to perform this command{c.RESET}")
        else:
            print(f"{c.RED}Error: Command not found{c.RESET}")

    elif userprompt.startswith("print"):
        if userprompt.startswith("print[") and userprompt.endswith("]"):
            print(userprompt[6:-1])
        elif userprompt.startswith("print") and userprompt.endswith("]") or userprompt.startswith("print[") and not userprompt.endswith("]"):
            print(f"{c.RED}Missing Argument{c.RESET}")
        else:
            print(f"{c.RED}Missing Argument{c.RESET}")

    elif userprompt.startswith("exit"):
        if userprompt in ["exit -force", "exit -f"]:
            ter.clear_ter()
            exit()
        elif userprompt == "exit":
            if user_bool == False:
                sure = input("Are your sure? (y/n) \n> ")
                if sure in ["yes", "y", "1"]:
                    print("Exiting")
                    ter.clear_ter()
                    exit()
                else:
                    ter.clear_ter()
                    print("PyOS vers", version)
            elif user_bool == True:
                logout = input("Would you like to logout? (y/n)\n> ")
                if logout in ["yes", "y", "1"]:
                    uam.logout(username_str)
                    print("Exiting")
                    ter.clear_ter()
                    exit()
                else:
                    ter.clear_ter()
                    print("PyOS vers", version)


        else:
            print(f"{c.RED} Command not found: {userprompt}{c.RESET}")

    elif userprompt in ["clear", "clr"]:
        ter.clear_ter()
        print("PyOS vers", version)
        if admin_int >= 1:
            print("Admin account")
    elif userprompt in ["vers","version"]:
        update.check_for_updates()

    elif userprompt == "calc":
        if user_bool == True:
            ter.clear_ter()
            program = "Calculator"
            t = threading.Thread(target=animate)
            t.start()

            time.sleep(5)
            done = True
            time.sleep(2)
            apps.Calculator.calculator()
            ter.clear_ter()
            print("PyOS vers", version)
            if admin_int >= 1:
                print("Admin Account")
        else:
            print(f"{c.RED}Error: User must be logged in to use this{c.RESET}")

    elif userprompt.startswith("user"):
        if admin_int >= 1:
            if userprompt == "user":
                uam.uam_menu(username_str,admin_int,pin)
            elif userprompt == "user -list":
                auth = uam.admin_auth(admin_int,pin)
                if auth == True:
                    print("Authorisation failed")
                    uam.list_users(True)
                else:
                    print("Authorisation failed")
            elif userprompt == "user -add":
                auth = uam.admin_auth(admin_int,pin)
                if auth == True:
                    print("Authorisation failed")
                    uam.add_user()
                else:
                    print("Authorisation failed")
            elif userprompt == "user -remove":
                auth = uam.admin_auth(admin_int,pin)
                if auth == True:
                    print("Authorisation failed")
                    uam.remove_user()
                else:
                    print("Authorisation failed")
            elif userprompt == "user -modify":
                auth = uam.admin_auth(admin_int,pin)
                if auth == True:
                    print("Authorisation failed")
                    uam.modify_user(username_str)
                else:
                    print("Authorisation failed")
            else:
                print(f"{c.RED}Error: Command not found{c.RESET}")

    elif userprompt == "ccommand":
        if admin_int >= 1:
            auth = uam.admin_auth(admin_int,pin)
            if auth == True:
                print("Authorisation failed")
                help.create_new_command()
            else:
                print("Authorisation failed")
        else:
            print(f"{c.RED}Error: Command not found{c.RESET}")

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
        elif userprompt == "debug -user":
            if username_str == "":
                print(f"{c.RED}No user{c.RESET}")
            else:
                print(username_str)
            print(f" Is admin:{admin_int}")
        
        elif userprompt in ["debug", "debug "]:
            print(f"{c.RED}Error: Debug function name required{c.RESET}")
        else:
            print(f"{c.RED}Error: Function doesn't exist{c.RESET}")

    elif userprompt == "machine":
        if mach_type == 0:
            print(f"System OS: MacOS \nOS Version: {platform.release()}")
            print(f"TouchID compatible")
        elif mach_type == 1:
            print(f"System OS: MacOS \nOS Version: {platform.release()}")
        elif mach_type == 2:
            print(f"System OS: Windows \nOS Version: {platform.release()}")
        elif mach_type == 3:
            print(f"System OS: Linux \nOS Version: {platform.release()}")
        else:
            print(f"{c.RED}Error: Could not find machine information{c.RESET}")
    elif userprompt == "chess":
        if user_bool == True:
            program = "Chess"
            t = threading.Thread(target=animate)
            t.start()
            time.sleep(5)
            done = True
            time.sleep(2)

            os.system("chess")
            ter.clear_ter()
            print("PyOS vers", version)
        else:
            print(f"{c.RED}Error: User must be logged in to use this{c.RESET}")
    elif userprompt in [""]:
        pass
    else:
        print(f"{c.RED} Command not found: {userprompt}{c.RESET}")