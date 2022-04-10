
from cmath import log
import random
from items import Weapon
from log import log_message
from map import TileType, get_2d_map, get_path_to, p_idx, xy_idx
from utils import Point, a
from yamlReader import get_random_weapon

class Enemy:
    def __init__(self, enemyType: str, hp: int, weapon: Weapon) -> None:
        self.type = enemyType
        self.description = a(self.type) + " " + self.type
        if self.type[0].isupper():
            self.description = self.type
        self.hp = hp
        self.max_hp = hp
        self.weapon = weapon

    def __str__(self) -> str:
        return f'<Enemy - Type: {self.type}, Defense: {self.defense}, HP: {self.hp}, Weapon: {self.weapon}>'

    def set_position(self, position: Point):
        self.position = position
        return self

    def damage(self, amt, gs):
        self.hp -= amt
        if self.hp <= 0:
            item = self.weapon
            item.position = self.position.copy()
            gs.items.append(item)
            return True
        return False

    def attack(self, player):
        player.damage(self.weapon.atk, self)

    def turn(self, gs):
        dist = gs.player.position.distance(self.position)
        if dist < 7:
            if dist <= 1:
                # attack player
                self.attack(gs.player)
                log_message(f'{self.type.title()} attacks you for {self.weapon.atk:.1f} damage!!')
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

                if len(path) > 0:
                    self.position = Point(path[1 if len(path) > 1 else 0][0], path[1 if len(path) > 1 else 0][1])

def get_random_enemy(depth: int):
    choices = ['The Jolly Green Giant', 'ogre', 'goblin', 'werewolf', 'insurance salesman', 'Tom Cruise', 'Your Mother', 'ball python', 'rose-bellied ferret']
    type = random.choice(choices)
    hp = (len(choices) - choices.index(type)) * random.randint(5, 10) * (log(depth, 5) + 1).real
    weapon = get_random_weapon()
    return Enemy(type, hp, weapon)