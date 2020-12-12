import numpy as np

import pygame
from pygame.locals import *

# ウィンドウサイズ
DISP_SIZE = (600, 600)

# 色の設定
IVORY = (240, 227, 206)
_RED = (200, 0, 0)
_BLUE = (0, 0, 200)

# マスの大きさ
_SQUARE_SIZE = 90
# マージン幅
_MARGIN = (np.asarray(DISP_SIZE) - 6*_SQUARE_SIZE)/2
# 駒の大きさ
_PIECE_SIZE = 60


def _draw_grid(screen, coord, col, row):
    '''
    一辺が _SQUARE_SIZE のマスのグリッドを描く

    screen : pygame.display.set_mode
    coord : tuple <- (int, int)
        左上の座標
    col : int
        列数
    row : int
        行数
    '''
    _coord = np.asarray(coord)
    for i in range(row+1):
        pygame.draw.line(screen, (0, 0, 0),
            _coord + (0, _SQUARE_SIZE*i),
            _coord + (_SQUARE_SIZE*col, _SQUARE_SIZE*i), 2)
    for i in range(col+1):
        pygame.draw.line(screen, (0, 0, 0),
            _coord + (_SQUARE_SIZE*i, 0),
            _coord + (_SQUARE_SIZE*i, _SQUARE_SIZE*row), 2)


def _draw_piece(screen, color, pos, rev=False):
    '''
    駒を描画する

    screen : pygame.display.set_mode
    color : tuple <- (int, int, int)
        駒の色
    pos : tuple <- (int, int)
        盤面上の駒の位置
    rev : bool
        上下反転して表示する
    '''
    _padding = (_SQUARE_SIZE - _PIECE_SIZE)/2
    _coord = np.asarray(pos)*_SQUARE_SIZE + _MARGIN + _padding
    if rev:
        _points = [_coord,
            _coord + (_PIECE_SIZE, 0),
            _coord + (_PIECE_SIZE/2, _PIECE_SIZE)]
    else:
        _points = [_coord + (0, _PIECE_SIZE),
            _coord + (_PIECE_SIZE, _PIECE_SIZE),
            _coord + (_PIECE_SIZE/2, 0)]
    pygame.draw.polygon(screen, color, _points)


def _draw_button(screen, font, coord, size, text, disabled=True):
    '''
    ボタンを描画する

    screen : pygame.display.set_mode
    font : pygame.font.SysFont
        フォント
    color : tuple <- (int, int, int)
        背景色
    coord : tuple <- (int, int)
        左上の座標
    size : tuple <- (int, int)
        横、縦のサイズ
    text : str
        中身のテキスト
    disabled : bool
        押せなくする
    '''
    _color = (160, 140, 120) if disabled else (200, 180, 160)
    screen.fill(_color, (*coord, *size))
    _text = font.render(text, True, (0, 0, 0))
    _fsize = np.asarray(font.size(text))
    screen.blit(_text, coord + (size-_fsize)/2)


def draw_setup(screen, font, turn, posdict, disabled):
    '''
    screen : pygame.display.set_mode
    font : pygame.font.SysFont
        フォント
    turn : int
        先攻(1)か後攻(2)か
    posdict : dict <- {(int, int): str}
        どの位置にどの色の駒が置かれているかを表す辞書
    disabled : bool
        ボタンを押せない
    '''
    _text = font.render(('先' if turn == 1 else '後') + '攻の駒の配置を決めてね（↓自分側　↑相手側）',
        True, (0, 0, 0))
    screen.blit(_text, (20, 20))
    _draw_grid(screen, _MARGIN + _SQUARE_SIZE + (0, _SQUARE_SIZE), 4, 2)

    for (x, y), s in posdict.items():
        _draw_piece(screen, _RED if s == 'R' else _BLUE, (x, y))

    _draw_button(screen, font, (500, 530), (80, 50), 'OK', disabled)


def on_area(x, y, left, right, top, bottom):
    '''
    座標 x, y が範囲内にあるか
    -> bool

    x, y : int
        対象の座標
    left, right, top, bottom : int
        範囲の端の座標
    '''
    return left <= x <= right and top <= y <= bottom


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
    return (pos-_MARGIN)//_SQUARE_SIZE
    