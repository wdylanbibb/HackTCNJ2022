from random import random
import yaml
import random
import requests
from items import BuffItem, HealthItem, Weapon, Item

items = None
npcLines = None

def import_items():
    global items, npcLines
    with open('weapons.yaml') as file:
        items = yaml.safe_load(file)
    with open('npcs.yaml') as file:
        npcLines = yaml.safe_load(file)

def get_random_primary_line():
    return random.choice(npcLines['primary'].split('\n'))

def get_random_return_line():
    return random.choice(npcLines['return'].split('\n'))

def get_annoyed_dialog():
    return random.choice(npcLines['annoyed'].split('\n'))

def get_random_weapon() -> Weapon:
    weapons = items['weapons']
    choice = random.choice([i for i in weapons.keys()])
    weapon = Weapon(choice, weapons[choice]['description'], weapons[choice]['detailedDescription'], weapons[choice]['damage'])
    return weapon

def get_random_health_item() -> HealthItem:
    food = requests.get('https://www.themealdb.com/api/json/v1/1/random.php').json()['meals'][0]
    uses = 2 if random.randint(1, 30) == 1 else 1
    random.seed(food['idMeal'])
    healthItem = HealthItem(food['strMeal'], food['strMeal'], f'This is a {random.choice(["tasty", "delicious", "yummy", "nutritious", "hearty", "wholesome", "ready-to-eat"])} plate of {food["strMeal"].lower()}.', random.randint(1, 10), uses=uses)
    return healthItem

def get_random_potion() -> Item:
    drink = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php').json()['drinks'][0]
    random.seed(drink['idDrink'])
    stat = random.randint(0, 2)
    if stat == 2:
        amt = random.randint(1, 10)
        return HealthItem(drink['strDrink'], drink['strDrink'], f'In a glass is an intoxicating {drink["strDrink"]}.', amt, cocktail=True)
    amt = random.randint(1, 3)
    if random.randint(1, 10) == 1: amt *= -1
    return BuffItem(drink['strDrink'], drink['strDrink'], f'In a glass is an intoxicating {drink["strDrink"]}.', ['strength', 'attackSpeed'][stat], amt)

import_items()
print(get_random_primary_line())