# ensure when looking for a specific command, that command found is not Error as it could not be found 

import json

class Main:
    def __init__(self, config_file, verbose=False):
        """
        Initialize the Main class with configuration file path and verbose mode setting.

        Args:
            config_file (str): The file path to the JSON configuration file.
            verbose (bool): Flag to enable or disable verbose mode.
        """
        self.config_file = config_file  # Location of JSON configuration file
        self.verbose = verbose  # Verbose mode flag
        self.current_page = "Main Menu"  # Initially set to "Main Menu"
        self.previous_page = "Main Menu"  # Initially set to "Main Menu"
