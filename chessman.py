''' The color of the chess man '''
class ChessColor(object):
    def __init__(self, c: str = '#'):
        self.color = c

    def get_color(self) -> str:
        return self.color

''' Represent a chessman '''
class ChessMan(object):
    def __init__(self, color: ChessColor):
        self.color = color

    def get_color(self) -> ChessColor:
        return self.color
