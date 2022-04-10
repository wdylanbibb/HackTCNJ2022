import re


logs: list[str] = []

def log_message(msg: str):
    global logs
    words = re.split(r"\s+", msg)
    msg = ''
    for word in words:
        if len(word) + 1 + len(msg) < 76:
            msg += word + ' '
        else:
            logs.insert(0, msg)
            msg = word + ' '
    logs.insert(0, msg)
    logs = logs[0:5]

def draw_messages(stdscr):
    for i, log in enumerate(logs):
        stdscr.addstr(35 - i, 2, log)