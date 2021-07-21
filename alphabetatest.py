import unittest
from chessboard import *
from chessman import *
from alphabeta import *

class AlphaBetaTest(unittest.TestCase):

    def test_cur_branch(self):
        num = 5
        board = ChessBoard(num, num)
        color1 = ChessColor('@')
        color2 = ChessColor('#')
        board.add_chessman(1, 1, ChessMan(color1))
        #board.add_chessman(1, 2, ChessMan(color2))
        #board.add_chessman(1, 3, ChessMan(color1))
        #board.add_chessman(2, 1, ChessMan(color1))
        board.add_chessman(2, 2, ChessMan(color1))
        #board.add_chessman(3, 1, ChessMan(color1))
        #board.add_chessman(3, 2, ChessMan(color1))
        board.add_chessman(3, 3, ChessMan(color1))
        print(AlphaBeta(board, num).get_best_pos(True, color2, color1, 1))

if __name__ == "__main__":
    unittest.main()
