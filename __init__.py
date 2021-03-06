import curses
import sys
import curses.textpad
from chessboard import *
from chessman import *
from window import *
from alphabeta import *

def startup(scr):
    curses.curs_set(0)
    y, x = scr.getmaxyx()
    scr.addstr((y-8)//2, (x-42)//2, r"__        __   _          ")
    scr.addstr((y-8)//2+1, (x-42)//2, r"\ \      / /__| | ___ ___  _ __ ___   ___ ")
    scr.addstr((y-8)//2+2, (x-42)//2, r" \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ ")
    scr.addstr((y - 8) // 2 + 3, (x - 42) // 2, r"  \ V  V /  __/ | (_| (_) | | | | | |  __/")
    scr.addstr((y - 8) // 2 + 4, (x - 42) // 2, r"   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|")
    scr.addstr((y-8) // 2+6, (x - 9) //2, "<<五子棋>>",
                curses.A_STANDOUT|curses.A_ITALIC)
    scr.addstr((y-8)//2 + 8, (x - 22) // 2, "press <Enter> to start", curses.A_BLINK)
    scr.refresh()
    while True:
        try:
            if scr.getkey() == '\n':
                break
        except:
            curses.endwin()
            sys.exit(0)

def split_window(scr) -> tuple[ChessBoardWindow, ScoreWindow]:
    scrmaxy, scrmaxx = scr.getmaxyx()
    chessmaxy, chessmaxx = rows * 2 + 2, rows * 4 + 4
    winmarginx = (scrmaxx - 2 * chessmaxx) // 3
    winmarginy = (scrmaxy -  chessmaxy) // 2 
    try:
        chessboard = scr.derwin(chessmaxy, chessmaxx, 1 + winmarginy, 1 + winmarginx)
    except:
        import os
        curses.endwin()
        print("当前终端columns = ", scrmaxx, ", rows = ", scrmaxy)
        print("窗口加载失败，请尝试全屏运行")
        os._exit(0)
    chessboard.keypad(True)
    chessboard.clear()
    chessboard.border()
    chesswin = ChessBoardWindow(chessboard, rows, num)

    chessbegy, chessbegx = chessboard.getbegyx()
    scoreboard = scr.derwin(chessmaxy, chessmaxx, chessbegy, chessbegx + chessmaxx + winmarginx)
    scoreboard.keypad(True)
    scoreboard.border()
    scorewin = ScoreWindow(scoreboard)
    return (chesswin, scorewin)

def shortcuts(key: str) -> str:
    ''' short cut '''
    if key == 'j':
        key = 'KEY_DOWN'
    elif key == 'k':
        key = 'KEY_UP'
    elif key == 'l':
        key = 'KEY_RIGHT'
    elif key == 'h':
        key = 'KEY_LEFT'
    elif key == ' ':
        key = '\n'
    return key

def menu_select(scr, promt: str, strs:list, options: list, default):
    scr.clear()
    scr.refresh()
    scr.border()
    curses.curs_set(0)
    start_x, start_y = 2, 2
    step_y = 3
    x_tab = 3
    now_select = 0
    while True:
        scr.refresh()
        x, y = start_x, start_y
        scr.addstr(y, x, promt + "(<方向键>选择)", curses.A_ITALIC|curses.A_BOLD|curses.A_HORIZONTAL)
        x += x_tab
        for i in range(len(options)):
            y += step_y
            if i == now_select:
                scr.addstr(y, x, strs[i], curses.A_STANDOUT|curses.A_BOLD)
            else:
                scr.addstr(y, x, strs[i])
        try:
            key = scr.getkey()

            if shortcuts(key) == 'KEY_UP':
                now_select = max(0, now_select - 1)
                continue
            elif shortcuts(key) == 'KEY_DOWN':
                now_select = min(len(options) - 1, now_select + 1)
                continue
            elif key == '\n':
                return options[now_select]
            else:
                try:
                    key = int(key)
                except:
                    return default
                if 1 <= key <= len(options):
                    return options[key - 1]
                return default
        except KeyboardInterrupt:
            curses.endwin()
            sys.exit(0)

def exit(chesswin, scorewin):
    scorewin.add_msg("按<Enter>退出...", curses.A_BLINK)
    scorewin.refresh()
    while True:
        try:
            if chesswin.get_key() == '\n':
                break
        except:
            break
    curses.endwin()
    sys.exit(0)

def player_round(chesswin, scorewin, player: dict, competer: ChessColor) -> bool:
    chesswin.set_current_color(player['color'])
    scorewin.change_player(player['name'])
    scorewin.refresh()
    while True:
        try:
            key = chesswin.get_key()
        except KeyboardInterrupt:
            curses.endwin()
            exit(chesswin, scorewin)

        key = shortcuts(key)
        if (key == 'KEY_LEFT' 
            or key == 'KEY_RIGHT'
            or key == 'KEY_UP'
            or key == 'KEY_DOWN') :
            chesswin.move_dir(key)
        elif key == '\n':
            try:
                if chesswin.add_chessman(player['color']):
                    chesswin.set_board_blink(chesswin.chessboard.get_continue(
                                            *chesswin.winaddr2index(chesswin.y,
                                            chesswin.x), chesswin.num_to_win))
                    return True
                else:
                    return False
            except ValueError:
                continue
        elif key == 'a':
            alphabeta = AlphaBeta(chesswin.chessboard, chesswin.num_to_win)
            _, x, y = alphabeta.get_best_pos(True, player['color'], competer, 0)
            chesswin.set_cur(x, y)
        elif key == 'A':
            return computer_round(chesswin, scorewin, player, competer)


def computer_round(chesswin, scorewin, player: dict, competer: ChessColor):
    scorewin.change_player(player['name'])
    scorewin.refresh()
    alphabeta = AlphaBeta(chesswin.chessboard, chesswin.num_to_win)
    _, x, y = alphabeta.get_best_pos(True, player['color'], competer, 0)
    #scorewin.add_msg(str(t) + ", " + str(x) + ", " + str(y))
    chesswin.set_cur(x, y)
    try:
        if chesswin.add_chessman(player['color']):
            chesswin.set_board_blink(chesswin.chessboard.get_continue(x, y, chesswin.num_to_win))
            return True
        else:
            return False
    except ValueError:
        exit(chesswin, scorewin)

if __name__ == '__main__':
    scr = curses.initscr()
    scrmaxy, scrmaxx = scr.getmaxyx()
    scr.keypad(True)
    scr.border()

    curses.noecho()

    startup(scr)

    ''' Options '''

    # 其他棋盘规格没有做调整，不太美观
    # 只使用15 X 15的棋盘
    '''
    rows = menu_select(scr, "请选择棋盘规格",
                        ["10 x 10", "15 x 15",
                        "18 x 18"], [10, 15, 18], 10)
    '''
    rows = 15                  

    player_first = menu_select(scr, "请选择先手方",
                      ["玩家", "电脑"], [True, False], True)
    
    chessman_style = [["@", "#"], ["^", "*"], ["○", "●"], ["×", "Ø"]]
    chessman_style = menu_select(scr, "请选择棋子样式",
            list(map(lambda x: x[0] + ' - ' + x[1], chessman_style)),
            chessman_style, chessman_style[0])
    scr.clear()
    scr.border()

    num = 5
    chesswin, scorewin = split_window(scr)

    players = {"player" : {"name": "玩家", "color": ChessColor(chessman_style[0])},
              "computer": {"name": "电脑", "color": ChessColor(chessman_style[1])}}

    scorewin.add_msg("<Up, Down, Left, Right>: 移动", curses.A_ITALIC)
    scorewin.add_msg("<Enter>: 落子", curses.A_ITALIC)
    scorewin.add_msg("<a>: 提示", curses.A_ITALIC)
    scorewin.add_msg("<ctrl-c>: 退出", curses.A_ITALIC)

    # set cursor not visible
    curses.curs_set(0)

    while True:
        scorewin.refresh()
        scr.refresh()

        try:
            if player_first and player_round(chesswin, scorewin,
                            players['player'], players['computer']['color']):
                scorewin.add_msg("游戏结束,"
                                 + players['player']["name"] + "胜")
                exit(chesswin, scorewin)
            if computer_round(chesswin, scorewin, players['computer'], players['player']['color']):
                scorewin.add_msg("游戏结束,"
                                 + players['computer']["name"] + "胜")
                exit(chesswin, scorewin)

        except ChessBoard.FullException:
            scorewin.add_msg("游戏结束, 棋盘已满")
            exit(chesswin, scorewin)
        player_first = True

    curses.endwin()
