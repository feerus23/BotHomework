import json
import os
from src.body.data.storages.constants import CONFIGURATION_PATH


class Configuration:
    """Class for read configuration file"""

    def __init__(self):
        with open(CONFIGURATION_PATH, 'r') as config_file:
            self.json_variable = json.load(config_file)

    def __call__(self):
        return self.json_variable
