import numpy as np
import pygame
from pygame.locals import *

from config import *


def _arrow(screen, coord, direction):
    '''
    矢印を描く

    screen : pygame.display.set_mode
    coord : tuple <- (int, int)
        矢先の座標
    direction : str <- 'U', 'D'
        'U' - 上, 'D' - 下
    '''
    assert direction == 'U' or direction == 'D',\
        'draw._arrow の引数 direction は "U", "D" の値を取ります'
    _coord = np.asarray(coord)
    if direction == 'D':
        pygame.draw.line(screen, (0, 0, 0),
            _coord, _coord + (PIECE_SIZE/2, -PIECE_SIZE/2), 2)
        pygame.draw.line(screen, (0, 0, 0),
            _coord, _coord - (PIECE_SIZE/2, PIECE_SIZE/2), 2)
        pygame.draw.line(screen, (0, 0, 0),
            _coord, _coord - (0, PIECE_SIZE), 2)
    else:
        pygame.draw.line(screen, (0, 0, 0),
            _coord, _coord + (PIECE_SIZE/2, PIECE_SIZE/2), 2)
        pygame.draw.line(screen, (0, 0, 0),
            _coord, _coord + (-PIECE_SIZE/2, PIECE_SIZE/2), 2)
        pygame.draw.line(screen, (0, 0, 0),
            _coord, _coord + (0, PIECE_SIZE), 2)


def _grid(screen, coord, col, row):
    '''
    一辺が SQUARE_SIZE のマスのグリッドを描く

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
            _coord + (0, SQUARE_SIZE*i),
            _coord + (SQUARE_SIZE*col, SQUARE_SIZE*i), 2)
    for i in range(col+1):
        pygame.draw.line(screen, (0, 0, 0),
            _coord + (SQUARE_SIZE*i, 0),
            _coord + (SQUARE_SIZE*i, SQUARE_SIZE*row), 2)


def _piece(screen, color, pos, rev=False):
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
    _padding = (SQUARE_SIZE - PIECE_SIZE)/2
    _coord = np.asarray(pos)*SQUARE_SIZE + MARGIN + _padding
    if rev:
        _points = [_coord,
            _coord + (PIECE_SIZE, 0),
            _coord + (PIECE_SIZE/2, PIECE_SIZE)]
    else:
        _points = [_coord + (0, PIECE_SIZE),
            _coord + (PIECE_SIZE, PIECE_SIZE),
            _coord + (PIECE_SIZE/2, 0)]
    pygame.draw.polygon(screen, color, _points)


def _button(screen, font, coord, size, text, disabled=False):
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


def setup(screen, font, turn, posdict, disabled):
    '''
    screen : pygame.display.set_mode
    font : pygame.font.SysFont
        フォント
    turn : int
        先攻(0)か後攻(1)か
    posdict : dict <- {(int, int): str}
        どの位置にどの色の駒が置かれているかを表す辞書
    disabled : bool
        ボタンを押せない
    '''
    assert turn == 0 or turn == 1, 'draw.setup の引数 turn は 0, 1 の値を取ります'
    _text1 = font.render(
        ('先' if turn == 0 else '後') + '攻の駒の配置を決めてね（↓自分側　↑相手側）',
        True, (0, 0, 0))
    _text2 = font.render(
        '左クリックで悪いおばけ（赤）、右クリックで良いおばけ（青）を配置するよ',
        True, (0, 0, 0))
    screen.blit(_text1, (20, 20))
    screen.blit(_text2, (20, 50))
    _grid(screen, MARGIN + SQUARE_SIZE + (0, SQUARE_SIZE), 4, 2)

    for (x, y), s in posdict.items():
        _piece(screen, RED if s == 'R' else BLUE, (x, y))

    _button(screen, font, (500, 530), (80, 50), 'OK', disabled)


def board(screen, board, turn):
    '''
    ゲームボードと盤面上の駒を描く

    screen : pygame.display.set_mode
    board : dict <- {(int, int): obj}
        駒の位置とオブジェクト
    turn : int <- 0, 1, 2
        0 - 先攻の駒を開く, 1 - 後攻の駒を開く, 2 - 両方伏せる,
    '''
    assert turn == 0 or turn == 1 or turn == 2, 'draw.board の引数 turn は 0, 1, 2 の値を取ります'
    # グリッド
    _grid(screen, MARGIN, 6, 6)
    # 角の矢印
    _padding = (SQUARE_SIZE - PIECE_SIZE)/2
    _arrow(screen, MARGIN+(SQUARE_SIZE/2, _padding), 'U')
    _arrow(screen, MARGIN+(11*SQUARE_SIZE/2, _padding), 'U')
    _arrow(screen, DISP_SIZE-MARGIN-(SQUARE_SIZE/2, _padding), 'D')
    _arrow(screen, DISP_SIZE-MARGIN-(11*SQUARE_SIZE/2, _padding), 'D')
    # 駒
    for pos, piece in board.items():
        if turn == 2:
            _piece(screen, GREY, pos, True if piece.side == 1 else False)
        elif turn == 0:
            if piece.side == 0:
                _piece(screen, RED if piece.color == 'R' else BLUE, pos)
            else:
                _piece(screen, GREY, pos, True)
        elif turn == 1:
            if piece.side == 0:
                _piece(screen, GREY, pos)
            else:
                _piece(screen, RED if piece.color == 'R' else BLUE, pos, True)


def confirmation(screen, font, turn):
    '''
    手番交代の確認画面を表示する

    screen : pygame.display.set_mode
    font : pygame.font.SysFont
        フォント
    turn : int <- 0, 1
        0 - 次は先攻, 1 - 次は後攻
    '''
    assert turn == 0 or turn == 1, 'draw.confirmation の引数 turn は 0, 1 の値を取ります'
    pygame.draw.rect(screen, (255, 255, 255), (*MARGIN, 6*SQUARE_SIZE, 6*SQUARE_SIZE))
    _str1 = ('先' if turn == 0 else '後') + '攻のターンだよ'
    _str2 = '画面をクリックしてね'
    _text1 = font.render(_str1, True, (0, 0, 0))
    _text2 = font.render(_str2, True, (0, 0, 0))
    screen.blit(_text1, DISP_SIZE/2-(len(_str1)*32/2, 32))
    screen.blit(_text2, DISP_SIZE/2-(len(_str2)*32/2, -32))
