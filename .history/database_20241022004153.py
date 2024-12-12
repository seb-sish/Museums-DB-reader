from dataclasses import dataclass
import json 

class Museums:
    def __init__(self, path:str = "db.json"):
        self.path = path
        self.open_file()

    def open_file(self):
        with open(self.path, "r", encoding="UTF-8") as file:
            self.file = json.load(file)
            self.values = [museum(**info) for info in self.file]      
    
@dataclass
class museum:
    """Class for keeping track of an item in inventory."""
    name: str
    address: str
    date: int
    description: str = ""

    def __str__(self) -> str:
        return f"{self.name} ({self.address}) {self.date} год - {self.description}"
    
if __name__ == "__main__":
    museums = Museums()
    for i in museums:
        print(i)
    # print(museums.values[0].name)