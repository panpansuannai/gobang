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

if __name__ == '__main__':
    unittest.main()
