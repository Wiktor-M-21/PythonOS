import system.colours as c
import os
import re
import touchid
import time
import itertools
import threading
import sys
import system.help as help
import apps.calc
import system.user_acc_management as uam
import system.login as login
import platform
from getpass import getpass

#Use python3 pythonOS.py
done = False
#here is the animation
def animate():
    for c in itertools.cycle(['.', '..', '...']):
        if done:
            break
        sys.stdout.write('\rOpening '+ program + " " + c)
        sys.stdout.flush()
        time.sleep(0.5)
        os.system("clear")
    sys.stdout.write('\rDone!     ')
    time.sleep(1)
    os.system("clear")

if platform.system() not in ["Darwin","Linux"]:
    if platform.system() == "Windows":
        print("Windows is not compatible with this version of PyOS")
    else:
        print("Your OS is not compatible with this version of PyOS")


username = ""
admin_acc = False
version = "1.0"
user = False
runtime = 0
os.system("clear")
print("PyOS vers",version)
while runtime != 1:
    userprompt = input("> ")
    while True:
        try:
            if " " == list(userprompt)[0]:
                userprompt = "".join(list(userprompt)[1:])
            else:
                break
        except:
            break
    if userprompt in ["help","?"]:
        if admin_acc == True:
            help.display_commands(admin=True)
        elif user == True:
            help.display_commands(user=True)
        else:
            help.display_commands()
    elif userprompt == "login":
        if user == True:
            print("User already selected")
        else:
            # Use the login system in this program
            user_status, logged_in_user = login.login_system()

            if user_status:
                os.system("clear")
                print(f"User '{logged_in_user}' logged in successfully!")
                username = logged_in_user
                user = True

            else:
                print("Login failed.")
                time.sleep(1)
                print("PyOS vers.",version)
                                

    elif userprompt.startswith("print"):
        if userprompt.startswith("print[") and userprompt.endswith("]"):
            print(userprompt[6:-1])
        elif userprompt.startswith("print") and userprompt.endswith("]") or userprompt.startswith("print[") and not userprompt.endswith("]"):
            print(f"{c.RED}Missing Argument{c.RESET}")
        else:
            print(f"{c.RED}Missing Argument{c.RESET}")
    elif userprompt.startswith("exit"):
        if userprompt in ["exit -force","exit -f"]:
            os.system("clear")
            exit()
        elif userprompt == "exit":
            sure = input("Are your sure? \n> ")
            if sure in ["yes","y","1"]:
                print("Exiting")
                os.system("clear")
                exit()
            else:
                os.system("clear")
                print("PyOS vers",version)
        else:
            print(f"{c.RED} Command not found: {userprompt}{c.RESET}")
    
    elif userprompt.startswith("admin"):
        if admin_acc == True:
            print("Admin already logged in")
        else:
            if userprompt == "admin -2105":
                admin_acc = True
                os.system("clear")
                print("PyOS vers",version)
                print("Admin account")
                user == True
                username = "admin"
            elif userprompt == "admin -fp":
                try:
                    fp_admin = touchid.authenticate(reason="access Admin")
                except:
                    fp_admin = False
                if fp_admin == True:
                    admin_acc = True
                    os.system("clear")
                    print("PyOS vers",version)
                    print("Admin account")
                    user == True
                    username = "admin"
                else:
                    print("Authenication failed")
            elif userprompt.startswith("admin -") and re.search("[8,9,10,11]",userprompt):
                print(f"{c.RED}Wrong auth code{c.RESET}")
            elif userprompt == "admin":
                print(f"{c.RED}Auth code required{c.RESET}")
            elif userprompt.startswith("admin -") and len(userprompt) > 11:
                print(f"{c.RED}Auth code invalid")
            else:
                print(f"{c.RED}Invalid syntax{c.RESET}")

    elif userprompt in ["clear","clr"]:
        os.system("clear")
        print("PyOS vers",version)
        if admin_acc == True:
            print("Admin account")
    elif userprompt == "calc":
            if user == True or admin_acc == True:
                os.system("clear")
                program = "Calculator"
                t = threading.Thread(target=animate)
                t.start()
                
                time.sleep(5)
                done = True
                time.sleep(2)
                apps.calc.calculator()
                os.system("clear")
                print("PyOS vers",version)
                if admin_acc == True:
                    print("Admin Account")
            else:
                print("User must be logged in to use this")
    elif userprompt.startswith("user"):
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
                    if show_passwords in ["y","1"]:
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
            if userprompt in ["user -active","user -a"]:
                print(username)
                print("Is admin \n",admin_acc.__bool__)
            else:
                print(f"{c.RED}Admin permissions required{c.RESET}")

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
            os.system("clear")
            print("PyOS vers",version)
        else:
            print(f"User must be logged in to use this")
    elif userprompt in [""]:
        pass
    else:
        print(f"{c.RED} Command not found: {userprompt}{c.RESET}")