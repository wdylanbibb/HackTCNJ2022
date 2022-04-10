from draw import dec_index, get_idx, inc_index, is_show_inventory, toggle_inventory
import map
from utils import Point
import curses
import log

class Player:
    def __init__(self, position: Point, name: str, health: int, strength: int, attackSpeed: int) -> None:
        self.name = name
        self.hp = health
        self.max_hp = health
        self.stats = { 'strength': strength, 'attackSpeed': attackSpeed }
        self.position = position
        self.inventory = []

    def input(self, event, gs):
        if event == ord('h') or event == curses.KEY_LEFT:
            if not is_show_inventory():
                if gs.map[map.p_idx(self.position + Point(-1, 0))] == map.TileType.FLOOR:
                    self.position += Point(-1, 0)
                    log.log_message("You step.")
        elif event == ord('j') or event == curses.KEY_DOWN:
            if not is_show_inventory():
                if gs.map[map.p_idx(self.position + Point(0, 1))] == map.TileType.FLOOR:
                    self.position += Point(0, 1)
            else:
                inc_index()
        elif event == ord('k') or event == curses.KEY_UP:
            if not is_show_inventory():
                if gs.map[map.p_idx(self.position + Point(0, -1))] == map.TileType.FLOOR:
                    self.position += Point(0, -1)
            else:
                dec_index()
        elif event == ord('l') or event == curses.KEY_RIGHT:
            if not is_show_inventory():
                if gs.map[map.p_idx(self.position + Point(1, 0))] == map.TileType.FLOOR:
                    self.position += Point(1, 0)
        elif event == ord('i'):
            toggle_inventory()
        items = [i for i in gs.items if i.position == self.position]
        npc = [i for i in gs.npcs if i.position == self.position]
        enemy = [i for i in gs.enemies if i.position == self.position]
        for item in items:
            item.position = None
            gs.items.remove(item)
            self.inventory.append(item)
        if len(npc) != 0:
            npc = npc[0]
            # dialog
            pass
        if len(enemy) != 0:
            enemy = enemy[0]
            # attack
            pass