import pygame
from pygame.locals import *


# 色の設定
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# マスの大きさ
SQUARE_SIZE = 90
# 駒の大きさ
PIECE_SIZE = 60


def draw_button(screen, font, coord, size, text, disabled=True):
    '''
    ボタンを描画する

    Parameters
    ----------
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
    screen.blit(_text, (coord[0]+size[0]/3, coord[1]+size[1]/3))


def draw_grid(screen, coord, col, row):
    '''
    一辺が SQUARE_SIZE のマスのグリッドを描く

    Parameters
    ----------
    screen : pygame.display.set_mode
    coord : tuple <- (int, int)
        左上の座標
    col : int
        列数
    row : int
        行数
    '''
    for i in range(row+1):
        pygame.draw.line(screen, (0, 0, 0),
            (coord[0], coord[1]+SQUARE_SIZE*i),
            (coord[0]+SQUARE_SIZE*col, coord[1]+SQUARE_SIZE*i), 2)
    for i in range(col+1):
        pygame.draw.line(screen, (0, 0, 0),
            (coord[0]+SQUARE_SIZE*i, coord[1]),
            (coord[0]+SQUARE_SIZE*i, coord[1]+SQUARE_SIZE*row), 2)


def draw_piece(screen, color, pos, rev=False):
    '''
    駒を描画する

    Parameters
    ----------
    screen : pygame.display.set_mode
    color : tuple <- (int, int, int)
        駒の色
    pos : tuple <- (int, int)
        盤面上の駒の位置
    rev : bool
        上下反転して表示する
    '''
    _padding = (SQUARE_SIZE - PIECE_SIZE)/2
    _x = SQUARE_SIZE*pos[0]+30+_padding
    _y = SQUARE_SIZE*pos[1]+30+_padding
    if rev:
        _points = [[_x, _y],
        [_x+PIECE_SIZE, _y],
        [_x+PIECE_SIZE/2, _y+PIECE_SIZE]]
    else:
        _points = [[_x, _y+PIECE_SIZE],
            [_x+PIECE_SIZE, _y+PIECE_SIZE],
            [_x+PIECE_SIZE/2, _y]]
    pygame.draw.polygon(screen, color, _points)


def draw_setup(screen, font, turn):
    '''
    Parameters
    ----------
    screen : pygame.display.set_mode
    font : pygame.font.SysFont
        フォント
    turn : int
        先攻(1)か後攻(2)か
    '''
    _text = font.render(('先' if turn == 1 else '後') + '攻の駒の配置を決めてね（↓自分側　↑相手側）',
        True, (0, 0, 0))
    screen.blit(_text, (20, 20))
    draw_grid(screen, (30+SQUARE_SIZE, 30+SQUARE_SIZE), 4, 2)

    for i in range(4):
        draw_piece(screen, RED, (i+1, 3))
    for i in range(4):
        draw_piece(screen, BLUE, (i+1, 4))

    draw_button(screen, font, (500, 530), (80, 50), 'OK')