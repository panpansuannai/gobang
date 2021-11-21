from typing import Optional
from chessman import ChessMan

""" 1-index chess board """
class ChessBoard(object):
    class FullException(Exception):
        def __init__(self):
            pass

    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.board = [[None for _ in range(cols)] for _ in range(rows)]

    ''' Add a chessman at the position (x, y) '''
    def add_chessman(self, x: int, y: int, chessman: ChessMan) -> bool:
        if 1 <= x <= self.cols and 1 <= y <= self.rows:
            self.board[y - 1][x - 1] = chessman
            return True
        return False

    ''' Get the chessman at the position (x, y) '''
    def get_chessman(self, x: int, y: int) -> object:
        if 1 <= x <= self.cols and 1 <= y <= self.rows:
            return self.board[y-1][x-1]
        return None

    def remove_chessman(self, x: int, y: int):
        if 1 <= x <= self.cols and 1 <= y <= self.rows:
            self.board[y-1][x-1] = None

    ''' Check how many chessmans are in the same color
        in the direction 
    '''
    def get_dir(self, x: int, y: int, dir) -> set[tuple[int, int]]: 
        if not (1 <= x <= self.cols and 1 <= y <= self.rows):
            return set()
        if self.board[y - 1][x - 1] == None:
            return set()
        color = self.board[y-1][x-1].get_color()
        ret = set() 
        xp, yp = x, y
        while (1 <= xp <= self.cols and 1 <= yp <= self.rows 
                and self.board[yp-1][xp-1] != None
                and self.board[yp - 1][xp - 1].get_color() == color):
            ret.add((xp, yp))
            xp, yp = dir(xp, yp)
        return ret

    def get_corner(self, x: int, y: int, dir) -> tuple[int, int]:
        while 1 <= x <= self.cols and 1 <= y <= self.rows:
            x, y = dir(x, y)
        return (x, y)

    ''' Check the position (x, y) whether are in the line 
        that contians n chessman with the same color
    '''
    def check_n_chessman(self, x: int, y: int, n: int) -> bool:
        if not (1 <= x <= self.cols and 1 <= y <= self.rows):
            return False
        if self.board[y - 1][x - 1] == None:
            return False
        up = lambda x, y: (x, y - 1)
        down = lambda x, y: (x, y + 1)
        left = lambda x, y: (x - 1, y)
        right = lambda x, y: (x + 1, y)
        upper_left = lambda x, y: left(*up(x, y))
        lower_left = lambda x, y: left(*down(x,y))
        upper_right = lambda x, y: right(*up(x, y))
        lower_right = lambda x, y: right(*down(x,y))
        if (len(self.get_dir(x, y, upper_left)) + len(self.get_dir(x, y, lower_right)) >= n + 1
            or len(self.get_dir(x, y, upper_right)) 
                + len(self.get_dir(x, y, lower_left)) >= n + 1
            or len(self.get_dir(x, y, up))
                + len(self.get_dir(x, y, down)) >= n + 1
            or len(self.get_dir(x, y, left)) 
                + len(self.get_dir(x, y, right)) >= n + 1):
            return True
        return False

    def get_continue(self, x: int, y: int, n: int) -> set:
        if not (1 <= x <= self.cols and 1 <= y <= self.rows):
            return set()
        if self.board[y - 1][x - 1] == None:
            return set()
        up = lambda x, y: (x, y - 1)
        down = lambda x, y: (x, y + 1)
        left = lambda x, y: (x - 1, y)
        right = lambda x, y: (x + 1, y)
        upper_left = lambda x, y: left(*up(x, y))
        lower_left = lambda x, y: left(*down(x,y))
        upper_right = lambda x, y: right(*up(x, y))
        lower_right = lambda x, y: right(*down(x,y))
        if (len(self.get_dir(x, y, upper_left)
            .union(self.get_dir(x, y, lower_right))) >= n):
            return self.get_dir(x, y, upper_left).union(self.get_dir(x, y, lower_right))
        if (len(self.get_dir(x, y, upper_right)
            .union(self.get_dir(x, y, lower_left))) >= n):
            return self.get_dir(x, y, upper_right).union(self.get_dir(x, y, lower_left))
        if (len(self.get_dir(x, y, up)
            .union(self.get_dir(x, y, down))) >= n):
            return self.get_dir(x, y, up).union(self.get_dir(x, y, down))

        if (len(self.get_dir(x, y, left)
            .union(self.get_dir(x, y, right))) >= n):
            return self.get_dir(x, y, left).union(self.get_dir(x, y, right))
        return set()

    ''' Check whether the board is full '''
    def check_full(self) -> bool:
        for i in self.board:
            for j in i:
                if j == None:
                    return False
        return True
    
    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def __str__(self):
        s = ''
        for i in self.board:
            for j in i:
                if j != None:
                    s += j.get_color().color() + ' '
                else:
                    s += '! '
            s += '\n'
        return s

