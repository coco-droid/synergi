import json
import os

class APIKeyManager:
    def __init__(self):
        # Load the config.json file
        dirname = os.path.dirname(__file__)
        config_file_r = os.path.join(dirname, "config.json")
        with open(config_file_r, 'r') as config_file:
            self.api_keys = json.load(config_file)

    def get_api_key(self,key_name):
        """Retrieve API key based on the provided key name."""
        return self.api_keys.get(key_name)

        

