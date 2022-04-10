logs: list[str] = []

def log_message(msg: str):
    global logs
    logs.insert(0, msg[:76])
    if len(msg) > 76:
        log_message(msg[76:])
    logs = logs[0:5]

def draw_messages(stdscr):
    for i, log in enumerate(logs):
        stdscr.addstr(35 - i, 2, log)