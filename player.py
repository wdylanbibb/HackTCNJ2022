from hashlib import new
from draw import dec_index, get_idx, inc_index, is_show_inventory, toggle_inventory
from items import Item, Weapon
from log import log_message
import map
from utils import Point
import curses
from enum import Enum

class PlayerInputResult(Enum):
    Move = 1
    Attack = 2
    Talk = 3
    UseItem = 4
    PickUp = 5
    Wait = 7
    Nothing = 8
    DropItem = 9

class Player:
    def __init__(self, position: Point, name: str, health: int, strength: int, attackSpeed: int) -> None:
        self.name = name
        self.hp = health
        self.max_hp = health
        self.stats = { 'strength': strength, 'attackSpeed': attackSpeed }
        self.position = position
        self.inventory = []
        self.equipped = None

    def attempt_movement(self, gs, new_position: Point):
        npcs = [i for i in gs.npcs if i.position == self.position + new_position]
        enemies = [i for i in gs.enemies if i.position == self.position + new_position]

        for npc in npcs:
            # dialog
            npc.talk()
            return PlayerInputResult.Talk
        for enemy in enemies:
            # attack
            self.attack(gs, enemy)
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

            elif event == ord('g'):
                items = [item for item in gs.items if item.position == self.position]
                for item in items:
                    item.position = None
                    gs.items.remove(item)
                    self.inventory.append(item)
                    log_message(f'You pick up the {item.name}.')
                    if self.equipped is None and isinstance(item, Weapon):
                        self.equip_weapon(item)
                        log_message(f'You equipped the {item.name}.')
                if len(items) > 0:
                    return PlayerInputResult.PickUp
                else:
                    log_message('There was nothing to pick up.')
                    return PlayerInputResult.Nothing
        else:
            if event == ord('j') or event == curses.KEY_DOWN:
                inc_index()
            elif event == ord('k') or event == curses.KEY_UP:
                dec_index()
            elif event == ord(' '):
                if not self.inventory[get_idx()].use(self):
                    self.inventory.pop(get_idx())
                return PlayerInputResult.UseItem
            elif event == ord('g'):
                item = self.inventory[get_idx()]
                item.position = self.position.copy()
                gs.items.append(item)
                self.inventory.remove(item)
                log_message(f'You drop the {item.name}.')
                if item == self.equipped:
                    self.unequip_weapon()
                return PlayerInputResult.DropItem

        if event == ord('i'):
            toggle_inventory()

        return PlayerInputResult.Nothing

    def attack(self, gs, enemy):
        noneEquipped = self.equipped is None
        if noneEquipped:
            self.equipped = Weapon('your fists', 'your fists', 'Just your fists.', 2)
        for atk in range(self.stats['attackSpeed']):
            dmg = self.equipped.atk * (abs(self.stats['strength'] - 1) * .1 + 1)
            log_message(f'You deal {dmg} damage to {enemy.type}')
            if enemy.damage(dmg):
                log_message(f'{enemy.type} has been vanquished!')
                gs.enemies.remove(enemy)
                return
        if noneEquipped:
            self.equipped = None

    def damage(self, amt, enemy):
        self.hp -= amt
        if self.hp <= 0:
            log_message(f'You were defeated by {enemy.type}. Game over.')

    def equip_weapon(self, weapon):
        self.equipped = weapon

    def unequip_weapon(self):
        self.equipped = None