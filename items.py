import math
from log import log_message
from utils import Point


class Item:
    def __init__(self, name: str, description: str, detailedDesc: str, cocktail=False) -> None:
        self.name = name
        self.description = description
        self.detailedDesc = detailedDesc
        self.cocktail = cocktail

    def set_position(self, position: Point):
        self.position = position
        return self
    
    def get_name(self):
        return self.name

    def use(self, player):
        return True

class Weapon(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, atk: int) -> None:
        super().__init__(name, description, detailedDesc)
        self.atk = atk
    
    def get_name(self):
        return self.name

    def use(self, player):
        if player.equipped == self:
            player.unequip_weapon()
            log_message(f'You unequipped the {self.name}.')
        else:
            player.equip_weapon(self)
            log_message(f'You equipped the {self.name}.')
        return True

    def __str__(self) -> str:
        return f'<Weapon - Name: {self.name}, Description: {self.description}, Detailed Description: {self.detailedDesc}, ATK: {self.atk}>'

class HealthItem(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, healingAmt: int, cocktail=False, uses: int = 1) -> None:
        super().__init__(name, description, detailedDesc, cocktail=cocktail)
        self.healingAmt = healingAmt
        self.uses = uses

    def use(self, player):
        self.uses -= 1
        player.hp = min(player.max_hp, player.hp + self.healingAmt)
        log_message(f'You ate/drank the {self.name} and gained {self.healingAmt} health.')
        if self.uses == 0:
            log_message('You finished it! It is gone from your inventory.')
            return False
        return True

    def get_name(self):
        return f'{self.name} ({self.uses} uses left)'

    def __str__(self) -> str:
        return f'<HealthItem - Name: {self.name}, Description: {self.description}, Detailed Description: {self.detailedDesc}, Healing: {self.healingAmt}, Uses: {self.uses}>'


class BuffItem(Item):
    def __init__(self, name: str, description: str, detailedDesc: str, stat: str, buff: int) -> None:
        super().__init__(name, description, detailedDesc, cocktail=True)
        self.stat = stat
        self.buff = buff
    
    def get_name(self):
        return self.name

    def use(self, player):
        player.stats[self.stat] += self.buff
        if self.buff > 0:
            log_message(f'You drank the {self.name} and suddenly gained {str(self.buff)} {" ".join([i.lower() for i in self.stat.split(r"[A-Z]")])}!')
        else:
            log_message(f'You drank the {self.name} and suddenly lost {str(self.buff)} {" ".join([i.lower() for i in self.stat.split(r"[A-Z]")])}!')
        return False

    def __str__(self) -> str:
        return f'<BuffItem - Name: {self.name}, Description: {self.description}, Detailed Description: {self.detailedDesc}, Stat: {self.stat}, Buff: {self.buff}>'
