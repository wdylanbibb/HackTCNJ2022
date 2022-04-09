class Item:
    def __init__(self, name: str, description: str, detailedDesc: str) -> None:
        self.name = name
        self.description = description
        self.detailedDesc = detailedDesc

class Weapon(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, atk: int) -> None:
        super().__init__(name, description, detailedDesc)
        self.atk = atk

class HealthItem(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, healingAmt: int, uses: int = 1) -> None:
        super().__init__(name, description, detailedDesc)
        self.healingAmt = healingAmt
        self.uses = uses

class BuffItem(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, stat: str, buff: int) -> None:
        super().__init__(name, description, detailedDesc)
        self.stat = stat
        self.buff = buff