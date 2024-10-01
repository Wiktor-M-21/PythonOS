import system.colours as c
import os

def calculator():
    calc_running = True
    print(f"Please enter an equation \n{c.BLUE}If you need help type ?{c.RESET}")
    while calc_running == True:
        user_equation = input("> ")
        if user_equation in ["help","h","?"]:
            print("Here are all available commands and operators")
            print(f"{c.GREEN}exit  {c.BLUE}exits this program")
            print(f"{c.RESET}You can use the following operators...")
            print(f"{c.GREEN}+     {c.BLUE}Addition        ")
            print(f"{c.GREEN}-     {c.BLUE}Subtraction     ")
            print(f"{c.GREEN}*     {c.BLUE}Multiplication  ")
            print(f"{c.GREEN}/     {c.BLUE}Division        ")
            print(f"{c.GREEN}%     {c.BLUE}Modulas         {c.YELLOW}Remainder of a division")
            print(f"{c.GREEN}**    {c.BLUE}Exponent        {c.YELLOW}Powers")
            print(f"{c.GREEN}//    {c.BLUE}Floor division  {c.YELLOW}Rounds to the nearest intiger")
            print(f"{c.RESET}")
        elif user_equation == "exit":
            break
        elif user_equation == "clear":
            os.system("clear")

        else:
            try:
                solution = eval(user_equation)
                print(solution)
            except SyntaxError:
                print(f"{c.RED}Error{c.RESET}")
            except NameError:
                print(f"{c.RED}Error: Do not use names{c.RESET}")
            except ZeroDivisionError:
                print(f"{c.RESET}Error: Division by 0{c.RESET}")