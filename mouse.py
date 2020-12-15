from config import MARGIN, SQUARE_SIZE


def on_area(x, y, left, top, w, h):
    '''
    座標 x, y が範囲内にあるか
    -> bool

    x, y : int
        対象の座標
    left, top : int
        範囲の左・上端の座標
    w, h : int
        範囲の横・縦幅
    '''
    return left <= x <= left+w and top <= y <= top+h


def chcoord(pos):
    '''
    座標 pos がどのマス上にあるかその位置を返す
    -> tuple <- (int, int)
    (0, 0)│...│(5, 0)
    ──────┼───┼──────
           ...
    ──────┼───┼──────
    (5, 0)│...│(5, 5)

    pos : tuple <- (int, int)
        対象の座標
    '''
    return (pos-MARGIN)//SQUARE_SIZE
