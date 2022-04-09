from items import Item

class NPC:
    def __init__(self, name: str) -> None:
        self.name = name
        self.inventory: list[Item] = []
        
    def addItem(self, item: Item):
        self.inventory.append(item)

    def __str__(self) -> str:
        return f'<Person - Name: {self.name}>'