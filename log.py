import curses
import textwrap

logs: list[str] = []

def log_message(msg: str):
    global logs
    logs.insert(0, msg)
    logs = logs[0:5]

def draw_messages(stdscr):
    for i, log in enumerate(logs):
        log = textwrap.shorten(log, width=78, placeholder='...')
        stdscr.addstr(35 - i, 2, log)