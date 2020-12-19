'''定数を定義する'''
import numpy as np

# ウィンドウサイズ
DISP_SIZE = np.asarray((600, 600))

# 色の設定
IVORY = (240, 227, 206)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
LAWNGREEN = (124, 252, 0)
GREY = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# マスの大きさ
SQUARE_SIZE = 90
# マージン幅
MARGIN = (np.asarray(DISP_SIZE) - 6*SQUARE_SIZE)/2
# 駒の大きさ
PIECE_SIZE = 60
# 盤面端に表示する駒の大きさ
PIECE_SIZE_SMALL = 10