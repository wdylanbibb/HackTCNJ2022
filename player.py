from utils import Point

class Player:
    def __init__(self, position: Point, name: str, health: int, speed: int) -> None:
        self.name = name
        self.stats = { 'health': health, 'speed': speed }
        self.position = position