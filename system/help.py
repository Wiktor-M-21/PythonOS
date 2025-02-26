import csv
import system.colours as colour

def display_commands(admin=False, user=False):
    # Load the CSV file
    commands = []
    with open('system/cmds.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Clean up headers in case of spaces or extra characters
            command = {key.strip(): value for key, value in row.items()}
            commands.append(command)

    # Filter based on user/admin state
    none_commands = []
    user_commands = []
    admin_commands = []

    # Classify commands based on "User Required"
    for command in commands:
        user_type = command.get("User Required", "") or ""
        user_type = user_type.strip()
        if user_type == "none":
            none_commands.append(command)
        elif user_type == "user":
            user_commands.append(command)
        elif user_type == "admin":
            admin_commands.append(command)

    # Adjust column widths
    name_width = 15
    description_width = 35
    argument_width = 15

    # Header with colors
    print(f"{colour.GREEN}{'Command':<{name_width}} {colour.BLUE}{'Description':<{description_width}} {colour.YELLOW}{colour.BOLD}{'Argument':<{argument_width}}{colour.RESET}")
    print("=" * (95))

    # Show commands that don't require login
    print("Commands available to everyone:")
    for command in none_commands:
        print(f"{colour.GREEN}{command['Name']:<{name_width}} {colour.BLUE}{command['Description']:<{description_width}} {colour.YELLOW}{colour.BOLD}{command['Arguments']:<{argument_width}}{colour.RESET}")
    print("-" * (95))

    # Show commands that require a logged-in user
    if user or admin:
        print("Commands available to logged-in users:")
        for command in user_commands:
            print(f"{colour.GREEN}{command['Name']:<{name_width}} {colour.BLUE}{command['Description']:<{description_width}} {colour.YELLOW}{colour.BOLD}{command['Arguments']:<{argument_width}}{colour.RESET}")
        print("-" * (95))

    # Show commands that require admin
    if admin:
        print("Commands available to admins:")
        for command in admin_commands:
            print(f"{colour.GREEN}{command['Name']:<{name_width}} {colour.BLUE}{command['Description']:<{description_width}} {colour.YELLOW}{colour.BOLD}{command['Arguments']:<{argument_width}}{colour.RESET}")
        print("-" * (95))