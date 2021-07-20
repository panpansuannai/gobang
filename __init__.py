import curses
import sys
import curses.textpad
from chessboard import *
from chessman import *
from window import *

if __name__ == '__main__':
    scr = curses.initscr()
    scr.keypad(True)
    scr.border()

    curses.noecho()

    ''' Select num '''
    rows = 3
    scr.addstr(2, 2, "1 - 10 x 10")
    scr.addstr(5, 2, "2 - 15 x 15(默认)")
    scr.addstr(8, 2, "3 - 20 x 20")
    scr.addstr(11, 2, "请选择棋盘规格: ")
    key = scr.getkey()
    if key == '1':
        rows = 10
    elif key == '2':
        rows = 15
    elif key == '3':
        rows = 20

    max_y, max_x = scr.getmaxyx()
    chessboard = scr.derwin(max_y - 2, max_x // 2, 1, 1)
    chessboard.keypad(True)
    chessboard.clear()
    chessboard.border()
    chesswin = ChessBoardWindow(chessboard, rows, 5)

    scoreboard = scr.derwin(max_y - 2, max_x // 2 - 3, 1, 2 + max_x // 2)
    scoreboard.keypad(True)
    scoreboard.border()
    scorewin = ScoreWindow(scoreboard)

    colors = [{"name":"白棋", "color":ChessColor('#')}, {"name":"黑棋", "color":ChessColor('@')}]
    color_num = 0

    scorewin.change_player(colors[color_num]["name"]
            + " " + colors[color_num]["color"].get_color())
    scorewin.add_msg("使用方向键移动, 使用Enter下棋, ctrl-c 退出")

    ''' Draw window'''
    chesswin.draw_board()
    chesswin.set_current_color(colors[color_num]["color"])
    chesswin.reset_cur()

    while True:
        scorewin.refresh()
        scr.refresh()

        try:
            key = chesswin.get_key()
        except KeyboardInterrupt:
            curses.endwin()
            sys.exit(0)

        finish = False
        ''' short cut '''
        if key == 'j':
            key = 'KEY_DOWN'
        elif key == 'k':
            key = 'KEY_UP'
        elif key == 'l':
            key = 'KEY_RIGHT'
        elif key == 'h':
            key = 'KEY_LEFT'

        if (key == 'KEY_LEFT' 
            or key == 'KEY_RIGHT'
            or key == 'KEY_UP'
            or key == 'KEY_DOWN') :
            chesswin.move(key)
        elif key == '\n':
            try:
                finish = chesswin.add_chessman(colors[color_num]["color"])
            except ValueError:
                chesswin.move('')
                continue
            except ChessBoard.FullException:
                scorewin.add_msg("游戏结束, 棋盘已满")
                scorewin.add_msg("按任意键退出...", curses.A_BLINK)
                scorewin.refresh()
                key = chesswin.get_key()
                curses.endwin()
                sys.exit(0)

            color_num = (color_num + 1) % 2
            scorewin.change_player(colors[color_num]["name"]
                    + " " + colors[color_num]["color"].get_color())
            chesswin.set_current_color(colors[color_num]["color"])
        
        if finish:
            scorewin.add_msg("游戏结束，" + colors[(color_num + 1)%2]["name"] + "胜")
            scorewin.add_msg("按任意键退出...", curses.A_BLINK)
            scorewin.refresh()
            key = chesswin.get_key()
            curses.endwin()
            sys.exit(0)

    curses.endwin()
