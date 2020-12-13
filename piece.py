import numpy as np

class Piece:
    def __init__(self, color, side):
        self.color = color  # 赤('R') or 青('B')
        self.side = side    # 先攻(0) or 後攻(1)
    
    def __repr__(self):
        return self.color + str(self.side)
    
    def covering_squares(self, pos):
        '''
        可能な移動先のマスのリスト
        -> list <- [(int, int)]

        pos : tuple <- (int, int)
            現在の位置
        '''
        _pos = np.asarray(pos) + [(0, 1), (0, -1), (-1, 0), (1, 0)]
        return [(x, y) for x, y in _pos if 0 <= x <= 5 and 0 <= y <= 5]