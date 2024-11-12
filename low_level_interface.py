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
        self.pages = []  # Initialize pages to store the structure of pages and commands.
        self.commands = []  # List to store all commands across pages for listing/searching
        self.load_from_file()

    def load_from_file(self):
        """
        Loads the JSON configuration from the file and creates Command objects from it.
        """
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                
                # Clear and populate pages attribute from JSON file data
                self.pages = data.get('pages', [])
                print(f"Loaded pages: {[page['name'] for page in self.pages]}")  # Debugging

                # Populate command list from each page
                for page_data in self.pages:
                    for cmd_data in page_data.get('commands', []):
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

    def find_command_by_trigger(self, trigger_command):
        """
        Find a command by its trigger string, allowing for arguments to be passed in.

        Args:
            trigger_command (str): The trigger string to search for (including arguments).
            
        Returns:
            Command or None: The matched command, or None if no match is found.
        """
        # Iterate over all commands
        for cmd in self.commands:
            # Extract the base command (everything before any space) from the trigger command
            base_command = cmd.trigger_command.split(' ')[0]  # First word is the base command
            # Compare the base part of the trigger command
            if trigger_command.lower() == base_command.lower():
                # If the base command matches, you could optionally parse arguments here
                return cmd
    
        return Command("Error", "No command found with this trigger", None, None, None, None, False, None, None, "none")

    def get_page_names(self):
        """
        Retrieves the names of all pages in the JSON configuration.
        """
        return [page['name'] for page in self.pages]

    def get_commands_for_page(self, page_name="Main Menu"):
        """
        Retrieves the commands available on a specific page.

        Args:
            page_name (str): The name of the page for which to retrieve commands.
        
        Returns:
            list: A list of command names available on the specified page.
        """
        page = next((page for page in self.pages if page['name'] == page_name), None)
        if page:
            return [cmd['trigger_command'] for cmd in page['commands']]
        else:
            return []

# Initialize and use the MainClass
if __name__ == "__main__":
    app = MainClass(json_file=r"C:\01_PYTHON_CODE\Projects\CPI__CUSTOM_PC_INTERFACE\configuration.json")
    # print(app.get_commands_for_page("Main Menu"))
    debugger = app.find_command_by_trigger("deasdfbug")
