import platform
import os
import system.colours as c
if platform.system() == "Darwin":
    import touchid


def check_machine():
    machine = platform.system()
    global machine_type
    if machine == "Darwin":
        touchid_avail = touchid.is_available()
        if touchid_avail == True:
            machine_type = 0
            return 0
        else:
            machine_type = 1
            return 1
    elif machine == "windows":
        machine_type = 2
        return 2
    elif machine == "Linux":
        machine_type = 3
        return 3


def auth_sys(owner_pin):
    if machine_type == 0:
        while True:
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
                    print("Error verification unsuccessful")
            elif user_choice == "n":
                code = False
                pincode = input("Please input code \n> ")
                if pincode == owner_pin:
                    print("Authentication Successful")
                    return True
                else:
                    print(f"{c.RED}Authentication Failed: Invalid Code{c.RESET}")
                    return False
            elif user_choice == "exit":
                print("Exiting...")
                return False
            else:
                return False
    else:
        print("TouchID is not available")
        pincode = input("Please input code \n> ")
        if pincode == owner_pin:
            print(f"{c.GREEN}Authentication Successful{c.RESET}")
            return True
        else:
            print("Authentication Failed: Invalid Code")
            return False

def clear_ter():
    if machine_type == 0 or machine_type == 3:
        os.system("clear")
    elif machine_type == 2:
        os.system("cls")
    else:
        print("ERROR")

def fingerprint_trial():
    auth = False
    try:
        auth = touchid.authenticate()
        if auth == True:
            return True
        else:
            return False
    except:
        pass