from dataclasses import dataclass


@dataclass
class museum:
    """Class for keeping track of an item in inventory."""
    name: str
    address: str
    date: int
    description: str = ""