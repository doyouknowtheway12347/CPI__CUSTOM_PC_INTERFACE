import json

class Command:
    def __init__(self, display_name, description, trigger_command, function, args=None, next_page=None, 
                 execution_on_initialize=False, importance="medium", run_on_closure=False, scheduling="none"):
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
    def __init__(self, name, commands=None):
        self.name = name
        self.commands = commands if commands else []

    def add_command(self, command):
        self.commands.append(command)

    def remove_command(self, command_name):
        self.commands = [cmd for cmd in self.commands if cmd.display_name != command_name]

    def to_dict(self):
        return {
            "name": self.name,
            "commands": [cmd.to_dict() for cmd in self.commands]
        }

    @staticmethod
    def from_dict(data):
        commands = [Command.from_dict(cmd_data) for cmd_data in data['commands']]
        return Page(name=data['name'], commands=commands)


class CommandLineApp:
    def __init__(self, json_file=None):
        self.pages = []
        self.json_file = json_file
        if json_file:
            self.load_from_file()

    def add_page(self, page):
        self.pages.append(page)

    def find_page(self, page_name):
        for page in self.pages:
            if page.name == page_name:
                return page
        return None

    def save_to_file(self):
        data = {"pages": [page.to_dict() for page in self.pages]}
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
                self.pages = [Page.from_dict(page_data) for page_data in data['pages']]
        except FileNotFoundError:
            print("File not found. Starting with an empty structure.")
            self.pages = []

    def add_page_from_parameters(self, page_name):
        """Adds a new page to the application."""
        page = Page(name=page_name)
        self.add_page(page)
        print(f"Page '{page_name}' has been added.")

    def add_command_to_existing_page(self, page_name, display_name, description, trigger_command, function, args=None, 
                                     next_page=None, execution_on_initialize=False, importance="medium", 
                                     run_on_closure=False, scheduling="none"):
        """Adds a new command to an existing page."""
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
        """Lists all available pages."""
        if not self.pages:
            print("No pages available.")
        else:
            for idx, page in enumerate(self.pages, 1):
                print(f"{idx}. {page.name}")


# Example Usage
if __name__ == "__main__":
    # Initialize the app (if you want to load from a file)
    app = CommandLineApp(json_file=r"C:\01_PYTHON_CODE\Projects\CPI__CUSTOM_PC_INTERFACE\configuration.json")
    
    # Add a command to an existing page
    app.add_command_to_existing_page(
        page_name="Main Menu",
        display_name="Debugger",
        description="Used to debug the code of this project.",
        trigger_command="debug",
        function="debug",
        args=None,
        next_page=None,
        execution_on_initialize=False,
        importance="moderate",
        run_on_closure=False,
        scheduling="none"
    )


    # Save the configuration to file
    app.save_to_file()
