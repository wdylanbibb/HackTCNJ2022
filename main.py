from NPC import get_random_NPC
from draw import draw_box, draw_inventory, draw_label, draw_label_centered, toggle_inventory
from enemy import get_random_enemy
from items import BuffItem, HealthItem, Weapon
from player import Player, PlayerInputResult
import random
import map as map_tools
import log
from enum import Enum

import curses

from yamlReader import get_random_health_item, get_random_potion, get_random_weapon, import_items
from utils import Point, Rect

class Game:
    def __init__(self) -> None:
        self.room_list, self.map = map_tools.new_map_rooms_and_corridors(30, 6, 10)
        self.player = Player(Point(self.room_list[0].center()[0], self.room_list[0].center()[1]), "Player", 100, 1, 1)
        self.items = []
        self.enemies = []
        self.npcs = []
        import_items()
        self.populate_rooms()

    def draw_map(self, stdscr):
        for x in range(map_tools.MAP_WIDTH):
            for y in range(map_tools.MAP_HEIGHT):
                match self.map[map_tools.xy_idx(x, y)]:
                    case map_tools.TileType.WALL:
                        stdscr.addch(y, x, '#')
                    case map_tools.TileType.FLOOR:
                        stdscr.addch(y, x, '.')

    def draw_items(self, stdscr):
        for item in self.items:
            if isinstance(item, Weapon):
                stdscr.addstr(item.position.y, item.position.x, 'w')
            elif item.cocktail:
                stdscr.addstr(item.position.y, item.position.x, 'c')
            else:
                stdscr.addstr(item.position.y, item.position.x, 'f')


    def draw_npcs(self, stdscr):
        for npc in self.npcs:
            stdscr.addstr(npc.position.y, npc.position.x, 'n')

    def draw_enemies(self, stdscr):
        for enemy in self.enemies:
            stdscr.addstr(enemy.position.y, enemy.position.x, 'e')

    def draw_player(self, stdscr):
        stdscr.addch(self.player.position.y, self.player.position.x, '@')

    def draw_ui(self, stdscr):
        draw_box(stdscr, Rect(0, 30, 80, 6))

        draw_label(stdscr, Point(2, 30), " " + self.player.name + " ")

        draw_label(stdscr, Point(20, 30), " " + str(self.player.hp) + " / " + str(self.player.max_hp) + " ")

        log.draw_messages(stdscr)

    def draw(self, stdscr):
        # draw map
        self.draw_map(stdscr)
        self.draw_items(stdscr)
        self.draw_enemies(stdscr)
        self.draw_npcs(stdscr)
        self.draw_player(stdscr)
        draw_inventory(stdscr, self.player.inventory, self.player.equipped)
        self.draw_ui(stdscr)

    def populate_rooms(self):
        for room in self.room_list[1:]:
            itemNum = random.randint(0, room.width // 5)
            usedPoints: list[Point] = [Point(room.x + (room.width // 2), room.y + (room.height // 2))]
            for i in range(itemNum):
                point = Point(room.x + 1 + random.randint(0, room.width - 2), room.y + 1 + random.randint(0, room.height - 2))
                while point in usedPoints:
                    point = Point(room.x + 1 + random.randint(0, room.width - 2), room.y + 1 + random.randint(0, room.height - 2))
                usedPoints.append(point)
                match random.randint(0, 2):
                    case 0:
                        item = get_random_weapon().set_position(point)
                    case 1:
                        item = get_random_health_item().set_position(point)
                    case 2:
                        item = get_random_potion().set_position(point)
                self.items.append(item)
            if random.randint(1, 20) == 1:
                point = Point(room.x + 1 + random.randint(0, room.width - 2), room.y + 1 + random.randint(0, room.height - 2))
                while point in usedPoints:
                    point = Point(room.x + 1 + random.randint(0, room.width - 2), room.y + 1 + random.randint(0, room.height - 2))
                usedPoints.append(point)
                self.npcs.append(get_random_NPC().set_position(point))

            if random.randint(1, 4) >= 2:
                point = usedPoints[0]

                self.enemies.append(get_random_enemy().set_position(point))
    
    def enemy_turn(self):
        for enemy in self.enemies:
            enemy.turn(self)

    def npc_turn(self):
        for npc in self.npcs:
            npc.turn(self)


def game_loop(stdscr, gs):
    kk = 0
    k = 0
    height, width = stdscr.getmaxyx()
    cursor_x = 0
    cursor_y = 0

    curses.curs_set(1)
    stdscr.nodelay(True)

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    # curses.resizeterm(50, 80)
    stdscr.refresh()

    curses.mousemask(1)


    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    log.log_message("Welcome to the Dungeon of Curses!")

    # Loop where k is the last character pressed
    while (k != ord('q')):
        # Initialization
        if k == curses.KEY_RESIZE:
            curses.resize_term(0, 0)
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        # print(height, width)

        # if k == curses.KEY_RESIZE:
        #     stdscr.addstr(0, 0, f'{width}, {height}')
        if k == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            cursor_x = mx
            cursor_y = my

            [log.log_message("You see " + enemy.type) for enemy in gs.enemies if enemy.position == Point(mx, my)]
            [log.log_message("You see " + npc.name) for npc in gs.npcs if npc.position == Point(mx, my)]
            [log.log_message("You see a(n) " + item.name) for item in gs.items if item.position == Point(mx, my)]
        else:
            match gs.player.input(k, gs):
                case PlayerInputResult.Move:
                    # Enemy Move
                    gs.npc_turn()
                    gs.enemy_turn()
                    pass
                case PlayerInputResult.Attack:
                    # Enemy Move
                    gs.npc_turn()
                    gs.enemy_turn()
                    pass
                case PlayerInputResult.Talk:
                    # Enemy Move
                    gs.npc_turn()
                    gs.enemy_turn()
                    pass
                case PlayerInputResult.UseItem:
                    # Enemy Move
                    gs.npc_turn()
                    gs.enemy_turn()
                    pass
                case PlayerInputResult.PickUp:
                    # Enemy Move
                    gs.npc_turn()
                    gs.enemy_turn()
                    pass
                case PlayerInputResult.Wait:
                    # Enemy Move
                    gs.npc_turn()
                    gs.enemy_turn()
                    pass
                case PlayerInputResult.DropItem:
                    # Enemy Move
                    gs.npc_turn()
                    gs.enemy_turn()
                    pass
                case PlayerInputResult.Nothing:
                    # Nothing
                    pass

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)


        if height <= 37 - 1 or width <= 80 - 1:
            draw_label_centered(stdscr, (height // 2) - 1, 'Your screen is too small!')
            draw_label_centered(stdscr, (height // 2), 'Required: 80x37')
            draw_label_centered(stdscr, (height // 2) + 1, f'Current Size: {width}x{height}')
        else:
            gs.draw(stdscr)
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        # kk = stdscr.getkey()

        stdscr.refresh()

def main():

    gs = Game()

    curses.wrapper(game_loop, gs)

if __name__ == "__main__":
    main()
