from chessman import ChessMan

""" 1-index chess board """
class ChessBoard(object):
    class FullException(Exception):
        def __init__(self):
            pass

    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.board = [[None for i in range(cols)] for j in range(rows)]

    ''' Add a chessman at the position (x, y) '''
    def add_chessman(self, x: int, y: int, chessman: ChessMan) -> bool:
        if 1 <= x <= self.cols and 1 <= y <= self.rows:
            self.board[y - 1][x - 1] = chessman
            return True
        return False

    ''' Get the chessman at the position (x, y) '''
    def get_chessman(self, x: int, y: int):
        if 1 <= x <= self.cols and 1 <= y <= self.rows:
            return self.board[y-1][x-1]
        return None

    def remove_chessman(self, x: int, y: int):
        if 1 <= x <= self.cols and 1 <= y <= self.rows:
            self.board[y-1][x-1] = None

    ''' Check how many chessmans are in the same color
        in the direction 
    '''
    def check_dir(self, x: int, y: int, dir) -> int:
        if not (1 <= x <= self.cols and 1 <= y <= self.rows):
            return 0
        if self.board[y - 1][x - 1] == None:
            return 0
        color = self.board[y-1][x-1].get_color()
        cur_n = 0
        xp, yp = x, y
        while (1 <= xp <= self.cols and 1 <= yp <= self.rows 
                and self.board[yp-1][xp-1] != None
                and self.board[yp-1][xp-1].get_color() == color):
            cur_n += 1
            xp, yp = dir(xp, yp)
        return cur_n

    def get_corner(self, x: int, y: int, dir) -> (int, int):
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
        if (self.check_dir(x, y, upper_left) + self.check_dir(x, y, lower_right)
                                >= n + 1
            or self.check_dir(x, y, upper_right) + self.check_dir(x, y, lower_left)
                                >= n + 1
            or self.check_dir(x, y, up) + self.check_dir(x, y, down)
                                >= n + 1
            or self.check_dir(x, y, left) + self.check_dir(x, y, right)
                                >= n + 1 ):
            return True
        return False

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

