import system.colours as c
import os
import math

version = 1.3

def clear():
    os.system("clear")
    print(f"Calculator vers {version}")
    print(f"Please enter an equation or command\n{c.BLUE}If you need help type: \"?\"{c.RESET}")

def calculator():
    calc_running = True
    print(f"Calculator vers {version}")
    print(f"Please enter an equation or command\n{c.BLUE}If you need help type: \"?\"{c.RESET}")
    while calc_running == True:
        user_equation = input("> ")
        if user_equation in ["help","h","?"]:
            print("Here are all available commands and operators")
            print(f"{c.GREEN}?        {c.BLUE}Help                                 {c.YELLOW}Exits the program: args: -f to force exit OS")
            print(f"{c.GREEN}exit     {c.BLUE}Exits                                {c.YELLOW}Exits the program: args: -f to force exit OS")
            print(f"{c.GREEN}base     {c.BLUE}Binary, Denary and Hex converter     {c.YELLOW}Converts Binary, Denary or Hex to each other")
            print(f"{c.GREEN}pyth     {c.BLUE}Pythagoras                           {c.YELLOW}Calculates lengths of triangles")
            print(f"{c.GREEN}trig     {c.BLUE}Triginometry                         {c.YELLOW}Calculates angles and lengths in right angled triangles")
            print(f"{c.RESET}You can use the following operators...")
            print(f"{c.GREEN}+        {c.BLUE}Addition                             ")
            print(f"{c.GREEN}-        {c.BLUE}Subtraction                          ")
            print(f"{c.GREEN}*        {c.BLUE}Multiplication                       ")
            print(f"{c.GREEN}/        {c.BLUE}Division                             ")
            print(f"{c.GREEN}%        {c.BLUE}Modulas                              {c.YELLOW}Remainder of a division")
            print(f"{c.GREEN}**       {c.BLUE}Exponent                             {c.YELLOW}Powers")
            print(f"{c.GREEN}//       {c.BLUE}Floor division                       {c.YELLOW}Rounds to the nearest intiger")
            print(f"{c.GREEN}v        {c.BLUE}Square root                          {c.YELLOW}Reverse of powers giving the number used to multiply together to get number inputed")
            print(f"{c.RESET}")
        elif user_equation.startswith(("help ", "h ", "? ")):  # Check for specific operator help
            parts = user_equation.split(" ")
            if len(parts) > 1:
                operator = parts[1]

                help_messages = {
                    "+": "Addition: Adds two numbers together. Example: 3 + 2 = 5",
                    "-": "Subtraction: Subtracts the second number from the first. Example: 5 - 3 = 2",
                    "*": "Multiplication: Multiplies two numbers. Example: 4 * 3 = 12",
                    "/": "Division: Divides the first number by the second. Example: 6 / 2 = 3.0",
                    "%": "Modulus: Gives the remainder of a division. Example: 7 % 3 = 1",
                    "**": "Exponent: Raises the first number to the power of the second. Example: 2 ** 3 = 8",
                    "//": "Floor Division: Divides and rounds down to the nearest integer. Example: 7 // 3 = 2",
                    "?": "Brings up all functions and commands that are available only usable in the main command line of the Calculator. Add a command at the end to learn about a specific command and an example usage of it. Example: help -",
                    "v": "Square root: Returns the square root of a number. Example: v9 = 3.0",
                    "h": "Brings up all functions and commands that are available only usable in the main command line of the Calculator. Add a command at the end to learn about a specific command and an example usage of it. Example: help -",
                    "exit": "Allows the user to exit this program. Functional at any input line",
                    "help": "Brings up all functions and commands that are available only usable in the main command line of the Calculator. Add a command at the end to learn about a specific command and an example usage of it. Example: help -",
                    "base": "Base 2,10,16: Calculates between Binary (Base 2), Denary (Base 10) and Hexadecimal (Base 16). Example: 10110010 = 178 = B2",
                    "pyth": "Pythagoras: Allows you to calculate a third side of a triangle with 2 sides. Example: A = 3, B = 4 C = 5",
                    "trig": "Trigometry: Calculate sides with adjacent angles. ",
                }

                if operator in help_messages:
                    print(f"{c.GREEN}{operator.ljust(9)}{c.BLUE}{help_messages[operator]}{c.RESET}")
                else:
                    print(f"{c.RED}Unknown operator: {operator}. Try '? +' for help with addition.{c.RESET}")


        elif user_equation.startswith("exit"):
            if user_equation == "exit":
                break
            if user_equation == "exit -f":
                quit()
        elif user_equation == "clear":
            clear()


        elif user_equation == "pyth":
            print("Pythagoras Calculator")
            intro = input("Introduction? (y/n)\n>")
            if intro == "y":
                print(f"{c.BLUE}Introduction")
                print(f"{c.RESET}A and B = Shorter sides\nC = Hypotenuse")
                print(f"{c.GREEN}Type \"calc\" for number to be calculated")
                print(f"At any point type \"exit\" to exit the pythagoras module{c.RESET}")
            elif intro == "exit":
                    clear()
                    continue    

            while True:
                apyth = input("A = ")
                if apyth == "exit":
                    clear()
                    break
                bpyth = input("B = ")
                if bpyth == "exit":
                    clear()
                    break
                cpyth = input("C = ")
                if cpyth == "exit":
                    clear()
                    break

                inputs = [apyth, bpyth, cpyth]
                calc_count = inputs.count("calc")
                number_count = sum(1 for x in inputs if x.isdigit())
                
                if calc_count != 1 or number_count != 2:
                    print(f"{c.RED}Calc Error: Exactly one value must be 'calc' and the other two must be numbers.{c.RESET}")
                    continue

                if cpyth == "calc": # Calculate C
                    print("Calculating the Hypotenuse")
                    apyth = int(apyth)
                    bpyth = int(bpyth)
                    resulta = apyth ** 2
                    resultb = bpyth ** 2
                    resultc = resulta + resultb
                    result = math.sqrt(resultc)
                    print(f"Side C: {round(result,3)}")
                    break

                elif apyth == "calc":  # Calculate A
                    print("Calculating Side A")
                    bpyth = int(bpyth)
                    cpyth = int(cpyth)
                    
                    if cpyth ** 2 - bpyth ** 2 < 0:
                        print(f"{c.RED}Calc Error: Invalid input. Hypotenuse must be the longest side.{c.RESET}")
                    else:
                        result = math.sqrt(cpyth ** 2 - bpyth ** 2)
                        print(f"Side A is: {round(result,3)}")

                elif bpyth == "calc":  # Calculate B
                    print("Calculating Side B")
                    apyth = int(apyth)
                    cpyth = int(cpyth)

                    if cpyth ** 2 - apyth ** 2 < 0:
                        print(f"{c.RED}Calc Error: Invalid input. Hypotenuse must be the longest side.{c.RESET}")
                    else:
                        result = math.sqrt(cpyth ** 2 - apyth ** 2)
                        print(f"Side B is: {round(result,3)}")
                        break
                
                else:
                    print(f"{c.RED}Calc Error: Unkown reason")
        
        elif user_equation == "trig":
            print("Triginometry calculator")
            intro = input("Introduction? (y/n)\n> ").lower()
            if intro == "y":
                print(f"{c.BLUE}Introduction")
                print(f"{c.RESET}This tool calculates missing angles or side lengths in right-angled triangles.")
                print(f"{c.GREEN}Type \"calc\" for the value you want to find.")
                print(f"{c.GREEN}Press enter ⏎ for the side that doesn't apply.")
                print(f"At any point, type \"exit\" to return to the main menu.{c.RESET}")
            elif intro == "exit":
                    clear()
                    continue
            
            while True:
                print("\nWhich values do you have?")
                angle = input("Angle (degrees) = ").strip().lower()
                if angle == "exit":
                    clear()
                    break
                elif angle.isalpha() and angle != "calc":
                    print(f"{c.RED}Error: Cannot use letters{c.RESET}")
                    continue
                elif angle == "":
                    angle = None
                else:
                    angle = float(angle)

                opposite = input("Opposite side = ").strip().lower()
                if opposite == "exit":
                    clear()
                    break
                elif opposite.isalpha() and opposite != "calc":
                    print(f"{c.RED}Error: Cannot use letters{c.RESET}")
                    continue
                elif opposite == "":
                    opposite = None
                elif opposite != "calc":
                    opposite = float(opposite)

                adjacent = input("Adjacent side = ").strip().lower()
                if adjacent == "exit":
                    clear()
                    break
                elif adjacent.isalpha() and adjacent != "calc":
                    print(f"{c.RED}Error: Cannot use letters{c.RESET}")
                    continue
                elif adjacent == "":
                    adjacent = None
                elif adjacent != "calc":
                    adjacent = float(adjacent)

                hypotenuse = input("Hypotenuse = ").strip().lower()
                if hypotenuse == "exit":
                    clear()
                    break
                elif hypotenuse.isalpha() and hypotenuse != "calc":
                    print(f"{c.RED}Error: Cannot use letters{c.RESET}")
                    continue
                elif hypotenuse == "":
                    hypotenuse = None
                elif hypotenuse != "calc":
                    hypotenuse = float(hypotenuse)

                # Validate input: Must have at least one side and optionally an angle
                given_sides = sum(1 for x in [opposite, adjacent, hypotenuse] if isinstance(x, float))
                if given_sides == 0:
                    print(f"{c.RED}Error: You must provide at least one side.{c.RESET}")
                    continue
                if given_sides == 1 and angle is None:
                    print(f"{c.RED}Error: You must provide an angle if you only give one side.{c.RESET}")
                    continue

                if angle is not None:
                    angle_rad = math.radians(angle)

                # Calculate missing values
                if opposite == "calc":
                    if hypotenuse is not None:
                        opposite = hypotenuse * math.sin(angle_rad)
                    elif adjacent is not None:
                        opposite = adjacent * math.tan(angle_rad)

                if adjacent == "calc":
                    if hypotenuse is not None:
                        adjacent = hypotenuse * math.cos(angle_rad)
                    elif opposite is not None:
                        adjacent = opposite / math.tan(angle_rad)

                if hypotenuse == "calc":
                    if opposite is not None:
                        hypotenuse = opposite / math.sin(angle_rad)
                    elif adjacent is not None:
                        hypotenuse = adjacent / math.cos(angle_rad)

                if angle is None:  # Calculate angle if not given
                    if opposite is not None and hypotenuse is not None:
                        angle = math.degrees(math.asin(opposite / hypotenuse))
                    elif adjacent is not None and hypotenuse is not None:
                        angle = math.degrees(math.acos(adjacent / hypotenuse))
                    elif opposite is not None and adjacent is not None:
                        angle = math.degrees(math.atan(opposite / adjacent))

                # Display results
                if angle is not None:
                    print(f"The angle is: {angle:.2f}°")
                if opposite is not None:
                    print(f"The opposite side is: {opposite:.2f}")
                if adjacent is not None:
                    print(f"The adjacent side is: {adjacent:.2f}")
                if hypotenuse is not None:
                    print(f"The hypotenuse is: {hypotenuse:.2f}")

                break
        elif user_equation == "base":
            print("Base number calculator")
            print("Select from below the system your digits are in")
            print(f"{c.GREEN}1. Binary (base 2){c.RESET}")
            print(f"{c.GREEN}2. Denary (base 10){c.RESET}")
            print(f"{c.GREEN}3. Hexadecimal (base 16){c.RESET}")
            while True:
                baseselect = input("> ")
                baseselect = baseselect.lower()
                if baseselect == "binary" or baseselect == "1":
                    print("Binary")
                    print("Input a valid binary number")
                    while True:
                        digit = input("> ")
                        if set(digit) <= {"0", "1"}:
                            print(f"Denary: {int(digit, 2)}")
                            print(f"Hexadecimal: {hex(int(digit, 2))[2:]}")
                            print("")
                            print("Select from below the system your digits are in")
                            print(f"{c.GREEN}1. Binary (base 2){c.RESET}")
                            print(f"{c.GREEN}2. Denary (base 10){c.RESET}")
                            print(f"{c.GREEN}3. Hexadecimal (base 16){c.RESET}")
                            break
                        else:
                            print(f"{c.RED}Error: Invalid format{c.RESET}")
                            continue
                elif baseselect == "denary" or baseselect == "2":
                    print("Denary")
                    print("Input a valid Denary number")
                    while True:
                        digit = input("> ")
                        if digit.isdigit():
                            print(f"Binary: {bin(int(digit, 10))[2:]}")
                            print(f"Hexadecimal: {hex(int(digit, 10))[2:]}")
                        elif digit == "exit":
                            print("Returning to Base Number Calculator")
                            print("Select from below the system your digits are in")
                            print(f"{c.GREEN}1. Binary (base 2){c.RESET}")
                            print(f"{c.GREEN}2. Denary (base 10){c.RESET}")
                            print(f"{c.GREEN}3. Hexadecimal (base 16){c.RESET}")
                            break
                        else:
                            print(f"{c.RED}Error: Invalid format{c.RESET}")
                            continue
                elif baseselect in ["hex","hexadecimal","3"]:
                    print("Hexadecimal")
                    print("Input a valid hexadecimal number")
                    while True:
                        digit = input("> ")
                        if set(digit) <= set("0123456789ABCDEFabcdef"):
                            print(f"Binary: {bin(int(digit, 16))[2:]}")
                            print(f"Decimal: {int(digit, 16)}")
                        elif digit == "exit":
                            print("Returning to Base Number Calculator")
                            print("Select from below the system your digits are in")
                            print(f"{c.GREEN}1. Binary (base 2){c.RESET}")
                            print(f"{c.GREEN}2. Denary (base 10){c.RESET}")
                            print(f"{c.GREEN}3. Hexadecimal (base 16){c.RESET}")
                            break
                
                        else:
                            print(f"{c.RED}Error: Invalid format{c.RESET}")
                            continue
                elif baseselect == "exit":
                        break
                        
                    


        elif user_equation.startswith("v"):
            try:
                sqrteq = float(user_equation[1:])
                solutionsqrt = math.sqrt(sqrteq)
                print(solutionsqrt)
            except ValueError:
                print(f"{c.RED}Calc Error: Syntax{c.RESET}")

        else:
            try:
                solution = eval(user_equation)
                print(solution)
            except SyntaxError:
                print(f"{c.RED}Calc Error: Syntax{c.RESET}")
            except NameError:
                print(f"{c.RED}Calc Error: Do not use names{c.RESET}")
            except ZeroDivisionError:
                print(f"{c.RESET}Calc Error: Division by 0{c.RESET}")

calculator()