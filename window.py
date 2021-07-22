from chessboard import *
from chessman import *
import curses

''' Represent a window that contains a chessboard
'''
class ChessBoardWindow(object):
    def __init__(self, window, rows: int, num: int):
        self.__window = window
        self.board = ChessBoard(rows, rows)
        self.rows = rows
        self.num = num
        self.null_char = '⋅'
        self.cur_color = ChessColor(' ')

    ''' Move the cursor to the direction
        @param direction must be 'KEY_UP' or 'KEY_DOWN' or 'KEY_LEFT' or 'KEY_RIGHT'
    '''
    def move(self, direction: str):
        if direction == 'KEY_UP' and self.y > self.start_y:
            self.y, self.x = self.y - self.row_step, self.x
        elif direction == 'KEY_DOWN' and self.y < self.start_y + (self.rows - 1)*self.row_step:
            self.y, self.x = self.y + self.row_step, self.x
        elif direction == 'KEY_LEFT' and self.x > self.start_x:
            self.y, self.x = self.y, self.x - self.col_step
        elif direction == 'KEY_RIGHT' and self.x < self.start_x + (self.rows - 1) * self.col_step:
            self.y, self.x = self.y, self.x + self.col_step
        self.draw_board()
        if self.board.get_chessman(*self.winaddr2index(self.y, self.x)) == None:
            self.__window.addch(self.y, self.x,
                        self.cur_color.color(), curses.A_BLINK|curses.A_BOLD)
        else:
            self.__window.addch(self.y, self.x,
                self.board.get_chessman(
                    *self.winaddr2index(self.y, self.x)).get_color().color(),
                    curses.A_BOLD|curses.A_UNDERLINE)
        self.__window.move(self.y, self.x)

    def set_cur(self, x: int, y: int):
        self.y, self.x = self.index2windaddr(x, y)
        self.__window.move(self.y, self.x)
        self.move('')

    ''' Draw the chessboard to the console '''
    def draw_board(self):
        chess_max_y, chess_max_x = self.__window.getmaxyx()

        self.col_step = chess_max_x // (self.rows + 1)
        self.row_step = chess_max_y // (self.rows + 1)

        for j in range(1, self.rows + 1):
            for i in range(1, self.rows + 1):
                if self.board.get_chessman(i, j) == None:
                    self.__window.addch(*(self.index2windaddr(i, j)), self.null_char)
                else:
                    color = self.board.get_chessman(i, j).get_color()
                    self.__window.addch(*(self.index2windaddr(i, j)),
                                        color.color())

    ''' Reset the cursor to the begining '''
    def reset_cur(self):
        self.start_y, self.start_x = self.index2windaddr(1,1) 
        self.__window.move(self.start_y, self.start_x)
        self.y, self.x = self.start_y, self.start_x
        self.move('')

    ''' Transform the windows position to 
        chessboard index
    '''
    def winaddr2index(self, y: int, x: int) -> (int, int):
        return (x // self.col_step , y // self.row_step )

    ''' Transform the chessboard index to 
        the window position
    '''
    def index2windaddr(self, x: int, y: int) -> (int, int):
        return (self.row_step*y, self.col_step*x)

    ''' Add a chessman at the current cursor,
        if game finish return True
        else return False
    '''
    def add_chessman(self, color: ChessColor) -> bool:
        if self.board.get_chessman(*self.winaddr2index(self.y, self.x)) == None:
            self.board.add_chessman(
                                    *self.winaddr2index(self.y, self.x),
                                    ChessMan(color))
            self.draw_board()
            self.__window.refresh()
            self.move('')
            if self.board.check_n_chessman(*self.winaddr2index(self.y, self.x), self.num):
                return True
            elif self.board.check_full():
                raise ChessBoard.FullException
        else:
            raise ValueError

    ''' Set the current cursor to the target color '''
    def set_current_color(self, color: ChessColor):
        self.cur_color = color

    ''' Get a key from window '''
    def get_key(self) -> str:
        return self.__window.getkey()

    def set_board_blink(self, pos: set):
        for x, y in pos:
            self.__window.chgat(*self.index2windaddr(x, y), 1, curses.A_BLINK)
        self.__window.refresh()

''' Represent a window containing some message '''
class ScoreWindow(object):

    init_msg_pos = (1,3)

    def __init__(self, window):
        self.__window = window
        self.player_pos = (1, 1)
        self.last_msg = self.init_msg_pos
        self.player = ''
        self.message = ''
        self.__window.scrollok(True)

    ''' Change the current player name '''
    def change_player(self, player: str):
        self.player = player

    ''' Add a message to the window '''
    def add_msg(self, msg: str, attr=0):
        y, x = self.last_msg
        my, _ = self.__window.getmaxyx()
        if y + 2 >= my:
            self.__window.clear()
            self.__window.border()
            self.__window.refresh()
            self.last_msg = self.init_msg_pos
            y, x = self.last_msg
        y += 2
        self.last_msg = (y, x)
        self.__window.addstr(y, x, msg, attr)

    ''' Refresh the window '''
    def refresh(self):
        self.__window.addstr(*self.player_pos, "当前棋方: " 
                            + self.player, curses.A_STANDOUT)
        self.__window.refresh()
