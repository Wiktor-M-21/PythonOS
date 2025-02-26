import platform
import os
import system.colours as c
if platform.system() == "Darwin":
    import touchid


def check_machine():
    machine = platform.system()
    if machine == "Darwin":
        touchid_avail = touchid.is_available()
        if touchid_avail:
            machine_type = 0
            return machine_type
        else:
            machine_type = 2
            return machine_type
    elif machine == "windows":
        machine_type = 1
        return machine_type
    elif machine == "Linux":
        machine_type = 2
        return machine_type

correctpin = "2105"

def auth_sys(machine_type):
    if machine_type == 0:
        user_choice = input("Would you like to verify with fingerprint? (y/n) \n>")
        if user_choice == "y":
            auth = False
            try:
                auth = touchid.authenticate()
            except:
                pass
            if auth == True:
                return True
            else:
                return False
        elif user_choice == "n":
            code = False
            pincode = input("Please input code \n> ")
            if pincode == correctpin:
                print("Authentication Successful")
                return True
            else:
                print(f"{c.RED}Authentication Failed: Invalid Code{c.RESET}")
                return False
        else:
            return False
    else:
        print("TouchID is not available")
        pincode = input("Please input code \n> ")
        if pincode == correctpin:
            print(f"{c.GREEN}Authentication Successful{c.RESET}")
            return True
        else:
            print("Authentication Failed: Invalid Code")
            return False

def clear_ter(machine_type):
    if machine_type == 0 or machine_type == 2:
        os.system("clear")
    elif machine_type == 1:
        os.system("cls")
    else:
        print("ERROR")