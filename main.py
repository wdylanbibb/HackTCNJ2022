import requests
from NPC import get_random_NPC
from draw import draw_box, draw_inventory, draw_label, draw_label_centered, draw_legend, toggle_inventory
from enemy import get_random_enemy
from items import Weapon
from player import Player, PlayerInputResult
import random
import map as map_tools
import log

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
        self.is_dead = False
        self.depth = 1
        self.introduced = False

    def draw_map(self, stdscr):
        for x in range(map_tools.MAP_WIDTH):
            for y in range(map_tools.MAP_HEIGHT):
                curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
                match self.map[map_tools.xy_idx(x, y)]:
                    case map_tools.TileType.WALL:
                        stdscr.addch(y, x, '#', curses.color_pair(1))
                    case map_tools.TileType.FLOOR:
                        stdscr.addch(y, x, ' ')
                    case map_tools.TileType.DOWNSTAIR:
                        stdscr.addch(y, x, '>')

    def draw_items(self, stdscr):
        for item in self.items:
            if isinstance(item, Weapon):
                stdscr.addstr(item.position.y, item.position.x, '/')
            elif item.cocktail:
                stdscr.addstr(item.position.y, item.position.x, 'u')
            else:
                stdscr.addstr(item.position.y, item.position.x, '%')


    def draw_npcs(self, stdscr):
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        for npc in self.npcs:
            stdscr.addstr(npc.position.y, npc.position.x, '☺', curses.color_pair(2))

    def draw_enemies(self, stdscr):
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        for enemy in self.enemies:
            stdscr.addstr(enemy.position.y, enemy.position.x, enemy.type.lower()[0], curses.color_pair(3))

    def draw_player(self, stdscr):
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        stdscr.addch(self.player.position.y, self.player.position.x, '@', curses.color_pair(4))

    def draw_ui(self, stdscr):
        draw_box(stdscr, Rect(0, 30, 80, 6))

        draw_label(stdscr, Point(1, 0), f' Depth: {self.depth} ')

        draw_label(stdscr, Point(2, 30), " " + self.player.name + " ")

        draw_label(stdscr, Point(max(20, len(self.player.name) + 6), 30), " " + str(int(self.player.hp)) + " / " + str(self.player.max_hp) + " ")

        log.draw_messages(stdscr)

    def draw(self, stdscr):
        # draw map
        self.draw_map(stdscr)
        self.draw_items(stdscr)
        self.draw_enemies(stdscr)
        self.draw_npcs(stdscr)
        self.draw_player(stdscr)
        draw_inventory(stdscr, self.player.inventory, self.player.equipped)
        draw_legend(stdscr, [{'key': '>', 'value': 'stairs'}, {'key': 'u', 'value': 'cocktail'}, {'key': '%', 'value': 'food'}, {'key': '/', 'value': 'weapon'}, {'key': 'y', 'value': 'Your Mother'}, {'key': 't', 'value': 'Tom Cruise'}, {'key': 'w', 'value': 'werewolf'}, {'key': 'o', 'value': 'ogre'}, {'key': 'g', 'value': 'goblin'}, {'key': 'b', 'value': 'ball python'}, {'key': 'i', 'value': 'insurance salesman'}, {'key': 'r', 'value': 'rose-bellied ferret'}])
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

    def delve_deeper(self):
        self.room_list, self.map = map_tools.new_map_rooms_and_corridors(30, 6, 10)
        self.player.position = Point(self.room_list[0].center()[0], self.room_list[0].center()[1])
        self.items = []
        self.enemies = []
        self.npcs = []
        import_items()
        self.populate_rooms()
        self.depth += 1

        log.clear_log()
        log.log_message("You descend into the dungeon...")
leaderboard = False

def game_loop(stdscr, gs):
    kk = ''
    kw = 0
    k = 0
    height, width = stdscr.getmaxyx()
    cursor_x = 0
    cursor_y = 0

    stdscr.nodelay(True)

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    # curses.resizeterm(50, 80)
    stdscr.refresh()

    curses.mousemask(1)
    # curses.echo(True)

    
    player_name = ''

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    log.log_message("Welcome to the Dungeon of Curses!")

    # Loop where k is the last character pressed
    while not (gs.introduced and k == ord('q')):
        # Initialization
        if k == curses.KEY_RESIZE:
            curses.resize_term(0, 0)
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        # print(height, width)

        # if k == curses.KEY_RESIZE:
        #     stdscr.addstr(0, 0, f'{width}, {height}')
        if not gs.is_dead:
            if k == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                cursor_x = mx
                cursor_y = my

                [log.log_message("You see " + enemy.description) for enemy in gs.enemies if enemy.position == Point(mx, my)]
                [log.log_message("You see " + npc.name) for npc in gs.npcs if npc.position == Point(mx, my)]
                [log.log_message("You see a(n) " + item.name) for item in gs.items if item.position == Point(mx, my)]
            else:
                if gs.introduced:
                    match gs.player.input(k, gs):
                        case PlayerInputResult.Move | PlayerInputResult.Attack | PlayerInputResult.Talk | PlayerInputResult.UseItem | PlayerInputResult.PickUp | PlayerInputResult.Wait | PlayerInputResult.DropItem:
                            # Enemy Move
                            gs.npc_turn()
                            gs.enemy_turn()

                            if gs.player.hp <= 0:
                                gs.is_dead = True
                        case PlayerInputResult.Nothing:
                            # Nothing
                            pass
                # else:
                #     if kk == 0:
                #         player_name = ' '
                #     else:
                #         player_name = str(kk)



        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)
        global leaderboard


        if height <= 37 - 1 or width <= 80 - 1:
            curses.curs_set(0)
            draw_label_centered(stdscr, (height // 2) - 1, 'Your screen is too small!')
            draw_label_centered(stdscr, (height // 2), 'Required: 80x37')
            draw_label_centered(stdscr, (height // 2) + 1, f'Current Size: {width}x{height}')
        elif gs.is_dead:
            curses.curs_set(0)
            draw_box(stdscr, Rect(0, 0, width - 1, height - 1))

            if not leaderboard:
                draw_label_centered(stdscr, (height // 2) - 7, '   _____                         ____                 ')
                draw_label_centered(stdscr, (height // 2) - 6, '  / ____|                       / __ \                ')
                draw_label_centered(stdscr, (height // 2) - 5, ' | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ ')
                draw_label_centered(stdscr, (height // 2) - 4, " | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|")
                draw_label_centered(stdscr, (height // 2) - 3, ' | |__| | (☠| | | | | | |  __/ | |__| |\ V /  __/ |   ')
                draw_label_centered(stdscr, (height // 2) - 2, '  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   ')
                draw_label_centered(stdscr, (height // 2) - 1, '                                                      ')
                draw_label_centered(stdscr, (height // 2), f'☠ Score: {gs.player.score} ☠')
                draw_label_centered(stdscr, (height // 2) + 1, 'Press l to view leaderboard.')
                draw_label_centered(stdscr, (height // 2) + 2, '☠ Press Q to Quit ☠')
            else:
                curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
                curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
                curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_BLACK)
                curses.init_pair(9, curses.COLOR_BLUE, curses.COLOR_BLACK)
                draw_label_centered(stdscr, 3, '  _      ______          _____  ______ _____  ____   ____          _____  _____  ', curses.color_pair(6))
                draw_label_centered(stdscr, 4, ' | |    |  ____|   /\   |  __ \|  ____|  __ \|  _ \ / __ \   /\   |  __ \|  __ \ ', curses.color_pair(6))
                draw_label_centered(stdscr, 5, ' | |    | |__     /  \  | |  | | |__  | |__) | |_) | |  | | /  \  | |__) | |  | |', curses.color_pair(6))
                draw_label_centered(stdscr, 6, ' | |    |  __|   / /\ \ | |  | |  __| |  _  /|  _ <| |  | |/ /\ \ |  _  /| |  | |', curses.color_pair(6))
                draw_label_centered(stdscr, 7, ' | |____| |____ / ____ \| |__| | |____| | \ \| |_) | |__| / ____ \| | \ \| |__| |', curses.color_pair(6))
                draw_label_centered(stdscr, 8, ' |______|______/_/    \_\_____/|______|_|  \_\____/ \____/_/    \_\_|  \_\_____/ ', curses.color_pair(6))
                draw_label_centered(stdscr, 9, '─────────────────────────────────────────────────────────────────────────────────', curses.color_pair(6))
                highscores = requests.get('https://dungeon-of-curses.herokuapp.com/highscores').json()
                for i, score in enumerate(highscores):
                    if i == 0:
                        draw_label_centered(stdscr, i + 11, f'{score["user"]}: {score["score"]} points', curses.color_pair(7))
                    elif i == 1:
                        draw_label_centered(stdscr, i + 11, f'{score["user"]}: {score["score"]} points', curses.color_pair(8))
                    elif i == 2:
                        draw_label_centered(stdscr, i + 11, f'{score["user"]}: {score["score"]} points', curses.color_pair(9))
                    else:
                        draw_label_centered(stdscr, i + 11, f'{score["user"]}: {score["score"]} points')
                draw_label_centered(stdscr, 20, 'Press l to stop viewing leaderboard.');
                draw_label_centered(stdscr, 21, '☠ Press Q to Quit ☠')
            if (k == ord('l')):
                leaderboard = not leaderboard
        elif not gs.introduced:
            curses.curs_set(0)

            if 32 <= k <= 126:
                player_name += chr(k) if k in range(0x110000) else ''
            else:
                if k == 127:
                    player_name = player_name[:-1]
                elif k == ord('\n'):
                    gs.introduced = True
                    gs.player.name = player_name

            curses.init_pair(10, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(11, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            draw_label_centered(stdscr, (height // 2) - 10, "  (                                                                                       ", curses.color_pair(10))
            draw_label_centered(stdscr, (height // 2) - 9, "  )\ )                                              (        (                            ", curses.color_pair(10))
            draw_label_centered(stdscr, (height // 2) - 8, " (()/(     (          (  (     (                    )\ )     )\     (   (          (      ", curses.color_pair(10))
            draw_label_centered(stdscr, (height // 2) - 7, "  /(_))   ))\   (     )\))(   ))\  (    (       (  (()/(   (((_)   ))\  )(   (    ))\ (   ", curses.color_pair(10))
            draw_label_centered(stdscr, (height // 2) - 6, " (_))_   /((_)  )\ ) ((_))\  /((_) )\   )\ )    )\  /(_))  )\___  /((_)(()\  )\  /((_))\  ", curses.color_pair(10))
            draw_label_centered(stdscr, (height // 2) - 5, "  |   \ (_))(  _(_/(  (()(_)(_))  ((_) _(_/(   ((_)(_) _| ((/ __|(_))(  ((_)((_)(_)) ((_) ", curses.color_pair(10))
            draw_label_centered(stdscr, (height // 2) - 4, "  | |) || || || ' \))/ _` | / -_)/ _ \| ' \)) / _ \ |  _|  | (__ | || || '_|(_-</ -_)(_-< ", curses.color_pair(11))
            draw_label_centered(stdscr, (height // 2) - 3, "  |___/  \_,_||_||_| \__, | \___|\___/|_||_|  \___/ |_|     \___| \_,_||_|  /__/\___|/__/ ", curses.color_pair(11))
            draw_label_centered(stdscr, (height // 2) - 2, "                     |___/                                                                ", curses.color_pair(11))
            draw_label_centered(stdscr, (height // 2) - 1, 'Hello, traveller. What is your name?')
            draw_label_centered(stdscr, (height // 2), player_name)
            draw_box(stdscr, Rect(0, 0, width - 1, height - 1))
        else:
            curses.curs_set(1)
            gs.draw(stdscr)

        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        stdscr.refresh()

def main():

    gs = Game()

    curses.wrapper(game_loop, gs)

if __name__ == "__main__":
    main()

# def draw_menu(stdscr):
#     stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

#     editwin = curses.newwin(5,30, 2,1)
#     rectangle(stdscr, 1,0, 1+5+1, 1+30+1)
#     stdscr.refresh()

#     box = Textbox(editwin)

#     # Let the user edit until Ctrl-G is struck.
#     box.edit()

#     # Get resulting contents
#     message = box.gather()

#     print(message)

# def main():
#     curses.wrapper(draw_menu)

# if __name__ == "__main__":
#     main()