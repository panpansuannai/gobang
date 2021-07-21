''' The color of the chess man '''
class ChessColor(object):
    def __init__(self, c: str = '#'):
        self.c = c

    def color(self) -> str:
        return self.c

''' Represent a chessman '''
class ChessMan(object):
    def __init__(self, color: ChessColor):
        self.color = color

    def get_color(self) -> ChessColor:
        return self.color
    
    def __str__(self):
        return self.color.color()
