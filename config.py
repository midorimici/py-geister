'''定数を定義する'''
import numpy as np

# ウィンドウサイズ
DISP_SIZE = (600, 600)

# 色の設定
IVORY = (240, 227, 206)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GREY = (150, 150, 150)

# マスの大きさ
SQUARE_SIZE = 90
# マージン幅
MARGIN = (np.asarray(DISP_SIZE) - 6*SQUARE_SIZE)/2
# 駒の大きさ
PIECE_SIZE = 60