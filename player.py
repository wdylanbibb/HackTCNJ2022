from utils import Point

class Player:
    def __init__(self, position: Point, name: str, health: int, strength: int, attackSpeed: int) -> None:
        self.name = name
        self.hp = health
        self.stats = { 'strength': strength, 'attackSpeed': attackSpeed }
        self.position = position
