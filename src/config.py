import json
import os

DEFAULT_CONFIG = {
    "spam_link": "false",
    "link": "youtube.com/verybannable",
    "link_delay": 300
}

CONFIG_DIRECTORY = os.path.join('config.json')

class Config:
    def __init__(self) -> None:
        if not os.path.exists(CONFIG_DIRECTORY):
            with open(CONFIG_DIRECTORY, 'x') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)

        with open(CONFIG_DIRECTORY, 'r') as f:
            config = json.load(f)

        self.spam_link = config['spam_link'] == "true"
        self.link = config['link']
        self.link_delay = int(config['link_delay'])