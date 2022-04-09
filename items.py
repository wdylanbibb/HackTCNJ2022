class Item:
    def __init__(self, name: str, description: str, detailedDesc: str) -> None:
        self.name = name
        self.description = description
        self.detailedDesc = detailedDesc

class Weapon(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, atk: int) -> None:
        super().__init__(name, description, detailedDesc)
        self.atk = atk

    def __str__(self) -> str:
        return f'<Weapon - Name: {self.name}, Description: {self.description}, Detailed Description: {self.detailedDesc}, ATK: {self.atk}>'

class HealthItem(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, healingAmt: int, uses: int = 1) -> None:
        super().__init__(name, description, detailedDesc)
        self.healingAmt = healingAmt
        self.uses = uses

    def __str__(self) -> str:
        return f'<HealthItem - Name: {self.name}, Description: {self.description}, Detailed Description: {self.detailedDesc}, Healing: {self.healingAmt}, Uses: {self.uses}>'


class BuffItem(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, stat: str, buff: int) -> None:
        super().__init__(name, description, detailedDesc)
        self.stat = stat
        self.buff = buff

    def __str__(self) -> str:
        return f'<BuffItem - Name: {self.name}, Description: {self.description}, Detailed Description: {self.detailedDesc}, Stat: {self.stat}, Buff: {self.buff}>'
