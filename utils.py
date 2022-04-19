from __future__ import annotations
import math

from map import TileType, xy_idx

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

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def copy(self):
        return Point(self.x, self.y)

    def distance(self, other: Point) -> float:
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

class Ray:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def collides(self, map: list[TileType]):
        x1 = self.start.x
        x2 = self.end.x
        y1 = self.start.y
        y2 = self.end.y
 
        dx = x2 - x1
        dy = y2 - y1
        isSteep = abs(dy) > abs(dx)

        if isSteep:
            y1, x1 = x1, y1
            y2, x2 = x2, y2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        
        dx = x2 - x1
        dy = y2 - y1

        error = dx // 2
        ystep = 1 if y1 < y2 else -1

        y = y1
        for x in range(x1, x2 + 1):
            coords = (y, x) if isSteep else (x, y)
            if map[xy_idx(coords[0], coords[1])] == TileType.WALL:
                return True
            error -= abs(dy)
            # print(coords)
            if error < 0:
                y += ystep
                error += dx

        return False


# Returns an if string parameter n starts with a vowel, a otherwise (i think it's name is pretty funny)
def a(n) -> str:
    if len(n) < 1:
        return ""
    elif n[0].lower() in ['a', 'e', 'i', 'o', 'u']:
        return "an"
    else:
        return "a"

def the(n) -> str:
    if n[0].isupper():
        return ''
    
    return 'the '