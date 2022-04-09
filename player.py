class Player:
    def __init__(self, name: str, health: int, strength: int, attackSpeed: int) -> None:
        self.name = name
        self.hp = health
        self.stats = { 'strength': strength, 'attackSpeed': attackSpeed }