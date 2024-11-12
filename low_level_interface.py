import json

class Command:
    """
    Represents a command in the CLI application.
    Each command has a name, description, trigger, function, and other properties as specified in the JSON configuration.
    """

    def __init__(self, display_name, description, trigger_command, function, args=None, next_page=None,
                 execution_on_initialize=False, importance="medium", run_on_closure=False, scheduling="none"):
        """
        Initialize a Command object with the necessary details.

        Args:
            display_name (str): Display name shown to the user.
            description (str): Brief description of what the command does.
            trigger_command (str): Command string user types to trigger the function.
            function (str): Name of the function that gets called.
            args (dict): Additional arguments required by the function.
            next_page (str): Optional name of the next page to navigate to after execution.
            execution_on_initialize (bool): Whether the command runs automatically on app start.
            importance (str): Importance of the command, can be "low", "medium", or "high".
            run_on_closure (bool): Whether to run the command upon app closure.
            scheduling (str): Scheduling for running the command, can be "none", "daily", etc.
        """
        self.display_name = display_name
        self.description = description
        self.trigger_command = trigger_command
        self.function = function
        self.args = args if args else {}
        self.next_page = next_page
        self.execution_on_initialize = execution_on_initialize
        self.importance = importance
        self.run_on_closure = run_on_closure
        self.scheduling = scheduling

    def __str__(self):
        """String representation of the Command object."""
        return f"{self.display_name}: {self.description} (Trigger: {self.trigger_command})"


class MainClass:
    """
    Main interface that loads commands from the JSON configuration.
    """

    def __init__(self, json_file):
        """
        Initializes the MainClass and loads commands from the JSON configuration file.
        
        Args:
            json_file (str): Path to the JSON configuration file.
        """
        self.json_file = json_file
        self.commands = []  # List to store commands
        self.load_from_file()

    def load_from_file(self):
        """
        Loads the JSON configuration from the file and creates Command objects from it.
        """
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                print(data)  # Debugging: Check what data looks like
                
                # Iterate through each page in the JSON
                for page_data in data.get('pages', []):  # Use .get to avoid KeyError if 'pages' is missing
                    page_name = page_data.get('name', 'Unnamed Page')
                    print(f"Loading commands for page: {page_name}")
                    
                    # Iterate through the commands in each page
                    for cmd_data in page_data.get('commands', []):  # Same here for 'commands' in each page
                        # Convert each command data into a Command object
                        command = Command(
                            display_name=cmd_data['display_name'],
                            description=cmd_data['description'],
                            trigger_command=cmd_data['trigger_command'],
                            function=cmd_data['function'],
                            args=cmd_data.get('args', {}),
                            next_page=cmd_data.get('next_page'),
                            execution_on_initialize=cmd_data.get('execution_on_initialize', False),
                            importance=cmd_data.get('importance', "medium"),
                            run_on_closure=cmd_data.get('run_on_closure', False),
                            scheduling=cmd_data.get('scheduling', "none")
                        )
                        self.commands.append(command)
                    
        except FileNotFoundError:
            print(f"Configuration file '{self.json_file}' not found.")
        except json.JSONDecodeError:
            print(f"Error reading JSON from file '{self.json_file}'.")

    def list_commands(self):
        """
        Lists all available commands in the application.
        """
        if not self.commands:
            print("No commands available.")
        else:
            for idx, cmd in enumerate(self.commands, 1):
                print(f"{idx}. {cmd.display_name}: {cmd.description}")

    def find_command_by_trigger(self, trigger_command):
        """
        Find a command by its trigger string.

        Args:
            trigger_command (str): The trigger string to search for.
        """
        return next((cmd for cmd in self.commands if cmd.trigger_command == trigger_command), None)

    def run(self):
        """
        Starts the interactive CLI interface, allowing the user to input commands.
        """
        print("Welcome to the CLI App!")
        while True:
            print("\nAvailable Commands:")
            self.list_commands()
            user_input = input("\nEnter a command to execute (or 'exit' to quit): ").strip().lower()
            if user_input == 'exit':
                print("Exiting the application.")
                break
            else:
                command = self.find_command_by_trigger(user_input)
                if command:
                    print(f"Executing command: {command.display_name}")
                    print(f"Function to execute: {command.function}")
                    # You can later expand this to actually execute the command
                else:
                    print(f"Command '{user_input}' not found.")


if __name__ == "__main__":
    # Initialize the MainClass with the path to the JSON configuration file
    app = MainClass(json_file=r"C:\01_PYTHON_CODE\Projects\CPI__CUSTOM_PC_INTERFACE\configuration.json")

    # Run the CLI app
    app.run()