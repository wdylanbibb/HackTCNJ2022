from hashlib import new
from draw import dec_index, get_idx, inc_index, is_show_inventory, toggle_inventory
from log import log_message
import map
from utils import Point
import curses
import log
from enum import Enum

class PlayerInputResult(Enum):
    Move = 1
    Attack = 2
    Talk = 3
    UseItem = 4
    PickUp = 5
    Wait = 7
    Nothing = 8

class Player:
    def __init__(self, position: Point, name: str, health: int, strength: int, attackSpeed: int) -> None:
        self.name = name
        self.hp = health
        self.max_hp = health
        self.stats = { 'strength': strength, 'attackSpeed': attackSpeed }
        self.position = position
        self.inventory = []

    def attempt_movement(self, gs, new_position: Point):
        npcs = [i for i in gs.npcs if i.position == self.position + new_position]
        enemies = [i for i in gs.enemies if i.position == self.position + new_position]

        for npc in npcs:
            # dialog
            log_message(f'> {npc.name} - "{npc.next_message()}"')
            return PlayerInputResult.Talk
        for enemy in enemies:
            # attack
            log.log_message(f'{enemy.type} growls at you, but their feet stay planted in the ground.')
            return PlayerInputResult.Attack

        if gs.map[map.p_idx(self.position + new_position)] == map.TileType.FLOOR:
            self.position += new_position
            return PlayerInputResult.Move

        return PlayerInputResult.Nothing

    def input(self, event, gs):
        if not is_show_inventory():
            if event == ord('h') or event == curses.KEY_LEFT:
                return self.attempt_movement(gs, Point(-1, 0))
            elif event == ord('j') or event == curses.KEY_DOWN:
                return self.attempt_movement(gs, Point(0, 1))
            elif event == ord('k') or event == curses.KEY_UP:
                return self.attempt_movement(gs, Point(0, -1))
            elif event == ord('l') or event == curses.KEY_RIGHT:
                return self.attempt_movement(gs, Point(1, 0))
        else:
            if event == ord('j') or event == curses.KEY_DOWN:
                inc_index()
            elif event == ord('k') or event == curses.KEY_UP:
                dec_index()

            return PlayerInputResult.Nothing

        if event == ord('i'):
            toggle_inventory()

        return PlayerInputResult.Nothing


        items = [i for i in gs.items if i.position == self.position]

        for item in items:
            item.position = None
            gs.items.remove(item)
            self.inventory.append(item)
