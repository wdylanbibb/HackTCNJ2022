import re
from log import log_message
from audio import play_sound
from utils import Point, Rect
from PIL import Image, ImageOps
import curses

indexedImgs = {}

def draw_img(stdscr, imgName, x, y, width, height, *, bw = False):
    numColors = 8
    if imgName not in indexedImgs:
        try:
            img = Image.open(imgName)
        except Exception as e:
            print(e)
            return
        if not curses.has_colors() or not curses.can_change_color():
            return
        if bw:
            img = img.convert('L').convert('RGB')
        img = ImageOps.pad(ImageOps.contain(img, (width, height * 2)), (width, height * 2), color=(0, 0, 0), centering=(0.5, 0.5)).quantize(min(240, numColors))
    else:
        img = indexedImgs[imgName]
    palette = []
    pal = img.getpalette()
    zero = False
    for i in range(len(pal) // 3):
        if pal[i * 3] == 0 and pal[i * 3 + 1] == 0 and pal[i * 3 + 2] == 0:
            if not zero and i < 240:
                zero = True
            else: continue
        palette.append((pal[i * 3], pal[i * 3 + 1], pal[i * 3 + 2]))
    for i, color in enumerate(palette):
        curses.init_color(i + 16, color[0] * 1000 // 255, color[1] * 1000 // 255, color[2] * 1000 // 255)
    for i, _ in enumerate(palette):
        for j, _ in enumerate(palette):
            curses.init_pair(i + j * numColors + 16, i + 16, j + 16)
    stdscr.refresh()
    for i in range(width):
        for j in range(height):
            topColor = img.getpixel((i, j * 2))
            botColor = img.getpixel((i, j * 2 + 1))
            if palette[topColor] == (0, 0, 0) and palette[botColor] == (0, 0, 0):
                continue
            stdscr.addstr(j + y, i + x, '▀', curses.color_pair(topColor + botColor * numColors + 16))
    stdscr.refresh()
    indexedImgs[imgName] = img

def draw_box(stdscr, rect: Rect):
    stdscr.addstr(rect.y, rect.x, "┌" + ("─" * (rect.width - 2)) + "┐")
    for y in range(1, rect.height):
        stdscr.addstr(rect.y + y, rect.x, "│" + (" " * (rect.width - 2)) + "│")
    stdscr.addstr(rect.y + rect.height, rect.x, "└" + ("─" * (rect.width - 2)) + "┘")

def draw_label(stdscr, pos: Point, msg: str, color_pair = 0):
    _, width = stdscr.getmaxyx()

    if color_pair == 0:
        stdscr.addstr(pos.y, max(pos.x, 0), msg[abs(min(pos.x, 0)):width])
    else:
        stdscr.addstr(pos.y, max(pos.x, 0), msg[abs(min(pos.x, 0)):width], color_pair)

def draw_label_centered(stdscr, y: int, msg: str, color_pair = 0):
    _, width = stdscr.getmaxyx()
    draw_label(stdscr, Point((width // 2) - (len(msg) // 2), y), msg, color_pair)

showInventory = False
invIndex = 0
invStartIdx = 0
lastIndex = -1

showLegend = False
legIndex = 0
legStartIdx = 0
lastLegIdx = -1

def toggle_inventory() -> bool:
    global showInventory, showLegend, invIndex, invStartIdx, lastIndex
    showInventory = not showInventory
    showLegend = False
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

def toggle_legend() -> bool:
    global showInventory, showLegend, legIndex, legStartIdx
    showLegend = not showLegend
    showInventory = False
    legIndex = 0
    legStartIdx = 0
    lastLegIdx = -1

def is_show_legend():
    return showLegend

def inc_legend_index():
    global legIndex
    legIndex += 1

def dec_legend_index():
    global legIndex
    legIndex -= 1

def get_legend_idx():
    return legIndex

def draw_inventory(stdscr, inventory, equipped):
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
        offset = 0
        for idx, item in enumerate(inventory[invStartIdx:invStartIdx + 6]):
            firstLine = True
            if item == equipped:
                draw_label(stdscr, Point(16, 14 + (idx + offset) * 2), '*')
            words = re.split(r"\s+", item.get_name())
            msg = ''
            for word in words:
                if len(word) + 1 + len(msg) < 30:
                    msg += word + ' '
                else:
                    draw_label(stdscr, Point(18, 14 + (idx + offset) * 2), ('> ' if idx + invStartIdx == invIndex and firstLine else '') + msg)
                    offset += 1
                    msg = word + ' '
                    firstLine = False
            draw_label(stdscr, Point(18, 14 + (idx + offset) * 2), ('> ' if idx + invStartIdx == invIndex and firstLine else '') + msg)
        if len(inventory) - 1 > invStartIdx + 5:
            draw_label(stdscr, Point(40, 27), '☟')
        if invIndex >= 0 and lastIndex != invIndex:
            log_message(inventory[invIndex].detailedDesc)
            if lastIndex != -1:
                play_sound('select')
        lastIndex = invIndex

def draw_legend(stdscr, legend):
    global showLegend, legIndex, legStartIdx, lastLegIdx

    if showLegend:
        if legIndex < legStartIdx:
            if legStartIdx == 0:
                legIndex = 0
            else:
                legStartIdx -= 1
        if legIndex > legStartIdx + 5:
            legStartIdx += 1
        if legIndex > len(legend) - 1:
            legIndex = len(legend) - 1
        if legIndex < 0 and len(legend) > 0:
            legIndex = 0
        draw_box(stdscr, Rect(15, 8, 50, 20))
        draw_label(stdscr, Point(36, 10), 'LEGEND')
        draw_label(stdscr, Point(34, 11), '─' * 10)
        if legStartIdx > 0:
            draw_label(stdscr, Point(40, 13), '☝')
        offset = 0
        for idx, item in enumerate(legend[legStartIdx:legStartIdx + 6]):
            firstLine = True
            words = re.split(r"\s+", item['key'] + ' - ' + item['value'])
            msg = ''
            for word in words:

                if len(word) + 1 + len(msg) < 30:
                    msg += word + ' '
                else:
                    draw_label(stdscr, Point(18, 14 + (idx + offset) * 2), ('> ' if idx + legStartIdx == legIndex and firstLine else '') + msg)
                    offset += 1
                    msg = word + ' '
                    firstLine = False
            draw_label(stdscr, Point(18, 14 + (idx + offset) * 2), ('> ' if idx + legStartIdx == legIndex and firstLine else '') + msg)
        if len(legend) - 1 > legStartIdx + 5:
            draw_label(stdscr, Point(40, 27), '☟')
        if legIndex >= 0 and lastLegIdx != legIndex and lastLegIdx != -1:
            play_sound('select')
        lastLegIdx = legIndex