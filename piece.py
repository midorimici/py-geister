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
        pos_ = np.asarray(pos) + [(0, 1), (0, -1), (-1, 0), (1, 0)]
        dest = [(x, y) for x, y in pos_ if 0 <= x <= 5 and 0 <= y <= 5]
        if self.color == 'B':
            if self.side == 0:
                if pos == (0, 0):
                    dest += [(0, -1)]
                if pos == (5, 0):
                    dest += [(5, -1)]
            elif self.side == 1:
                if pos == (0, 5):
                    dest += [(0, 6)]
                if pos == (5, 5):
                    dest += [(5, 6)]
                
        return dest