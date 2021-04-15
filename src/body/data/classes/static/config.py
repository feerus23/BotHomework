import json

# CONSTANTS
CONFIGURATION_PATH = 'body\\data\\storages\\config.json' # Path to configuration file

class Configuration:
    """Class for read configuration file"""

    def __init__(self):
        self.json_variable = json.load(open(CONFIGURATION_PATH, 'r'))
        
    def __call__(self):
        return self.json_variable