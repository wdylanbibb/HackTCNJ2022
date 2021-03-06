import requests
from draw import dec_index, dec_legend_index, get_idx, inc_index, inc_legend_index, is_show_inventory, is_show_legend, toggle_inventory, toggle_legend
from items import Weapon
from log import log_message
import map
from audio import play_sound
from utils import Point, the
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
        self.score = 0

    def attempt_movement(self, gs, new_position: Point):
        npcs = [i for i in gs.npcs if i.position == self.position + new_position]
        enemies = [i for i in gs.enemies if i.position == self.position + new_position]

        for npc in npcs:
            # dialog
            initial_dialog = npc.talk()
            if initial_dialog:
                self.score += 20
            return PlayerInputResult.Talk
        for enemy in enemies:
            # attack
            self.attack(gs, enemy)
            return PlayerInputResult.Attack

        match gs.map[map.p_idx(self.position + new_position)]:
            case map.TileType.WALL:
                pass
            case map.TileType.FLOOR | map.TileType.DOWNSTAIR:
                self.position += new_position

                items = [item for item in gs.items if item.position == self.position]
                for item in items:
                    log_message(f'You pass by {item.description}.')

                return PlayerInputResult.Move

        return PlayerInputResult.Nothing

    def input(self, event, gs):
        if not is_show_inventory() and not is_show_legend():
            if event == ord('h') or event == curses.KEY_LEFT:
                return self.attempt_movement(gs, Point(-1, 0))
            elif event == ord('j') or event == curses.KEY_DOWN:
                return self.attempt_movement(gs, Point(0, 1))
            elif event == ord('k') or event == curses.KEY_UP:
                return self.attempt_movement(gs, Point(0, -1))
            elif event == ord('l') or event == curses.KEY_RIGHT:
                return self.attempt_movement(gs, Point(1, 0))
            elif event == ord('y'):
                return self.attempt_movement(gs, Point(-1, -1))
            elif event == ord('u'):
                return self.attempt_movement(gs, Point(1, -1))
            elif event == ord('b'):
                return self.attempt_movement(gs, Point(-1, 1))
            elif event == ord('n'):
                return self.attempt_movement(gs, Point(1, 1))

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
            elif event == ord('.'):
                if gs.map[map.p_idx(self.position)] == map.TileType.DOWNSTAIR:
                    self.score += 100
                    self.hp = max(self.max_hp // 2, self.hp)
                    gs.delve_deeper()
            elif event == ord(' '):
                # wait
                can_heal = True

                for enemy in gs.enemies:
                    if self.position.distance(enemy.position) < 7:
                        can_heal = False

                # if can_heal:
                #     self.hp = min(self.hp + 1, self.max_hp)

                return PlayerInputResult.Wait
        elif is_show_legend():
            if event == ord('j') or event == curses.KEY_DOWN:
                inc_legend_index()
            elif event == ord('k') or event == curses.KEY_UP:
                dec_legend_index()
        else:
            if event == ord('j') or event == curses.KEY_DOWN:
                inc_index()
            elif event == ord('k') or event == curses.KEY_UP:
                dec_index()
            elif event == ord(' '):
                if len(self.inventory) == 0: return PlayerInputResult.Nothing
                if not self.inventory[get_idx()].use(self):
                    self.score += 1
                    self.inventory.pop(get_idx())
                return PlayerInputResult.UseItem
            elif event == ord('g'):
                if len(self.inventory) == 0: return PlayerInputResult.Nothing
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
        if event == ord('/'):
            toggle_legend()

        return PlayerInputResult.Nothing

    def attack(self, gs, enemy):
        noneEquipped = self.equipped is None
        if noneEquipped:
            self.equipped = Weapon('your fists', 'your fists', 'Just your fists.', 2)
        for atk in range(self.stats['attackSpeed']):
            dmg = self.equipped.atk * (abs(self.stats['strength'] - 1) * .1 + 1)
            log_message(f'You deal {dmg} damage to {the(enemy.type)}{enemy.type}')
            if enemy.damage(dmg, gs):
                log_message(f'{the(enemy.type).title()}{enemy.type} has been vanquished!')
                gs.enemies.remove(enemy)
                self.score += int(enemy.max_hp)
                if noneEquipped:
                    self.equipped = None
                return
        if noneEquipped:
            self.equipped = None

    def damage(self, amt, enemy):
        self.hp -= amt
        play_sound('hit')
        if self.hp <= 0:
            self.hp = 0
            log_message(f'You were defeated by {the(enemy.type)}{enemy.type}. Game over.')

    def equip_weapon(self, weapon):
        self.equipped = weapon

    def unequip_weapon(self):
        self.equipped = None