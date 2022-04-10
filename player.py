import map
from utils import Point
import curses

class Player:
    def __init__(self, position: Point, name: str, health: int, strength: int, attackSpeed: int) -> None:
        self.name = name
        self.hp = health
        self.max_hp = health
        self.stats = { 'strength': strength, 'attackSpeed': attackSpeed }
        self.position = position

    def input(self, event, gs):
        if event == ord('h'):
            if gs.map[map.p_idx(self.position + Point(-1, 0))] == map.TileType.FLOOR:
                self.position += Point(-1, 0)
        elif event == ord('j'):
            if gs.map[map.p_idx(self.position + Point(0, -1))] == map.TileType.FLOOR:
                self.position += Point(0, 1)
        elif event == ord('k'):
            if gs.map[map.p_idx(self.position + Point(0, 1))] == map.TileType.FLOOR:
                self.position += Point(0, -1)
        elif event == ord('l'):
            if gs.map[map.p_idx(self.position + Point(1, 0))] == map.TileType.FLOOR:
                self.position += Point(1, 0)
