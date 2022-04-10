from utils import Point


class Item:
    def __init__(self, name: str, description: str, detailedDesc: str, cocktail=False) -> None:
        self.name = name
        self.description = description
        self.detailedDesc = detailedDesc
        self.cocktail = cocktail

    def set_position(self, position: Point):
        self.position = position
        return self

class Weapon(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, atk: int) -> None:
        super().__init__(name, description, detailedDesc)
        self.atk = atk

    def __str__(self) -> str:
        return f'<Weapon - Name: {self.name}, Description: {self.description}, Detailed Description: {self.detailedDesc}, ATK: {self.atk}>'

class HealthItem(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, healingAmt: int, cocktail=False, uses: int = 1) -> None:
        super().__init__(name, description, detailedDesc, cocktail=cocktail)
        self.healingAmt = healingAmt
        self.uses = uses

    def __str__(self) -> str:
        return f'<HealthItem - Name: {self.name}, Description: {self.description}, Detailed Description: {self.detailedDesc}, Healing: {self.healingAmt}, Uses: {self.uses}>'


class BuffItem(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, stat: str, buff: int) -> None:
        super().__init__(name, description, detailedDesc, cocktail=True)
        self.stat = stat
        self.buff = buff

    def __str__(self) -> str:
        return f'<BuffItem - Name: {self.name}, Description: {self.description}, Detailed Description: {self.detailedDesc}, Stat: {self.stat}, Buff: {self.buff}>'
