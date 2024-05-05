from curses import *
import curses
from os import getcwd, chdir, system, listdir, path
import json
import traceback
from sys import stdout, stderr

PAIR_NORMAL = 0
PAIR_CURSOR = 1
PAIR_SELECTED = 2
PAIR_SELECTED_CURSOR = 3

def init():
    global win, config
    win = initscr()
    # def_shell_mode()
    noecho()
    cbreak()

    config = json.load(open("/home/appo/Dev/EPFE/config.json"))
    start_color()
    use_default_colors()
    # if can_change_color():
    #     init_color(COLOR_BLACK, 0, 0, 0)
    #     init_color(COLOR_WHITE, 255, 255, 255)
    #     init_color(COLOR_BLUE, 0, 0, 255)
    #     init_color(COLOR_MAGENTA, 500, 0, 500)
    #     init_color(COLOR_CYAN, 0, 255, 255)
    init_pair(PAIR_SELECTED, COLOR_WHITE, COLOR_BLUE)
    init_pair(PAIR_SELECTED, COLOR_WHITE, COLOR_MAGENTA)
    init_pair(PAIR_SELECTED_CURSOR, COLOR_BLACK, COLOR_CYAN)


def stop():
    echo()
    nocbreak()
    print()
    quit()

def launch(app):
    ext = app.rsplit(".", 1)[1]
    if ext in config["launch"]:
        stop()
        quit(system(f"{config['launch'][ext]} {app}"))
    else:
        stop()
        quit(system(f"xdg-open {app}"))

ls = []
cursor = 0

SELECTED = []
VISUAL_MODE = False
def selection():
    if VISUAL_MODE:
        return SELECTED
    else:
        if len(ls) > cursor:
            return SELECTED + [ls[cursor]]
        else:
            return SELECTED

def main():
    while True:
        cwd = getcwd()
        ls = listdir()
        cursor = 0
        H,W = win.getmaxyx()
        while True:
            for n,i in enumerate(ls):
                win.move(n, 1)
                win.addstr(i, color_pair((n == cursor)*PAIR_CURSOR + (n in selection())*PAIR_SELECTED))
            win.move(H-1, 1)
            win.addstr(f"{len(selection())} elements selected.")
            win.refresh()
            inp = win.getkey()
            match ord(inp):
                case 10:
                    if VISUAL_MODE:
                        p = str(path.join(cwd, ls[cursor]))
                        if p in SELECTED:
                            SELECTED.remove(p)
                        else:
                            SELECTED.append(p)
                        break
                    if path.isdir(ls[cursor]):
                        chdir(ls[cursor])
                        break
                    for s in selection():
                        launch(str(path.join(cwd, s)))
                case 65:
                    cursor = (cursor-1)%len(ls)
                case 66:
                    cursor = (cursor+1)%len(ls)
                case 68:
                    chdir("..")
                    break
                case 67:
                    chdir(ls[cursor])
                    break
                case 113: # 'q'
                    stop()
                    quit(0)
                case 118: # 'v'
                    VISUAL_MODE = not VISUAL_MODE
                case 99: # 'c'
                    for src in selection():
                        system(f"cp {src} ./")
                    break
                case 109: # 'm'
                    for src in selection():
                        system(f"mv {src} ./")
                    break
    
if __name__ == "__main__":
    # err = None
    # try:
    init()
    main()
    stop()
    # except Exception as e:
    #     stop()
    #     err = e
    # if err is not None:
    #     traceback.print_exception(e, file=stderr)
    #     traceback.print_exc()
    #     traceback.print_exc()
    #     traceback.print_exc()

