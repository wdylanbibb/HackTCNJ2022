from __future__ import annotations
from enum import Enum
import random

class TileType(Enum):
    WALL = 1
    FLOOR = 2

MAP_WIDTH = 80
MAP_HEIGHT = 50
MAP_SIZE = MAP_WIDTH * MAP_HEIGHT

class Rect:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersect(self, other: Rect) -> bool:
        if self.x == self.x + self.width or self.y == self.y + self.height or other.x == other.x + other.width or other.y == other.y + other.height:
            return False

        if self.x >= other.x + other.width or other.x >= self.x + self.width:
            return False

        if self.y >= other.y + other.height or other.y >= self.y + self.height:
            return False

        return True

    def center(self) -> tuple(int, int):
        return (self.x + (self.width // 2), self.y + (self.height // 2))

    def __str__(self) -> str:
        return f'<{self.x},{self.y},{self.width},{self.height}>'

Map = list[TileType]

def roll_dice(n: int, die_type: int) -> int:
    return sum([random.randint(1, die_type + 1) for _ in range(n)])

def xy_idx(x: int, y: int) -> int:
    return (y * MAP_WIDTH) + x

def apply_room_to_map(room: Rect, map: Map):
    # print(room)
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
        if idx > 0 and idx < 80*50:
            map[idx] = TileType.FLOOR

def new_map_rooms_and_corridors(max_rooms: int, min_size: int, max_size: int) -> tuple(list[Rect], list[TileType]):
    map = [TileType.WALL] * MAP_SIZE

    rooms: list[Rect] = []

    for _i in range(0, max_rooms):
        w = random.randint(min_size, max_size)
        h = random.randint(min_size, max_size)
        x = roll_dice(1, 80 - w - 1) - 1
        y = roll_dice(1, 50 - h - 1) - 1
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

    return (rooms, map)

def draw_map(map: Map):
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            match map[xy_idx(x, y)]:
                case TileType.WALL:
                    print('#', end='')
                case TileType.FLOOR:
                    print('.', end='')
                case _:
                    print('!', end='')
        print()