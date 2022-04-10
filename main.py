from NPC import get_random_NPC
from enemy import get_random_enemy
from items import BuffItem, HealthItem, Weapon
from player import Player
import random
import map as map_tools

import curses

from utils import Point
from yamlReader import get_random_health_item, get_random_potion, get_random_weapon, import_items

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
                        pass
                    case map_tools.TileType.FLOOR:
                        stdscr.addch(y, x, '.')
                        pass

    def draw_items(self, stdscr):
        for item in self.items:
            if isinstance(item, Weapon):
                stdscr.addch(item.position.y, item.position.x, '?')
            elif item.cocktail:
                stdscr.addch(item.position.y, item.position.x, '\U0001f378')
            else:
                stdscr.addch(item.position.y, item.position.x, '\u1F33D')

            
    def draw_npcs(self, stdscr):
        for item in self.items:
            stdscr.addch(item.position.y, item.position.x, '?')

    def draw_enemies(self, stdscr):
        for item in self.items:
            stdscr.addch(item.position.y, item.position.x, '?')

    def draw_player(self, stdscr):
        stdscr.addch(self.player.position.y, self.player.position.x, '@')

    def draw(self, stdscr):
        # draw map
        self.draw_map(stdscr)
        self.draw_player(stdscr)

    def populate_rooms(self):
        for room in self.room_list:
            itemNum = random.randint(0, room.width // 5)
            usedPoints: list[Point] = [Point(room.x + (room.width // 2), room.y + (room.height // 2))]
            for i in range(itemNum):
                point = Point(room.x + random.randint(0, room.width - 1), room.y + random.randint(0, room.height - 1))
                while point in usedPoints:
                    point = Point(room.x + random.randint(0, room.width - 1), room.y + random.randint(0, room.height - 1))
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
                point = Point(room.x + random.randint(0, room.width - 1), room.y + random.randint(0, room.height - 1))
                while point in usedPoints:
                    point = Point(room.x + random.randint(0, room.width - 1), room.y + random.randint(0, room.height - 1))
                usedPoints.append(point)
                self.npcs.append(get_random_NPC().set_position(point))

            if random.randint(1, 4) >= 2:
                point = usedPoints[0]

                self.enemies.append(get_random_enemy().set_position(point))


def game_loop(stdscr, gs):
    kk = 0
    k = 0
    height, width = stdscr.getmaxyx()
    print(width, height)
    cursor_x = 0
    cursor_y = 0

    curses.curs_set(0)

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    # curses.resizeterm(50, 80)
    stdscr.refresh()


    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):
        # Initialization
        #stdscr.clear()
        height, width = stdscr.getmaxyx()

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        gs.draw(stdscr)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        kk = stdscr.getkey()

        stdscr.refresh()

def main():

    gs = Game()

    curses.wrapper(game_loop, gs)

if __name__ == "__main__":
    main()
