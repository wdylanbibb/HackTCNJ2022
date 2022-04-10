import random
import log
import names
from items import Item
from utils import Point
import requests

from yamlReader import get_annoyed_dialog, get_random_primary_line, get_random_return_line

class NPC:
    def __init__(self, name: str, initialDialog: str, returnDialog: str) -> None:
        self.name = name
        self.inventory: list[Item] = []
        self.initialDialog = initialDialog
        self.returnDialog = returnDialog
        self.numVisited = 1

    def set_position(self, position: Point):
        self.position = position
        return self

    def addItem(self, item: Item):
        self.inventory.append(item)

    def __str__(self) -> str:
        return f'<Person - Name: {self.name}>'

<<<<<<< HEAD
    def talk(self):
        log.log_message(f'{self.name} says hello.')
    
    def move(self):
        pass
=======
    def next_message(self):
        if self.numVisited == 0:
            self.numVisited += 1
            return self.initialDialog;
        if self.numVisited >= 5:
            self.numVisited += 1
            return get_annoyed_dialog()
        self.numVisited += 1
        return self.returnDialog
>>>>>>> 54e3c7905d6be008a05b6715e81433cd973af61e

def get_random_NPC():
    return NPC(names.get_full_name(), get_random_primary_line(), get_random_return_line())