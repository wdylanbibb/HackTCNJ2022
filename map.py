from __future__ import annotations
from enum import IntEnum
import random

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class TileType(IntEnum):
    WALL = 0
    FLOOR = 1
    DOWNSTAIR = 2

MAP_WIDTH = 80
MAP_HEIGHT = 30
MAP_SIZE = MAP_WIDTH * MAP_HEIGHT

Map = list[TileType]

def roll_dice(n: int, die_type: int) -> int:
    return sum([random.randint(1, die_type + 1) for _ in range(n)])

def xy_idx(x: int, y: int) -> int:
    return (y * MAP_WIDTH) + x

def p_idx(p) -> int:
    return (p.y * MAP_WIDTH) + p.x

def apply_room_to_map(room, map: Map):
    for y in range(room.y + 1, room.y + room.height):
        for x in range(room.x + 1, room.x + room.width):
            map[xy_idx(x, y)] = TileType.FLOOR

def apply_horizontal_tunnel(map: Map, x1: int, x2: int, y: int):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        idx= xy_idx(x, y)
        if idx > 0 and idx < MAP_SIZE:
            map[idx] = TileType.FLOOR

def apply_vertical_tunnel(map: Map, y1: int, y2: int, x: int):
    for y in range(min(y1,y2), max(y1,y2) + 1):
        idx = xy_idx(x, y)
        if idx > 0 and idx < MAP_WIDTH*MAP_HEIGHT:
            map[idx] = TileType.FLOOR

def new_map_rooms_and_corridors(max_rooms: int, min_size: int, max_size: int) -> tuple(list, list[TileType]):
    from utils import Rect
    map = [TileType.WALL] * MAP_SIZE

    rooms = []

    for _i in range(0, max_rooms):
        w = random.randint(min_size, max_size)
        h = random.randint(min_size, max_size)
        x = roll_dice(1, MAP_WIDTH - w - 1) - 1
        y = roll_dice(1, MAP_HEIGHT - h - 1) - 1
        new_room = Rect(x, y, w, h)
        ok = True
        for other_room in rooms:
            if new_room.intersect(other_room):
                ok = False
        if ok:
            apply_room_to_map(new_room, map)

            if not len(rooms) == 0:
                (new_x, new_y) = new_room.center()
                (prev_x, prev_y) = rooms[len(rooms)-1].center()
                if random.randint(0, 2) == 1:
                    apply_horizontal_tunnel(map, prev_x, new_x, prev_y)
                    apply_vertical_tunnel(map, prev_y, new_y, new_x)
                else:
                    apply_vertical_tunnel(map, prev_y, new_y, prev_x)
                    apply_horizontal_tunnel(map, prev_x, new_x, new_y)

            rooms.append(new_room)

    stair_pos_x, stair_pos_y = rooms[-1].center()
    stairs_idx = xy_idx(stair_pos_x, stair_pos_y)
    map[stairs_idx] = TileType.DOWNSTAIR

    return (rooms, map)

def get_2d_map(map: Map):
    map_2d = []

    for y in range(MAP_HEIGHT):
        map_2d.append(map[xy_idx(0, y):xy_idx(0, y) + MAP_WIDTH])

    return map_2d

def print_2d_map(map: Map):
    map_2d = get_2d_map(map)

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            match map_2d[y][x]:
                case TileType.FLOOR:
                    print('.', end='')
                case TileType.WALL:
                    print('#', end='')
                case TileType.DOWNSTAIR:
                    print('>', end='')
        print()


def get_path_to(map, start, end):
    grid = Grid(matrix=get_2d_map(map))

    start = grid.node(start.x, start.y)
    end = grid.node(end.x, end.y)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(start, end, grid)

    return path