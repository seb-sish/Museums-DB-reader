from dataclasses import dataclass
import json
import os

class Museums:
    def __init__(self, path:str = "._.json", create_new:bool = False):
        self.path = path
        if path != '' and os.path.isfile(path) \
            and path.split(".")[-1] in ("json"):
            self.open_file()
        elif create_new:
            self.create_new()
        else:
            raise FileNotFoundError("File not found!")
        
    def get_value(self, index):
        return self.values[index]
    
    def remove_value(self, index):
        return self.values.pop(index)
    
    def add_value(self, **kwargs):
        self.values.append(museum(kwargs))
        return self.values[-1]

    def create_new(self):
        with open(self.path, "w", encoding="UTF-8") as file:
            json.dump([{
            "name":        "",
            "address":     "",
            "date":        "",
            "description": "",
            "exposition":  ""
        }], file, ensure_ascii=False, indent=4)
        if self.path == "._.json":
            import subprocess
            subprocess.run(["attrib","+H",self.path],check=True)
        self.open_file()

    def open_file(self):
        with open(self.path, "r", encoding="UTF-8") as file:
            self.file = json.load(file)
            self.values = [museum(**info) for info in self.file]   

    def save_file(self):
        with open(self.path, "w", encoding="UTF-8") as file:
            json.dump(self.values, file, ensure_ascii=False, indent=4)

    def saveas_file(self, path):
        with open(path, "w", encoding="UTF-8") as file:
            json.dump(file, ensure_ascii=False, indent=4)

    def __len__(self):
        return len(self.values)
    
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.values):
            x = self.index
            self.index += 1
            return self.values[x]
        else:
            raise StopIteration
@dataclass
class museum:
    """Class for keeping track of an item in inventory."""
    name: str
    address: str
    date: int
    description: str = ""
    exposition: str = ""

    def __str__(self) -> str:
        return f"{self.name} ({self.address}) {self.date} год - {self.description}; {self.exposition}"
    
    def __getitem__(self, i):
        match i:
            case 0: return self.name
            case 1: return self.address
            case 2: return self.date
            case 3: return self.description
            case 4: return self.exposition
            case _: return None
    
if __name__ == "__main__":
    museums = Museums()
    for i in museums:
        print(i,"\n")
    # print(museums.values[0].name)