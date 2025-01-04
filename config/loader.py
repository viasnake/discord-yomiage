import json
import os
import sys

class ConfigLoader:

    #
    def __init__(self) -> None:
        self.config = self.load_config()

    #
    def load_config(self) -> dict[str, str]:

        #
        if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
            sys.exit("config.json not found.")

        #
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json", "r") as file:
            return json.load(file)

    #
    def get(self, key: str) -> str:
        return self.config.get(key, "")
