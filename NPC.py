import log
import names
from items import Item
from utils import Point

class NPC:
    def __init__(self, name: str) -> None:
        self.name = name
        self.inventory: list[Item] = []

    def set_position(self, position: Point):
        self.position = position
        return self

    def addItem(self, item: Item):
        self.inventory.append(item)

    def __str__(self) -> str:
        return f'<Person - Name: {self.name}>'

    def talk(self):
        log.log_message(f'{self.name} says hello.')

def get_random_NPC():
    return NPC(names.get_full_name())