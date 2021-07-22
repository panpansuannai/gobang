import curses
import sys
import curses.textpad
from chessboard import *
from chessman import *
from window import *
from alphabeta import *

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
    return key

def menu_select(scr, promt: str, strs:list, options: list, default):
    start_x, start_y = 2, 2
    step_y = 3
    now_select = 0
    while True:
        scr.refresh()
        x, y = start_x, start_y
        for i in range(len(options)):
            if i == now_select:
                scr.addstr(y, x, str(i + 1) + ' - ' + strs[i], curses.A_STANDOUT)
            else:
                scr.addstr(y, x, str(i + 1) + ' - ' + strs[i])
            y += step_y
        scr.addstr(y, x, promt + ": ")
        try:
            key = scr.getkey()

            if shortcuts(key) == 'KEY_UP':
                now_select = max(0, now_select - 1)
                continue
            elif shortcuts(key) == 'KEY_DOWN':
                now_select = min(len(options) - 1, now_select + 1)
                continue
            elif key == '\n':
                scr.clear()
                scr.refresh()
                scr.border()
                return options[now_select]
            else:
                scr.clear()
                scr.refresh()
                scr.border()
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
    scorewin.add_msg("按任意键退出...", curses.A_BLINK)
    scorewin.refresh()
    try:
        _ = chesswin.get_key()
    except:
        pass
    curses.endwin()
    sys.exit(0)

def player_round(chesswin, scorewin, player: dict) -> bool:
    chesswin.set_current_color(player['color'])
    scorewin.change_player(player['name'])
    scorewin.refresh()
    while True:
        try:
            key = chesswin.get_key()
        except KeyboardInterrupt:
            curses.endwin()
            sys.exit(0)

        key = shortcuts(key)
        if (key == 'KEY_LEFT' 
            or key == 'KEY_RIGHT'
            or key == 'KEY_UP'
            or key == 'KEY_DOWN') :
            chesswin.move(key)
        elif key == '\n':
            try:
                return chesswin.add_chessman(player['color'])
            except ValueError:
                chesswin.move('')
                continue


def computer_round(chesswin, scorewin, player: dict, human_color: ChessColor):
    scorewin.change_player(player['name'])
    scorewin.refresh()
    alphabeta = AlphaBeta(chesswin.board, chesswin.num)
    t, x, y = alphabeta.get_best_pos(True, player['color'], human_color, 0)
    #scorewin.add_msg(str(t) + ", " + str(x) + ", " + str(y))
    chesswin.set_cur(x, y)
    try:
        return chesswin.add_chessman(player['color'])
    except ValueError:
        exit(chesswin, scorewin)

if __name__ == '__main__':
    scr = curses.initscr()
    scr.keypad(True)
    scr.border()

    curses.noecho()

    ''' Select num '''
    rows = menu_select(scr, "请选择棋盘规格",
                        ["10 x 10(默认)", "12 x 12",
                        "15 x 15"], [10, 12, 15], 10)

    player_first = menu_select(scr, "请选择先手方",
                      ["玩家(默认)", "电脑"], [True, False], True)

    num = 5
    max_y, max_x = scr.getmaxyx()
    chessboard = scr.derwin(max_y - 2, max_x // 2, 1, 1)
    chessboard.keypad(True)
    chessboard.clear()
    chessboard.border()
    chesswin = ChessBoardWindow(chessboard, rows, num)

    scoreboard = scr.derwin(max_y - 2, max_x // 2 - 3, 1, 2 + max_x // 2)
    scoreboard.keypad(True)
    scoreboard.border()
    scorewin = ScoreWindow(scoreboard)

    players = {"player" : {"name": "玩家", "color": ChessColor('#')},
              "computer": {"name": "电脑", "color": ChessColor('@')}}

    scorewin.add_msg("使用方向键移动, 使用Enter下棋, ctrl-c 退出")

    ''' Draw window'''
    chesswin.draw_board()
    chesswin.reset_cur()

    while True:
        scorewin.refresh()
        scr.refresh()

        try:
            if player_first and player_round(chesswin, scorewin, players['player']):
                scorewin.add_msg("游戏结束，"
                                 + players['player']["name"] + "胜")
                exit(chesswin, scorewin)
            if computer_round(chesswin, scorewin, players['computer'], players['player']['color']):
                scorewin.add_msg("游戏结束，"
                                 + players['computer']["name"] + "胜")
                exit(chesswin, scorewin)

        except ChessBoard.FullException:
            scorewin.add_msg("游戏结束, 棋盘已满")
            exit(chesswin, scorewin)
        player_first = True

    curses.endwin()
