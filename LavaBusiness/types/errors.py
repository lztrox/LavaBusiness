from typing import Dict

class LavaError(Exception):
    def __init__(self, response: dict):
        self.error = response['error']

        if isinstance(self.error, Dict):
            self.message = ''
            for key, value in self.error.items():
                self.message += f"{key} - {value[0]}; "
        else:
            self.message = str(self.error)

    def __str__(self):
        return self.message