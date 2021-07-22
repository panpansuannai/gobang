from chessboard import *
from chessman import *
import sys
import tabulate

INF = sys.maxsize
NEG_INF = - INF

class AlphaBeta(object):
    def __init__(self, board: ChessBoard, num: int):
        self.board = board
        self.num = num
        self.max_depth = board.rows * board.cols
        self.pos_weight = [[min([i +1, j+1, board.get_cols() - i, board.get_rows() - j]) for i in range(board.get_cols())] for j in range(board.get_rows())]


    def get_best_pos(self, mini: bool, minicolor: ChessColor,
                maxcolor: ChessColor, max_depth: int = 4,
                a: int = NEG_INF, b: int = INF, depth: int = 0):

        board = [['-' for i in range(self.board.cols)] for j in range(self.board.rows)]
        for j in range(1, self.board.get_rows() + 1):
            for i in range(1, self.board.get_cols() + 1):
                if self.board.get_chessman(i, j) == None:
                    self.board.add_chessman(i, j,
                                    ChessMan(minicolor if mini else maxcolor))
                    board[j-1][i-1] = self.cut_branch(i, j, 
                                                      not mini, minicolor,
                                                      maxcolor, max_depth)
                    self.board.remove_chessman(i, j)
                    assert self.board.get_chessman(i, j) == None

        #print(tabulate.tabulate(board))

        if mini:
            v = NEG_INF
        else:
            v = INF
        x, y = 0, 0
        for j in range(1, self.board.get_rows() + 1):
            for i in range(1, self.board.get_cols() + 1):
                if self.board.get_chessman(i, j) == None:
                    if mini:
                        if board[j-1][i-1] > v:
                            v = board[j-1][i-1]
                            x, y = i, j
                    else:
                        if board[j-1][i-1] < v:
                            v = board[j-1][i-1]
                            x, y = i, j
        return (v, x, y)

    def cut_branch(self, x:int, y:int, mini: bool, minicolor: ChessColor,
                maxcolor: ChessColor, max_depth:int = 4, 
                a:int = NEG_INF, b:int = INF, depth:int = 0):

        if depth >= max_depth:
            #print("x: {}, y:{}, {}".format(x, y, minicolor.color() if mini else maxcolor.color()))
            scores = self.calc_board_scores(x, y, mini, minicolor, maxcolor)
            #print("scores: {}".format(scores))
            return scores 

        if mini:
            v = INF
            for j in range(1, self.board.get_rows() + 1):
                for i in range(1, self.board.get_cols() + 1):
                    if self.board.get_chessman(i, j) == None:

                        self.board.add_chessman(i, j, ChessMan(minicolor))
                        if self.board.check_n_chessman(i, j, self.num):
                            self.board.remove_chessman(i, j)
                            return self.calc_board_scores(i, j,
                                    mini, minicolor, maxcolor)
                        if self.board.check_full():
                            self.board.remove_chessman(i, j)
                            return self.calc_board_scores(i, j,
                                    mini, minicolor, maxcolor)

                        _t = self.cut_branch(i, j, False, 
                                            minicolor, maxcolor,max_depth, 
                                            a, b, depth + 1)

                        self.board.remove_chessman(i, j)
                        v = min(v, _t)
                        b = min(b, v)
                        if b <= a:
                            break
                        assert self.board.get_chessman(i, j) == None
            return v
        else:
            v = NEG_INF
            for j in range(1, self.board.get_rows() + 1):
                for i in range(1, self.board.get_cols() + 1):
                    if self.board.get_chessman(i, j) == None:

                        self.board.add_chessman(i, j, ChessMan(maxcolor))
                        if self.board.check_n_chessman(i, j, self.num):
                            self.board.remove_chessman(i, j)
                            return self.calc_board_scores(i, j,
                                    mini, minicolor, maxcolor)

                        if self.board.check_full():
                            self.board.remove_chessman(i, j)
                            return self.calc_board_scores(i, j,
                                    mini, minicolor, maxcolor)

                        _t = self.cut_branch(i, j, True, 
                                            minicolor, maxcolor,max_depth,
                                            a, b, depth + 1)

                        self.board.remove_chessman(i, j)
                        v = max(v, _t)
                        a = max(a, v)
                        if b <= a:
                            break
                        assert self.board.get_chessman(i, j) == None
            return v
        
    def calc_board_scores(self, x: int, y: int, mini: bool,
                            minicolor: ChessColor,
                            maxcolor: ChessColor) -> int:
        up = lambda x, y: (x, y - 1)
        down = lambda x, y: (x, y + 1)
        left = lambda x, y: (x - 1, y)
        right = lambda x, y: (x + 1, y)
        upper_left = lambda x, y: left(*up(x, y))
        lower_left = lambda x, y: left(*down(x,y))
        upper_right = lambda x, y: right(*up(x, y))
        lower_right = lambda x, y: right(*down(x, y))
        color = minicolor if mini else maxcolor
        chessman = self.board.get_chessman(x, y)

        scores = 0
        for i in [(*self.board.get_corner(x, y, up), 
                    *self.board.get_corner(x, y, down),
                    down),
                   (*self.board.get_corner(x, y, upper_left),
                   *self.board.get_corner(x, y, lower_right),
                   lower_right),
                   (*self.board.get_corner(x, y, left),
                   *self.board.get_corner(x, y, right), right),

                   (*self.board.get_corner(x, y, lower_left),
                    *self.board.get_corner(x, y, upper_right),
                    upper_right)]:
            start_x, start_y, end_x, end_y, direction = i
            start_x, start_y = direction(start_x, start_y)
            #print("(" + str(start_x) + ", " + str(start_y) + ") -> (" + str(end_x) + ", " + str(end_y) + ")")
            s = '|'
            while start_x != end_x or start_y != end_y:
                if self.board.get_chessman(start_x, start_y) == chessman:
                    s += '*'
                elif self.board.get_chessman(start_x, start_y) == None:
                    s += '_'
                elif (self.board.get_chessman(start_x, start_y)
                        .get_color() == color):
                    s += '#'
                else:
                    s += '@'
                start_x, start_y = direction(start_x, start_y)
            s += '|'
            #print(s)
            scores += self.__calc_scores(s) + self.pos_weight[y-1][x-1]
        return -scores if mini else scores

    def __calc_scores(self, s: str) -> int:
        ''' # : me, @: it , *: now'''
        scores = 0
        if (s.find('*####') != -1
           or s.find('#*###') != -1
           or s.find('##*##') != -1
           or s.find('###*#') != -1
           or s.find('####*') != -1):
            scores += 10000000

        elif (s.find('*@@@@') != -1
            or s.find('@*@@@') != -1
            or s.find('@@*@@') != -1
            or s.find('@@@*@') != -1
            or s.find('@@@@*') != -1):
            scores += 6000000

        elif (s.find('_*###_') != -1
            or s.find('_#*##_') != -1
            or s.find('_##*#_') != -1
            or s.find('_###*_') != -1):
            scores += 5000000

        elif ( s.find('*_###') != -1
            or s.find('*#_##') != -1
            or s.find('*##_#') != -1
            or s.find('*###_') != -1
            or s.find('_*###') != -1
            or s.find('#*_##') != -1
            or s.find('#*#_#') != -1
            or s.find('#*##_') != -1
            or s.find('_#*##') != -1
            or s.find('#_*##') != -1
            or s.find('##*_#') != -1
            or s.find('##*#_') != -1
            or s.find('_##*#') != -1
            or s.find('#_#*#') != -1
            or s.find('##_*#') != -1
            or s.find('###*_') != -1
            or s.find('_###*') != -1
            or s.find('#_##*') != -1
            or s.find('##_#*') != -1
            or s.find('###_*') != -1):
            scores += 500000

        elif (s.find('*@@@_') != -1
            or s.find('_*@@@') != -1
            or s.find('@*@@_') != -1
            or s.find('_@*@@') != -1
            or s.find('@@*@_') != -1
            or s.find('_@@*@') != -1
            or s.find('@@@*_') != -1
            or s.find('_@@@*') != -1):
            scores += 100000


        elif (s.find('*##__') != -1
            or s.find('#*#__') != -1
            or s.find('##*__') != -1
            or s.find('_*##_') != -1
            or s.find('_#*#_') != -1
            or s.find('_##*_') != -1
            or s.find('__*##') != -1
            or s.find('__#*#') != -1
            or s.find('__##*') != -1):
            scores += 50000

        elif (s.find('*@@_') != -1
            or s.find('_*@@') != -1
            or s.find('_@*@') != -1
            or s.find('@*@_') != -1
            or s.find('_@@*') != -1
            or s.find('@@*_') != -1):
            scores += 1000

        elif (s.find('*#___') != -1
            or s.find('#*___') != -1
            or s.find('_*#__') != -1
            or s.find('_#*__') != -1
            or s.find('__*#_') != -1
            or s.find('__#*_') != -1
            or s.find('___*#') != -1
            or s.find('___#*') != -1):
            scores += 500

        elif (s.find('*_#__') != -1
            or s.find('#_*__') != -1
            or s.find('_*_#_') != -1
            or s.find('_#_*_') != -1
            or s.find('__*_#') != -1
            or s.find('__#_*') != -1):
            scores += 100

        elif (s.find('*__#_') != -1
            or s.find('*__#_') != -1
            or s.find('_*__#') != -1
            or s.find('_#__*') != -1):
            scores += 50

        elif (s.find('*@_') != -1
            or s.find('_*@') != -1
            or s.find('_@*') != -1
            or s.find('@*_') != -1):
            scores += 5

        return scores

    """
    def __calc_scores(self, s: str) -> int:
        scores = 0
        if (s.find('*##') != -1
            or s.find('#*#') != -1
            or s.find('##*') != -1):
            scores += 100000
        if (s.find('*#') != -1
            or s.find('#*') != -1):
            scores += 5000
        if (s.find('*_#') != -1
            or s.find('#_*') != -1):
            scores += 3000

        if (s.find('*@') != -1
                or s.find('@*') != -1):
            scores += 500

        if (s.find('*@@') != -1
            or s.find('@*@') != -1
            or s.find('@@*') != -1):
            scores += 50000
        return scores
        """
