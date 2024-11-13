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
    
