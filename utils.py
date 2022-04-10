from __future__ import annotations
import math

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

    def distance(self, other: Point) -> float:
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)