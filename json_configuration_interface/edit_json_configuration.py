import json

class Command:
    """
    Represents a command with attributes for display, functionality, and execution context.
    """
    def __init__(self, display_name, description, trigger_command, function, args=None, next_page=None, 
                 execution_on_initialize=False, importance="medium", run_on_closure=False, scheduling="none"):
        """
        Initialize a command with required attributes.

        Parameters:
            display_name (str): The name to display for the command.
            description (str): A brief description of what the command does.
            trigger_command (str): The keyword or phrase to trigger the command.
            function (str): The function to be executed when the command is triggered.
            args (dict, optional): Arguments for the command function (default is None).
            next_page (str, optional): Page to navigate to after execution (default is None).
            execution_on_initialize (bool, optional): Whether to execute on page load (default is False).
            importance (str, optional): Importance level of the command (default is "medium").
            run_on_closure (bool, optional): Whether to run the command on page closure (default is False).
            scheduling (str, optional): Execution scheduling, if applicable (default is "none").
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

    def to_dict(self):
        """
        Converts the Command instance to a dictionary format suitable for JSON serialization.
        """
        return {
            "display_name": self.display_name,
            "description": self.description,
            "trigger_command": self.trigger_command,
            "function": self.function,
            "args": self.args,
            "next_page": self.next_page,
            "execution_on_initialize": self.execution_on_initialize,
            "importance": self.importance,
            "run_on_closure": self.run_on_closure,
            "scheduling": self.scheduling
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Command instance from a dictionary.

        Parameters:
            data (dict): Dictionary with command attributes.

        Returns:
            Command: A new Command object initialized with the provided data.
        """
        return Command(
            display_name=data['display_name'],
            description=data['description'],
            trigger_command=data['trigger_command'],
            function=data['function'],
            args=data.get('args', {}),
            next_page=data.get('next_page'),
            execution_on_initialize=data.get('execution_on_initialize', False),
            importance=data.get('importance', "medium"),
            run_on_closure=data.get('run_on_closure', False),
            scheduling=data.get('scheduling', "none")
        )


class Page:
    """
    Represents a page within the application that contains a list of commands.
    """
    def __init__(self, name, commands=None):
        """
        Initializes a page with a name and optional list of commands.

        Parameters:
            name (str): Name of the page.
            commands (list of Command, optional): List of Command objects (default is an empty list).
        """
        self.name = name
        self.commands = commands if commands else []

    def add_command(self, command):
        """
        Adds a Command to the page's command list.

        Parameters:
            command (Command): The command to add.
        """
        self.commands.append(command)

    def remove_command(self, command_name):
        """
        Removes a Command from the page's command list by name.

        Parameters:
            command_name (str): The display name of the command to remove.
        """
        self.commands = [cmd for cmd in self.commands if cmd.display_name != command_name]

    def to_dict(self):
        """
        Converts the Page instance to a dictionary format suitable for JSON serialization.
        """
        return {
            "name": self.name,
            "commands": [cmd.to_dict() for cmd in self.commands]
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Page instance from a dictionary.

        Parameters:
            data (dict): Dictionary with page attributes.

        Returns:
            Page: A new Page object initialized with the provided data.
        """
        commands = [Command.from_dict(cmd_data) for cmd_data in data['commands']]
        return Page(name=data['name'], commands=commands)


class CommandLineApp:
    """
    Manages pages and commands, with functionality to load from and save to a JSON file.
    """
    def __init__(self, json_file=None):
        """
        Initializes the app, optionally loading from a JSON file.

        Parameters:
            json_file (str, optional): Path to a JSON configuration file (default is None).
        """
        self.pages = []
        self.json_file = json_file
        if json_file:
            self.load_from_file()

    def add_page(self, page):
        """
        Adds a Page to the application's page list.

        Parameters:
            page (Page): The page to add.
        """
        self.pages.append(page)

    def find_page(self, page_name):
        """
        Finds a page by name.

        Parameters:
            page_name (str): The name of the page to find.

        Returns:
            Page: The Page object if found, or None if not found.
        """
        for page in self.pages:
            if page.name == page_name:
                return page
        return None

    def save_to_file(self):
        """
        Saves the current application configuration to a JSON file.
        """
        data = {"pages": [page.to_dict() for page in self.pages]}
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        """
        Loads the application configuration from a JSON file, if the file exists.
        """
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
                self.pages = [Page.from_dict(page_data) for page_data in data['pages']]
        except FileNotFoundError:
            print("File not found. Starting with an empty structure.")
            self.pages = []

    def add_page_from_parameters(self, page_name):
        """
        Adds a new page to the application by name.

        Parameters:
            page_name (str): The name of the page to add.
        """
        page = Page(name=page_name)
        self.add_page(page)
        print(f"Page '{page_name}' has been added.")

    def add_command_to_existing_page(self, page_name, display_name, description, trigger_command, function, args=None, 
                                     next_page=None, execution_on_initialize=False, importance="medium", 
                                     run_on_closure=False, scheduling="none"):
        """
        Adds a new command to an existing page.

        Parameters:
            page_name (str): Name of the page to add the command to.
            display_name (str): Display name of the command.
            description (str): Description of the command.
            trigger_command (str): The trigger command keyword.
            function (str): The function to execute.
            args (dict, optional): Arguments for the function (default is None).
            next_page (str, optional): Page to navigate to next (default is None).
            execution_on_initialize (bool, optional): Execute on page load (default is False).
            importance (str, optional): Importance level (default is "medium").
            run_on_closure (bool, optional): Run on page closure (default is False).
            scheduling (str, optional): Scheduling type (default is "none").
        """
        page = self.find_page(page_name)
        if not page:
            print(f"Page '{page_name}' not found. Please create the page first.")
            return

        # Create the new command with the provided parameters
        new_command = Command(
            display_name=display_name,
            description=description,
            trigger_command=trigger_command,
            function=function,
            args=args if args else {},
            next_page=next_page,
            execution_on_initialize=execution_on_initialize,
            importance=importance,
            run_on_closure=run_on_closure,
            scheduling=scheduling
        )

        # Add the command to the page
        page.add_command(new_command)
        print(f"Command '{display_name}' added to page '{page_name}'.")

    def list_pages(self):
        """
        Lists all available pages.
        """
        if not self.pages:
            print("No pages available.")
        else:
            for idx, page in enumerate(self.pages, 1):
                print(f"{idx}. {page.name}")


# Example Usage
# if __name__ == "__main__":
#     # Initialize the app (if you want to load from a file)
#     app = CommandLineApp(json_file=r"C:\01_PYTHON_CODE\Projects\CPI__CUSTOM_PC_INTERFACE\configuration.json")
    
#     # Add a command to an existing page
#     app.add_command_to_existing_page(
#         page_name="Main Menu",
#         display_name="Debugger",
#         description="Used to debug the code of this project.",
#         trigger_command="debug",
#         function="debug",
#         args=None,
#         next_page=None,
#         execution_on_initialize=False,
#         importance="moderate",
#         run_on_closure=False,
#         scheduling="none"
#     )

#     # Save the configuration to file
#     app.save_to_file()
