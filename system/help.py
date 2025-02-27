import csv
import textwrap
import sys
import argparse
import system.colours as colour

CSV_FILE = "system/cmds.csv"

# Default column widths
NAME_MIN_WIDTH = 15
DESC_WIDTH = 40
ARG_MIN_WIDTH = 15


def load_commands():
    """Loads commands from CSV file."""
    commands = []
    try:
        with open(CSV_FILE, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                command = {key.strip(): value.strip() for key, value in row.items()}
                commands.append(command)
    except FileNotFoundError:
        print(f"{colour.RED}Error: Command file '{CSV_FILE}' not found.{colour.RESET}")
        sys.exit(1)
    return commands


def categorize_commands(commands):
    """Categorizes commands based on access level."""
    categorized = {"none": [], "user": [], "admin": []}
    for cmd in commands:
        user_required = cmd.get("User Required", "").lower()
        if user_required in categorized:
            categorized[user_required].append(cmd)
    return categorized


def display_specific_command(command_name, commands):
    """Displays details of a specific command with properly aligned arguments."""
    for cmd in commands:
        if cmd["Name"] == command_name:
            print(f"{colour.GREEN}{'Command:':<15}{colour.RESET} {cmd['Name']}")
            print(f"{colour.BLUE}{'Description:':<15}{colour.RESET} {cmd['Description']}")
            
            # Display Command Type above Arguments
            command_type = cmd.get("Command Type", "Internal - System")
            print(f"{colour.CYAN}{'Command Type:':<15}{colour.RESET} {command_type}")

            if cmd.get("Arguments"):
                args = cmd["Arguments"].split()
                
                # Create a more robust argument descriptions parser
                arg_desc_map = {}
                if cmd.get("Argument Descriptions"):
                    # Split by comma, but handle the case where commas might appear in descriptions
                    raw_descriptions = cmd.get("Argument Descriptions", "")
                    
                    # Parse descriptions more carefully
                    current_desc = ""
                    in_quotes = False
                    descriptions = []
                    
                    for char in raw_descriptions:
                        if char == '"':
                            in_quotes = not in_quotes
                            current_desc += char
                        elif char == ',' and not in_quotes:
                            descriptions.append(current_desc.strip())
                            current_desc = ""
                        else:
                            current_desc += char
                    
                    if current_desc.strip():
                        descriptions.append(current_desc.strip())
                    
                    for desc in descriptions:
                        # Split only on first ":"
                        parts = desc.split(":", 1)
                        if len(parts) == 2:
                            # Clean up the argument name to match the format in the Arguments field
                            arg_name = parts[0].strip().strip('*-"')
                            arg_desc = parts[1].strip().strip('"')
                            arg_desc_map[arg_name] = arg_desc

                # Separate required and optional arguments
                required_args = [arg.lstrip('*') for arg in args if arg.startswith('*')]
                optional_args = [arg for arg in args if not arg.startswith('*')]

                # Print arguments, ensuring correct alignment
                arg_label = f"{colour.YELLOW}{'Arguments:':<15}{colour.RESET}"
                first_arg_indent = " " * 15  # Aligns arguments properly

                def format_arg(arg, is_required=True):
                    """Formats an argument with a required indicator and description."""
                    # Clean arg name for matching with descriptions
                    clean_arg = arg.lstrip('*')
                    display_arg = f"-{clean_arg}" if is_required else f"--{clean_arg}"
                    # Look up description with normalized name
                    description = arg_desc_map.get(clean_arg, "No description available")
                    return f"{display_arg}: {description}"

                # Print required arguments first
                if required_args:
                    print(f"{arg_label} {format_arg(required_args[0], True)}")
                    for arg in required_args[1:]:
                        print(f"{first_arg_indent} {format_arg(arg, True)}")

                # Print optional arguments next
                if optional_args:
                    if not required_args:  # If no required args, align the first optional argument
                        print(f"{arg_label} {format_arg(optional_args[0], False)}")
                    else:
                        print(f"{first_arg_indent} {format_arg(optional_args[0], False)}")
                    for arg in optional_args[1:]:
                        print(f"{first_arg_indent} {format_arg(arg, False)}")

            return

    print(f"{colour.RED}Error: Command '{command_name}' not found.{colour.RESET}")


def display_commands(admin=False, user=False, specific_command=None):
    """Displays commands based on user/admin status or a specific command."""
    commands = load_commands()
    if specific_command:
        display_specific_command(specific_command, commands)
        return

    categorized = categorize_commands(commands)

    # Calculate column widths dynamically
    max_name_length = max((len(cmd["Name"]) for cmd in commands), default=NAME_MIN_WIDTH)
    max_arg_length = max((len(cmd.get("Arguments", "")) for cmd in commands), default=ARG_MIN_WIDTH)

    name_width = max(max_name_length, NAME_MIN_WIDTH) + 2
    argument_width = max(max_arg_length, ARG_MIN_WIDTH) + 2
    separator_length = name_width + DESC_WIDTH + argument_width + 2

    print(f"{colour.GREEN}{'Command':<{name_width}} {colour.BLUE}{'Description':<{DESC_WIDTH}} {colour.YELLOW}{'Arguments':<{argument_width}}{colour.RESET}")
    print("=" * separator_length)

    def display_command_list(title, command_list):
        """Displays a formatted list of commands."""
        if command_list:
            print(f"\n{title}")
            print("-" * separator_length)
            for cmd in command_list:
                wrapped_desc = textwrap.wrap(cmd["Description"], width=DESC_WIDTH)
                args = cmd.get("Arguments", "").split()
                formatted_args = " ".join([arg.replace("*", "-") for arg in args])

                print(f"{colour.GREEN}{cmd['Name']:<{name_width}} {colour.BLUE}{wrapped_desc[0]:<{DESC_WIDTH}} {colour.YELLOW}{formatted_args:<{argument_width}}{colour.RESET}")
                for line in wrapped_desc[1:]:
                    print(f"{'':<{name_width}} {colour.BLUE}{line:<{DESC_WIDTH}} {colour.YELLOW}{'':<{argument_width}}{colour.RESET}")

    display_command_list("Commands available to everyone:", categorized["none"])
    if user or admin:
        display_command_list("Commands available to logged-in users:", categorized["user"])
    if admin:
        display_command_list("Commands available to admins:", categorized["admin"])


def main():
    """Handles command-line arguments and runs the program."""
    parser = argparse.ArgumentParser(description="Display available commands.")
    parser.add_argument("-c", "--command", help="Display details of a specific command")
    parser.add_argument("-a", "--admin", action="store_true", help="Show admin commands")
    parser.add_argument("-u", "--user", action="store_true", help="Show user commands")

    args = parser.parse_args()

    if args.command:
        display_commands(specific_command=args.command)
    else:
        display_commands(admin=args.admin, user=args.user)

def create_new_command():
    """Prompts the user to create a new command and saves it to the CSV file."""
    print(f"{colour.GREEN}Creating a new command...{colour.RESET}")
    
    # Prompt the user for command details
    name = input(f"{colour.BLUE}Enter the command name: {colour.RESET}").strip()
    description = input(f"{colour.BLUE}Enter the command description: {colour.RESET}").strip()
    arguments = input(f"{colour.BLUE}Enter the command arguments (e.g., *arg1 arg2): {colour.RESET}").strip()
    arg_descriptions = input(f"{colour.BLUE}Enter the argument descriptions (e.g., arg1:description1, arg2:description2): {colour.RESET}").strip()
    user_required = input(f"{colour.BLUE}Enter the user access level (none, user, admin): {colour.RESET}").strip().lower()
    command_type = input(f"{colour.BLUE}Enter the command type (e.g., Internal - System): {colour.RESET}").strip()

    # Validate user_required input
    if user_required not in ["none", "user", "admin"]:
        print(f"{colour.RED}Error: Invalid user access level. Must be 'none', 'user', or 'admin'.{colour.RESET}")
        return

    # Create a dictionary for the new command
    new_command = {
        "Name": name,
        "Description": description,
        "Arguments": arguments,
        "Argument Descriptions": arg_descriptions,
        "User Required": user_required,
        "Command Type": command_type
    }

    # Append the new command to the CSV file
    try:
        with open(CSV_FILE, mode='a', newline='', encoding="utf-8") as csvfile:
            fieldnames = ["Name", "Description", "Arguments", "Argument Descriptions", "User Required", "Command Type"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Ensure the file is not empty before writing headers
            csvfile.seek(0, 2)  # Move to the end of the file
            if csvfile.tell() == 0:  # Check if the file is empty
                writer.writeheader()  # Write headers only if the file is empty

            # Write the new command
            writer.writerow(new_command)
            print(f"{colour.GREEN}Command '{name}' successfully added!{colour.RESET}")
    except Exception as e:
        print(f"{colour.RED}Error: Failed to write to the CSV file. {e}{colour.RESET}")