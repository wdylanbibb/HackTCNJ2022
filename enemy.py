
import random
from items import Weapon
from log import log_message
from map import get_2d_map, p_idx
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

    def attack(self):
        log_message(f'{self.type.title()} growls at you.')

    def turn(self, gs):
        dist = int(gs.player.position.distance(self.position))
        if dist < 7:
            if dist <= 1:
                # attack player
                log_message(f'{self.type.title()} attacks you!')
            else:
                # Persue player
                pass


def get_random_enemy():
    choices = ['an ogre', 'a goblin', 'a werewolf', 'an insurance salesman', 'Tom Cruise', 'your mother', 'a ball python', 'Yellow-bellied ferret']
    type = random.choice(choices)
    hp = (len(choices) - choices.index(type)) * random.randint(5, 10)
    weapon = get_random_weapon()
    return Enemy(type, hp, weapon)