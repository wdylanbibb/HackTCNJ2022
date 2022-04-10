
import random
from items import Weapon
from log import log_message
from map import TileType, get_2d_map, get_path_to, p_idx, xy_idx
from utils import Point
from yamlReader import get_random_weapon
import astar


class Enemy:
    def __init__(self, enemyType: str, hp: int, weapon: Weapon) -> None:
        self.type = enemyType
        self.hp = hp
        self.max_hp = hp
        self.weapon = weapon

    def __str__(self) -> str:
        return f'<Enemy - Type: {self.type}, Defense: {self.defense}, HP: {self.hp}, Weapon: {self.weapon}>'

    def set_position(self, position: Point):
        self.position = position
        return self

    def damage(self, amt):
        self.hp -= amt
        if self.hp <= 0:
            return True
        return False

    def attack(self, player):
        player.damage(self.weapon.atk * 1.2, self)

    def turn(self, gs):
        dist = gs.player.position.distance(self.position)
        if dist < 7:
            if dist <= 1:
                # attack player
                self.attack(gs.player)
                log_message(f'{self.type.title()} attacks you for {self.weapon.atk * 1.2:.1f} damage!!')
            else:
                # Persue player
                
                blocked_map = gs.map.copy()
                for enemy in gs.enemies:
                    if enemy == self:
                        continue
                    blocked_map[xy_idx(enemy.position.x, enemy.position.y)] = TileType.WALL
                for npc in gs.npcs:
                    blocked_map[xy_idx(npc.position.x, npc.position.y)] = TileType.WALL
                
                path = get_path_to(blocked_map, self.position, gs.player.position)
                
                self.position = Point(path[1 if len(path) > 1 else 0][0], path[1 if len(path) > 1 else 0][1])

def get_random_enemy():
    choices = ['an ogre', 'a goblin', 'a werewolf', 'an insurance salesman', 'Tom Cruise', 'your mother', 'a ball python', 'Yellow-bellied ferret']
    type = random.choice(choices)
    hp = (len(choices) - choices.index(type)) * random.randint(5, 10)
    weapon = get_random_weapon()
    return Enemy(type, hp, weapon)