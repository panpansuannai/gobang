from chessboard import *
from chessman import *
import curses

''' Represent a window that contains a chessboard
'''
class ChessBoardWindow(object):
    def __init__(self, window, rows: int, num_to_win: int):
        self.__window = window
        self.rows = rows  # rows is equal to column
        chess_max_y, chess_max_x = self.__window.getmaxyx()
        self.col_step = chess_max_x // (self.rows + 1)
        self.row_step = chess_max_y // (self.rows + 1)
        self.chessboard = ChessBoard(rows, rows)
        self._num_to_win = num_to_win
        #self.null_char = '⋅'
        self.null_char = '.'
        self.cur_color = ChessColor(' ')
        self.draw_board()
        self.reset_cur()
    @property
    def num_to_win(self):
        return self._num_to_win


    ''' Move the cursor to the direction
        @param direction must be 'KEY_UP' or 'KEY_DOWN' or 'KEY_LEFT' or 'KEY_RIGHT'
    '''
    def move_dir(self, direction: str):
        old_y, old_x = self.y, self.x
        if direction == 'KEY_UP' and self.y > self.start_y:
            self.y, self.x = self.y - self.row_step, self.x
        elif direction == 'KEY_DOWN' and self.y < self.start_y + (self.rows - 1)*self.row_step:
            self.y, self.x = self.y + self.row_step, self.x
        elif direction == 'KEY_LEFT' and self.x > self.start_x:
            self.y, self.x = self.y, self.x - self.col_step
        elif direction == 'KEY_RIGHT' and self.x < self.start_x + (self.rows - 1) * self.col_step:
            self.y, self.x = self.y, self.x + self.col_step
        self.draw_point(*self.winaddr2index(old_y, old_x))
        if self.chessboard.get_chessman(*self.winaddr2index(self.y, self.x)) == None:
            self.__window.addch(self.y, self.x,
                        self.cur_color.color(), curses.A_BLINK|curses.A_BOLD)
        else:
            self.__window.addch(self.y, self.x,
                self.chessboard.get_chessman(
                    *self.winaddr2index(self.y, self.x)).get_color().color(),
                    curses.A_BOLD|curses.A_UNDERLINE)
        self.__window.move(self.y, self.x)
        self.__window.refresh()

    def set_cur(self, x: int, y: int):
        self.draw_point(*self.winaddr2index(self.y, self.x))
        self.y, self.x = self.index2windaddr(x, y)
        self.__window.move(self.y, self.x)
        self.move_dir('')


    def draw_point(self, i:int, j:int):
        if self.chessboard.get_chessman(i, j) == None:
            self.__window.addch(*(self.index2windaddr(i, j)), self.null_char)
        else:
            color = self.chessboard.get_chessman(i, j).get_color()
            self.__window.addch(*(self.index2windaddr(i, j)),
                        color.color())
        self.__window.refresh()

    ''' Draw the chessboard to the console '''
    def draw_board(self):

        for j in range(1, self.rows + 1):
            for i in range(1, self.rows + 1):
                self.draw_point(i, j)

    ''' Reset the cursor to the begining '''
    def reset_cur(self):
        self.start_y, self.start_x = self.index2windaddr(1,1) 
        self.__window.move(self.start_y, self.start_x)
        self.y, self.x = self.start_y, self.start_x

    ''' Transform the windows position to 
        chessboard index
    '''
    def winaddr2index(self, y: int, x: int) -> tuple[int, int]:
        return (x // self.col_step , y // self.row_step )

    ''' Transform the chessboard index to 
        the window position
    '''
    def index2windaddr(self, x: int, y: int) -> tuple[int, int]:
        return (self.row_step*y, self.col_step*x)

    ''' Add a chessman at the current cursor,
        if game finished return True
        else return False
    '''
    def add_chessman(self, color: ChessColor) -> bool:
        if self.chessboard.get_chessman(*self.winaddr2index(self.y, self.x)) == None:
            self.chessboard.add_chessman(
                                    *self.winaddr2index(self.y, self.x),
                                    ChessMan(color))
            self.draw_point(*self.winaddr2index(self.y, self.x))
            self.__window.refresh()
            if self.chessboard.check_n_chessman(*self.winaddr2index(self.y, self.x), self.num_to_win):
                return True
            elif self.chessboard.check_full():
                raise ChessBoard.FullException
        else:
            raise ValueError
        return False

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
