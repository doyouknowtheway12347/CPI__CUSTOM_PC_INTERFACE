import json

class Command:
    """
    Represents a single command in the CLI, with its attributes and functionality.
    Each command corresponds to an action that the user can trigger.

    Attributes:
        display_name (str): The name displayed to the user for the command.
        description (str): A brief description of what the command does.
        trigger_command (str): The command that the user types to trigger it.
        function (str): The function name to be called when the command is executed.
        args (dict): A dictionary of arguments required by the function.
        next_page (str or None): The name of the next page to navigate to after execution (if any).
        execution_on_initialize (bool): If True, the command runs automatically on application startup.
        importance (str): The importance level of the command (e.g., "high", "medium", "low").
        run_on_closure (bool): If True, the command runs when the application closes.
        scheduling (str): The scheduling for running the command (e.g., "daily", "weekly", "none").
    """

    def __init__(self, display_name, description, trigger_command, function, args=None, next_page=None, 
                 execution_on_initialize=False, importance="medium", run_on_closure=False, scheduling="none"):
        """
        Initializes a Command object with the provided attributes.

        Args:
            display_name (str): The name displayed to the user for the command.
            description (str): A brief description of what the command does.
            trigger_command (str): The command that the user types to trigger it.
            function (str): The function name to be called when the command is executed.
            args (dict, optional): A dictionary of arguments required by the function. Defaults to None.
            next_page (str, optional): The name of the next page to navigate to after execution. Defaults to None.
            execution_on_initialize (bool, optional): Whether the command runs on initialization. Defaults to False.
            importance (str, optional): The importance level of the command. Defaults to "medium".
            run_on_closure (bool, optional): Whether the command runs on closure. Defaults to False.
            scheduling (str, optional): The scheduling for running the command. Defaults to "none".
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
        Converts the Command object into a dictionary representation for saving to JSON.

        Returns:
            dict: A dictionary representing the Command object.
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
        Creates a Command object from a dictionary.

        Args:
            data (dict): The dictionary containing command data.

        Returns:
            Command: A new Command object based on the provided data.
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
    Represents a page in the command-line interface, which contains a list of commands.

    Attributes:
        name (str): The name of the page.
        commands (list): A list of Command objects associated with the page.
    """

    def __init__(self, name, commands=None):
        """
        Initializes a Page object with a name and optional list of commands.

        Args:
            name (str): The name of the page.
            commands (list, optional): A list of Command objects for this page. Defaults to an empty list.
        """
        self.name = name
        self.commands = commands if commands else []

    def add_command(self, command):
        """
        Adds a Command object to the page.

        Args:
            command (Command): The command to add to the page.
        """
        self.commands.append(command)

    def remove_command(self, command_name):
        """
        Removes a Command object from the page by its display name.

        Args:
            command_name (str): The display name of the command to remove.
        """
        self.commands = [cmd for cmd in self.commands if cmd.display_name != command_name]

    def to_dict(self):
        """
        Converts the Page object into a dictionary representation for saving to JSON.

        Returns:
            dict: A dictionary representing the Page object.
        """
        return {
            "name": self.name,
            "commands": [cmd.to_dict() for cmd in self.commands]
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Page object from a dictionary.

        Args:
            data (dict): The dictionary containing page data.

        Returns:
            Page: A new Page object based on the provided data.
        """
        commands = [Command.from_dict(cmd_data) for cmd_data in data['commands']]
        return Page(name=data['name'], commands=commands)


class CommandLineApp:
    """
    Represents the entire command-line application, which manages pages and commands.

    Attributes:
        pages (list): A list of Page objects for the CLI application.
        json_file (str, optional): The file path for saving and loading the configuration. Defaults to None.
    """

    def __init__(self, json_file=None):
        """
        Initializes the CommandLineApp with an optional JSON file.

        Args:
            json_file (str, optional): The file path for saving and loading the configuration. Defaults to None.
        """
        self.pages = []
        self.json_file = json_file
        if json_file:
            self.load_from_file()

    def add_page(self, page):
        """
        Adds a Page object to the CLI application.

        Args:
            page (Page): The page to add to the application.
        """
        self.pages.append(page)

    def remove_page(self, page_name):
        """
        Removes a Page object from the CLI application by its name.

        Args:
            page_name (str): The name of the page to remove.
        """
        self.pages = [page for page in self.pages if page.name != page_name]

    def find_page(self, page_name):
        """
        Finds and returns a page by its name.

        Args:
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
        Saves the current CLI configuration (pages and commands) to a JSON file.
        """
        data = {"pages": [page.to_dict() for page in self.pages]}
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        """
        Loads the CLI configuration from a JSON file, creating the necessary pages and commands.
        """
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
                self.pages = [Page.from_dict(page_data) for page_data in data['pages']]
        except FileNotFoundError:
            print("File not found. Starting with an empty structure.")
            self.pages = []

    def display_menu(self, page_name):
        """
        Displays a menu for a specified page, allowing the user to select commands.

        Args:
            page_name (str): The name of the page whose commands should be displayed.
        """
        page = self.find_page(page_name)
        if page:
            print(f"--- {page.name} ---")
            for i, command in enumerate(page.commands, 1):
                print(f"{i}. {command.display_name}: {command.description}")
            print("\nSelect an option or type 'exit' to quit.")
            choice = input("> ")
            if choice.lower() == 'exit':
                return
            try:
                selected_command = page.commands[int(choice) - 1]
                print(f"Running {selected_command.display_name}...")
                # Here, you'd trigger the actual function
            except (IndexError, ValueError):
                print("Invalid selection. Please try again.")
            return self.display_menu(page_name)
        else:
            print(f"Page '{page_name}' not found.")
            return


# Example Usage
if __name__ == "__main__":
    # Create some commands
    command1 = Command(
        display_name="Fetch Weather",
        description="Fetches weather data for a specified city.",
        trigger_command="weather <city>",
        function="fetch_weather",
        args={"city": "New York"},
        next_page=None,
        execution_on_initialize=True,
        importance="high",
        run_on_closure=False,
        scheduling="none"
    )

    command2 = Command(
        display_name="Display Disk Usage",
        description="Displays the current disk usage of the system.",
        trigger_command="disk_usage",
        function="display_disk_usage",
        args={},
        next_page="Disk Options",
        execution_on_initialize=False,
        importance="medium",
        run_on_closure=False,
        scheduling="none"
    )

    # Create a page and add commands
    main_menu = Page(name="Main Menu")
    main_menu.add_command(command1)
    main_menu.add_command(command2)

    # Create the application and add pages
    app = CommandLineApp(json_file="cli_config.json")
    app.add_page(main_menu)

    # Save the configuration to file
    app.save_to_file()

    # Load and display menu from the file
    app.load_from_file()
    app.display_menu("Main Menu")
