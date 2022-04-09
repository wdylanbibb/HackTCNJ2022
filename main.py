from player import Player
import player
import random
import map as map_tools

import curses

from utils import Point

class Game:
    def __init__(self) -> None:
        self.room_list, self.map = map_tools.new_map_rooms_and_corridors(30, 6, 10)
        self.player = Player(Point(self.room_list[0].center()[0], self.room_list[0].center()[1]), "Player", 100, 1, 1)

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

    def draw_player(self, stdscr):
        stdscr.addch(self.player.position.y, self.player.position.x, '@')

    def draw(self, stdscr):
        # draw map
        self.draw_map(stdscr)
        # height, width = stdscr.getmaxyx()
        # stdscr.addstr(0, 0, f'{width} {height}')
        
        self.draw_player(stdscr)


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
