class Player:
    def __init__(self, name: str, health: int, speed: int) -> None:
        self.name = name
        self.stats = { 'health': health, 'speed': speed }