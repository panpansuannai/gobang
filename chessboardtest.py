from chessboard import ChessBoard
from chessman import *
import unittest

class ChessBoardTest(unittest.TestCase):

    def test_add_chessman(self):
        board = ChessBoard(10, 20)
        chess1 = ChessMan(ChessColor())
        chess2 = ChessMan(ChessColor())
        board.add_chessman(1, 1, chess1)
        board.add_chessman(2, 1, chess2)
        self.assertEqual(chess1, board.get_chessman(1,1))
        self.assertEqual(chess2, board.get_chessman(2,1))
        self.assertEqual(None, board.get_chessman(3,1))

    def test_get_chessman(self):
        board = ChessBoard(40, 20)
        chess1 = ChessMan(ChessColor())
        chess2 = ChessMan(ChessColor())
        board.add_chessman(1, 1, chess1)
        board.add_chessman(2, 1, chess2)
        self.assertEqual(chess1, board.get_chessman(1,1))
        self.assertEqual(chess2, board.get_chessman(2,1))
        self.assertEqual(None, board.get_chessman(3,1))

    def test_check_n_chessman(self):
        board = ChessBoard(40, 20)
        color = ChessColor()
        board.add_chessman(1, 1, ChessMan(color))
        board.add_chessman(2, 2, ChessMan(color))
        board.add_chessman(3, 3, ChessMan(color))
        board.add_chessman(4, 4, ChessMan(color))
        board.add_chessman(5, 5, ChessMan(color))
        board.add_chessman(6, 4, ChessMan(color))
        board.add_chessman(7, 3, ChessMan(color))
        board.add_chessman(8, 2, ChessMan(color))
        board.add_chessman(9, 1, ChessMan(color))
        self.assertTrue(board.check_n_chessman(1, 1, 5))
        self.assertTrue(board.check_n_chessman(2, 2, 5))
        self.assertTrue(board.check_n_chessman(5, 5, 5))
        self.assertFalse(board.check_n_chessman(6, 6, 5))
        self.assertTrue(board.check_n_chessman(6, 4, 5))
        self.assertTrue(board.check_n_chessman(9, 1, 5))
        self.assertTrue(board.check_n_chessman(8, 2, 5))
        self.assertFalse(board.check_n_chessman(9, 2, 5))
    def test_get_corner(self):
        board = ChessBoard(5, 5)
        up = lambda x, y: (x, y - 1)
        down = lambda x, y: (x, y + 1)
        left = lambda x, y: (x - 1, y)
        right = lambda x, y: (x + 1, y)
        upper_left = lambda x, y: left(*up(x, y))
        lower_left = lambda x, y: left(*down(x,y))
        upper_right = lambda x, y: right(*up(x, y))
        lower_right = lambda x, y: right(*down(x, y))
        self.assertEqual(board.get_corner(3,2, up), (3, 0))
        self.assertEqual(board.get_corner(3,2, down), (3, 6))
        self.assertEqual(board.get_corner(3,2, upper_left), (1, 0))
        self.assertEqual(board.get_corner(3,2, lower_left), (0, 5))
        self.assertEqual(board.get_corner(3,2, upper_right), (5, 0))
        self.assertEqual(board.get_corner(3,2, lower_right), (6, 5))
        self.assertEqual(board.get_corner(3,2, left), (0, 2))
        self.assertEqual(board.get_corner(3,2, right), (6, 2))

if __name__ == '__main__':
    unittest.main()
