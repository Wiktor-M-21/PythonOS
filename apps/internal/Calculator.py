import system.colours as c
import os
import math
import textwrap

version = "1.3.1"

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
            print(f"{c.GREEN}?        {c.BLUE}Help                                 {c.YELLOW}Shows this help output giving all commands available")
            print(f"{c.GREEN}exit     {c.BLUE}Exits                                {c.YELLOW}Exits the program: args: -f to force exit OS")
            print(f"{c.GREEN}base     {c.BLUE}Binary, Denary and Hex converter     {c.YELLOW}Converts Binary, Denary or Hex to each other")
            print(f"{c.GREEN}pyth     {c.BLUE}Pythagoras                           {c.YELLOW}Calculates lengths of triangles")
            print(f"{c.GREEN}trig     {c.BLUE}Triginometry                         {c.YELLOW}Calculates angles and lengths in right angled triangles")
            print(f"{c.GREEN}snco     {c.BLUE}Sine and Cosine rule                 {c.YELLOW}Allows for calculation of sides and angles using sine and cosine rule")
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
        elif user_equation.startswith(("help -", "h -", "? -")):  # Check for specific operator help
            parts = user_equation.split(" -")
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
                    "?": "Displays available commands. Use '? -<command>' to get details. Example: help -+",
                    "v": "Square root: Returns the square root of a number. Example: v9 = 3",
                    "h": "Displays available commands. Use 'h -<command>' to get details. Example: help -+",
                    "exit": "Exits the program. Works at any input line.",
                    "help": "Displays available commands. Use 'help -<command>' to get details. Example: help -+",
                    "base": "Number Base Conversion: Converts between Binary (Base 2), Decimal (Base 10), and Hexadecimal (Base 16). Example: 10110010 = 178 = B2",
                    "pyth": "Pythagorean Theorem: Calculates the third side of a right triangle given two sides. Example: A = 3, B = 4, C = 5",
                    "trig": "Trigonometry: Calculates sides or angles using sine, cosine, or tangent. Example: Find the opposite side given hypotenuse = 10 and angle = 30° → opposite = 10 * sin(30) = 5",
                    "snco": "Sine and Cosine Rule: Solves for sides and angles in non-right triangles. Example: Using the Sine Rule: If A = 40°, a = 8, and B = 60°, then b = (8 * sin(60)) / sin(40) ≈ 11.5",
                }

                if operator in help_messages:
                    description = help_messages[operator]
                    indent_size = 12  # Consistent spacing
                    formatted_text = textwrap.fill(
                        description,
                        width=120 - indent_size,  # Adjust width to avoid early breaks
                        subsequent_indent=" " * indent_size  # Ensures continuation lines align neatly
                    )
                    print(f"{c.GREEN}{operator.ljust(12)}{c.BLUE}{formatted_text}{c.RESET}")
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
                    print(f"\n\nCalculator vers {version}")
                    print(f"Please enter an equation or command\n{c.BLUE}If you need help type: \"?\"{c.RESET}")
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
                        print(f"\n\nCalculator vers {version}")
                        print(f"Please enter an equation or command\n{c.BLUE}If you need help type: \"?\"{c.RESET}")
                        break

                elif bpyth == "calc":  # Calculate B
                    print("Calculating Side B")
                    apyth = int(apyth)
                    cpyth = int(cpyth)

                    if cpyth ** 2 - apyth ** 2 < 0:
                        print(f"{c.RED}Calc Error: Invalid input. Hypotenuse must be the longest side.{c.RESET}")
                    else:
                        result = math.sqrt(cpyth ** 2 - apyth ** 2)
                        print(f"Side B is: {round(result,3)}")
                        print(f"\n\nCalculator vers {version}")
                        print(f"Please enter an equation or command\n{c.BLUE}If you need help type: \"?\"{c.RESET}")
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

                given_sides = sum(1 for x in [opposite, adjacent, hypotenuse] if isinstance(x, float))
                if given_sides == 0:
                    print(f"{c.RED}Error: You must provide at least one side.{c.RESET}")
                    continue
                if given_sides == 1 and angle is None:
                    print(f"{c.RED}Error: You must provide an angle if you only give one side.{c.RESET}")
                    continue

                if angle is not None:
                    angle_rad = math.radians(angle)

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

                if angle is None:
                    if opposite is not None and hypotenuse is not None:
                        angle = math.degrees(math.asin(opposite / hypotenuse))
                    elif adjacent is not None and hypotenuse is not None:
                        angle = math.degrees(math.acos(adjacent / hypotenuse))
                    elif opposite is not None and adjacent is not None:
                        angle = math.degrees(math.atan(opposite / adjacent))

                if angle is not None:
                    print(f"The angle is: {angle:.2f}°")
                if opposite is not None:
                    print(f"The opposite side is: {opposite:.2f}")
                if adjacent is not None:
                    print(f"The adjacent side is: {adjacent:.2f}")
                if hypotenuse is not None:
                    print(f"The hypotenuse is: {hypotenuse:.2f}")
                print(f"\n\nCalculator vers {version}")
                print(f"Please enter an equation or command\n{c.BLUE}If you need help type: \"?\"{c.RESET}")
                break

        elif user_equation == "sincos":
            print("Sine and Cosine Rule Calculator")
            intro = input("Introduction? (y/n)\n> ").lower()
            if intro == "y":
                print("\nThis tool calculates missing sides or angles in any triangle using the Sine and Cosine rules.")
                print("Type \"calc\" for the value you want to find.")
                print("Press enter ⏎ for values that do not apply.")
                print("At any point, type \"exit\" to return to the main menu.")
            elif intro == "exit":
                return

            while True:
                print("\nWhich values do you have?")
                
                def get_input(prompt):
                    value = input(f"{prompt} = ").strip().lower()
                    if value == "exit":
                        return "exit"
                    if value == "":
                        return None
                    if value == "calc":
                        return "calc"
                    try:
                        return float(value)
                    except ValueError:
                        print("Error: Invalid input. Enter a number or \"calc\".")
                        return get_input(prompt)

                sidea = get_input("Side A")
                if sidea == "exit": break
                sideb = get_input("Side B")
                if sideb == "exit": break
                sidec = get_input("Side C")
                if sidec == "exit": break
                anglea = get_input("Angle A (degrees)")
                if anglea == "exit": break
                angleb = get_input("Angle B (degrees)")
                if angleb == "exit": break
                anglec = get_input("Angle C (degrees)")
                if anglec == "exit": break
                
                given_sides = sum(1 for x in [sidea, sideb, sidec] if isinstance(x, float))
                given_angles = sum(1 for x in [anglea, angleb, anglec] if isinstance(x, float))

                if given_sides == 0:
                    print("Error: You must provide at least one side.")
                    continue
                if given_angles == 2:
                    anglec = 180 - (anglea + angleb)
                
                if anglea == "calc" and sideb and sidec:
                    anglea = math.degrees(math.acos((sideb**2 + sidec**2 - sidea**2) / (2 * sideb * sidec)))
                if angleb == "calc" and sidea and sidec:
                    angleb = math.degrees(math.acos((sidea**2 + sidec**2 - sideb**2) / (2 * sidea * sidec)))
                if anglec == "calc" and sidea and sideb:
                    anglec = math.degrees(math.acos((sidea**2 + sideb**2 - sidec**2) / (2 * sidea * sideb)))

                if sidea == "calc":
                    if angleb and anglec:
                        sidea = (sideb / math.sin(math.radians(angleb))) * math.sin(math.radians(anglea))
                    elif angleb and sidec:
                        sidea = math.sqrt(sideb**2 + sidec**2 - 2 * sideb * sidec * math.cos(math.radians(anglea)))

                if sideb == "calc":
                    if anglea and anglec:
                        sideb = (sidea / math.sin(math.radians(anglea))) * math.sin(math.radians(angleb))
                    elif anglea and sidec:
                        sideb = math.sqrt(sidea**2 + sidec**2 - 2 * sidea * sidec * math.cos(math.radians(angleb)))

                if sidec == "calc":
                    if anglec is None and anglea and angleb:
                        anglec = 180 - (anglea + angleb)
                    if anglea and sidea and anglec:
                        sidec = (sidea / math.sin(math.radians(anglea))) * math.sin(math.radians(anglec))
                    elif anglec and sidea and sideb:
                        sidec = math.sqrt(sidea**2 + sideb**2 - 2 * sidea * sideb * math.cos(math.radians(anglec)))
                    else:
                        print("Error: Not enough values to calculate Side C.")
                        continue
                print(" ")
                print("\nResults:")
                if anglea is not None: print(f"Angle A: {anglea:.2f}°")
                if angleb is not None: print(f"Angle B: {angleb:.2f}°")
                if anglec is not None: print(f"Angle C: {anglec:.2f}°")
                if sidea is not None: print(f"Side A: {sidea:.2f}")
                if sideb is not None: print(f"Side B: {sideb:.2f}")
                if sidec is not None: print(f"Side C: {sidec:.2f}")

                print(f"\n\nCalculator vers {version}")
                print(f"Please enter an equation or command\n{c.BLUE}If you need help type: \"?\"{c.RESET}")
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
                            print("\n\nSelect from below the system your digits are in")
                            print(f"{c.GREEN}1. Binary (base 2){c.RESET}")
                            print(f"{c.GREEN}2. Denary (base 10){c.RESET}")
                            print(f"{c.GREEN}3. Hexadecimal (base 16){c.RESET}")
                            break
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
                elif baseselect == "denary" or baseselect == "2":
                    print("Denary")
                    print("Input a valid Denary number")
                    while True:
                        digit = input("> ")
                        if digit.isdigit():
                            print(f"Binary: {bin(int(digit, 10))[2:]}")
                            print(f"Hexadecimal: {hex(int(digit, 10))[2:]}")
                            print("\n\nSelect from below the system your digits are in")
                            print(f"{c.GREEN}1. Binary (base 2){c.RESET}")
                            print(f"{c.GREEN}2. Denary (base 10){c.RESET}")
                            print(f"{c.GREEN}3. Hexadecimal (base 16){c.RESET}")
                            break
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
                            print("\n\nSelect from below the system your digits are in")
                            print(f"{c.GREEN}1. Binary (base 2){c.RESET}")
                            print(f"{c.GREEN}2. Denary (base 10){c.RESET}")
                            print(f"{c.GREEN}3. Hexadecimal (base 16){c.RESET}")
                            break
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
                    print(f"\n\nCalculator vers {version}")
                    print(f"Please enter an equation or command\n{c.BLUE}If you need help type: \"?\"{c.RESET}")
                    break
                
                else:
                    print(f"{c.RED}Error: Invaild input{c.RESET}")
                        
                    


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
