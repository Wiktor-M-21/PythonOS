import csv
import textwrap
import sys  # Added for command-line argument parsing
import system.colours as colour

def display_commands(admin=False, user=False, specific_command=None):
    # Load the CSV file
    commands = []
    with open('system/cmds.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            command = {key.strip(): value.strip() for key, value in row.items()}
            commands.append(command)

    # Filter commands based on user/admin state
    none_commands = [cmd for cmd in commands if cmd.get("User Required", "") == "none"]
    user_commands = [cmd for cmd in commands if cmd.get("User Required", "") == "user"]
    admin_commands = [cmd for cmd in commands if cmd.get("User Required", "") == "admin"]

    # If a specific command is requested, display its details
    if specific_command:
        display_specific_command(specific_command, commands)
        return  # Exit after displaying the specific command

    # Dynamically adjust column widths
    max_name_length = max(len(cmd["Name"]) for cmd in commands) if commands else 15
    max_arg_length = max(len(cmd["Arguments"]) for cmd in commands) if commands else 15

    # Set minimum widths
    name_width = max(max_name_length, 15) + 2  # Minimum width of 15 for "Command"
    description_width = 40  # Initial width for description
    argument_width = max(max_arg_length, 15) + 2  # Minimum width of 15 for "Argument"

    # Adjust description width if any command name exceeds the current name_width
    for cmd in commands:
        if len(cmd["Name"]) > name_width - 2:  # Check if name exceeds current width
            name_width = len(cmd["Name"]) + 7  # Add 5 extra spaces for padding
            description_width = 40  # Reset description width

    # Calculate the maximum separator length
    separator_length = name_width + description_width + argument_width + 2  # +2 for spaces

    # Header
    print(f"{colour.GREEN}{'Command':<{name_width}} {colour.BLUE}{'Description':<{description_width}} {colour.YELLOW}{colour.BOLD}{'Arguments':<{argument_width}}{colour.RESET}")
    print("=" * separator_length)

    # Function to format and display commands
    def display_command_list(title, command_list):
        if command_list:
            print(f"{title}")
            print("-" * separator_length)
            for command in command_list:
                # Wrap the description to fit the description width
                wrapped_desc = textwrap.wrap(command["Description"], width=description_width)
                # Split arguments into required and optional
                args = command["Arguments"].split() if command["Arguments"] else []
                required_args = [arg[1:] if arg.startswith("*") else arg for arg in args if arg.startswith("*")]
                optional_args = [arg for arg in args if not arg.startswith("*")]

                # Combine required and optional arguments into a single string
                args_str = " ".join([f"-{arg}" if not arg.startswith("-") else arg for arg in required_args + optional_args])

                # Print the first line (command name, first line of description, and arguments)
                print(f"{colour.GREEN}{command['Name']:<{name_width}} {colour.BLUE}{wrapped_desc[0] if wrapped_desc else '':<{description_width}} {colour.YELLOW}{colour.BOLD}{args_str:<{argument_width}}{colour.RESET}")

                # Print additional lines for description (if any)
                for i in range(1, len(wrapped_desc)):
                    print(f"{colour.GREEN}{'':<{name_width}} {colour.BLUE}{wrapped_desc[i]:<{description_width}} {colour.YELLOW}{colour.BOLD}{'':<{argument_width}}{colour.RESET}")

    # Display categorized commands
    display_command_list("Commands available to everyone:", none_commands)
    if user or admin:
        display_command_list("Commands available to logged-in users:", user_commands)
    if admin:
        display_command_list("Commands available to admins:", admin_commands)

# Function to display details of a specific command
def display_specific_command(command_name, commands):
    # Search for the command
    found = False
    for cmd in commands:
        if cmd["Name"] == command_name:
            found = True
            # Print the command name and description
            print(f"{colour.GREEN}{'Command:':<15}{colour.RESET} {cmd['Name']}")
            print(f"{colour.BLUE}{'Description:':<15}{colour.RESET} {cmd['Description']}")

            # Split arguments into required and optional
            args = cmd["Arguments"].split() if cmd["Arguments"] else []
            required_args = [arg[1:] if arg.startswith("*") else arg for arg in args if arg.startswith("*")]
            optional_args = [arg for arg in args if not arg.startswith("*")]

            # Print required arguments
            if required_args:
                print(f"{colour.YELLOW}{'Required Args:':<15}{colour.RESET}")
                for arg in required_args:
                    print(f"{' ' * 15} -{arg}")

            # Print optional arguments
            if optional_args:
                print(f"{colour.YELLOW}{'Optional Args:':<15}{colour.RESET}")
                for arg in optional_args:
                    print(f"{' ' * 15} -{arg}")
            break

    # If the command is not found, display an error message
    if not found:
        print(f"{colour.RED}Error: Command '{command_name}' not found.{colour.RESET}")

# Main function to handle command-line arguments
def main():
    # Check if a specific command is requested
    if len(sys.argv) > 1 and sys.argv[1].startswith("-"):
        specific_command = sys.argv[1][1:]  # Remove the '-' from the argument
        display_commands(specific_command=specific_command)
    else:
        # Display all commands
        display_commands(admin=True, user=True)

# Run the main function
if __name__ == "__main__":
    main()