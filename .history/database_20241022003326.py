from dataclasses import dataclass
import json 

class museums:
    def __init__(self, path:str = "db.json"):
        self.path = path
        self.open_file()

    def open_file(self):
        with open(self.path, "r", encoding="UTF-8") as file:
            self.file = json.load(file)
            
    
@dataclass
class museum:
    """Class for keeping track of an item in inventory."""
    name: str
    address: str
    date: int
    description: str = ""