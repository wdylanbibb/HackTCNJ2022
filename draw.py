from log import log_message
from utils import Point, Rect
from enum import Enum





def draw_box(stdscr, rect: Rect):
    stdscr.addstr(rect.y, rect.x, "┌" + ("─" * (rect.width - 2)) + "┐")
    for y in range(1, rect.height):
        stdscr.addstr(rect.y + y, rect.x, "│" + (" " * (rect.width - 2)) + "│")
    stdscr.addstr(rect.y + rect.height, rect.x, "└" + ("─" * (rect.width - 2)) + "┘")

def draw_label(stdscr, pos: Point, msg: str):
    _, width = stdscr.getmaxyx()

    stdscr.addstr(pos.y, max(pos.x, 0), msg[abs(min(pos.x, 0)):width])

def draw_label_centered(stdscr, y: int, msg: str):
    _, width = stdscr.getmaxyx()
    draw_label(stdscr, Point((width // 2) - (len(msg) // 2), y), msg)

showInventory = False
invIndex = 0
invStartIdx = 0
lastIndex = -1

def toggle_inventory() -> bool:
    global showInventory, invIndex, invStartIdx, lastIndex
    showInventory = not showInventory
    invIndex = 0
    invStartIdx = 0
    lastIndex = -1

def is_show_inventory():
    return showInventory

def inc_index():
    global invIndex
    invIndex += 1

def dec_index():
    global invIndex
    invIndex -= 1

def get_idx():
    return invIndex

def draw_inventory(stdscr, inventory):
    global showInventory, invIndex, invStartIdx, lastIndex

    if showInventory:
        if invIndex < invStartIdx:
            if invStartIdx == 0:
                invIndex = 0
            else:
                invStartIdx -= 1
        if invIndex > invStartIdx + 5:
            invStartIdx += 1
        if invIndex > len(inventory) - 1:
            invIndex = len(inventory) - 1
        if invIndex < 0 and len(inventory) > 0:
            invIndex = 0
        draw_box(stdscr, Rect(15, 8, 50, 20))
        draw_label(stdscr, Point(36, 10), 'INVENTORY')
        draw_label(stdscr, Point(34, 11), '─' * 13)
        if invStartIdx > 0:
            draw_label(stdscr, Point(40, 13), '☝')
        for idx, item in enumerate(inventory[invStartIdx:invStartIdx + 6]):
            draw_label(stdscr, Point(18, 14 + idx * 2), ('> ' if idx + invStartIdx == invIndex else '') + item.name)
        if len(inventory) - 1 > invStartIdx + 5:
            draw_label(stdscr, Point(40, 27), '☟')
        if invIndex >= 0 and lastIndex != invIndex:
            log_message(inventory[invIndex].detailedDesc)
        lastIndex = invIndex