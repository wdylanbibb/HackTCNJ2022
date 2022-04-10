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
        if event == ord('h') or event == curses.KEY_LEFT:
            if gs.map[map.p_idx(self.position + Point(-1, 0))] == map.TileType.FLOOR:
                self.position += Point(-1, 0)
        elif event == ord('j') or event == curses.KEY_DOWN:
            if gs.map[map.p_idx(self.position + Point(0, 1))] == map.TileType.FLOOR:
                self.position += Point(0, 1)
        elif event == ord('k') or event == curses.KEY_UP:
            if gs.map[map.p_idx(self.position + Point(0, -1))] == map.TileType.FLOOR:
                self.position += Point(0, -1)
        elif event == ord('l') or event == curses.KEY_RIGHT:
            if gs.map[map.p_idx(self.position + Point(1, 0))] == map.TileType.FLOOR:
                self.position += Point(1, 0)
