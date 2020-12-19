import numpy as np
import pygame
from pygame.locals import *

from config import *


def _triangle_points(coord, size, rev=False):
    '''
    三角形の各頂点を出力
    -> list <- [(int, int)]

    coord : tuple <- (int, int)
        中央の頂点の座標
    size : int
        三角形のサイズ
    rev : bool (=False)
        逆転する
    '''
    coord = np.asarray(coord)
    if rev:
        return [coord,
        coord - (-size/2, size),
        coord - (size/2, size)]
    else:
        return [coord,
            coord + (-size/2, size),
            coord + (size/2, size)]


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
        pygame.draw.line(screen, BLACK,
            _coord, _coord + (PIECE_SIZE/2, -PIECE_SIZE/2), 2)
        pygame.draw.line(screen, BLACK,
            _coord, _coord - (PIECE_SIZE/2, PIECE_SIZE/2), 2)
        pygame.draw.line(screen, BLACK,
            _coord, _coord - (0, PIECE_SIZE), 2)
    else:
        pygame.draw.line(screen, BLACK,
            _coord, _coord + (PIECE_SIZE/2, PIECE_SIZE/2), 2)
        pygame.draw.line(screen, BLACK,
            _coord, _coord + (-PIECE_SIZE/2, PIECE_SIZE/2), 2)
        pygame.draw.line(screen, BLACK,
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
        pygame.draw.line(screen, BLACK,
            _coord + (0, SQUARE_SIZE*i),
            _coord + (SQUARE_SIZE*col, SQUARE_SIZE*i), 2)
    for i in range(col+1):
        pygame.draw.line(screen, BLACK,
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
    rev : bool (=False)
        上下反転して表示する
    '''
    _padding = (SQUARE_SIZE - PIECE_SIZE)/2
    _coord = np.asarray(pos)*SQUARE_SIZE + (PIECE_SIZE/2, 0) + MARGIN + _padding
    if rev:
        _coord += (0, PIECE_SIZE)
        _points = _triangle_points(_coord, PIECE_SIZE, True)
    else:
        _points = _triangle_points(_coord, PIECE_SIZE)
    pygame.draw.polygon(screen, color, _points)


def _button(screen, font, coord, size, text, disabled):
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
    _text = font.render(text, True, BLACK)
    _fsize = np.asarray(font.size(text))
    screen.blit(_text, coord + (size-_fsize)/2)


def setup(screen, font, turn, posdict, disabled):
    '''
    screen : pygame.display.set_mode
    font : pygame.font.SysFont
        フォント
    turn : int <- 0 | 1
        先攻(0)か後攻(1)か
    posdict : dict <- {(int, int): str}
        どの位置にどの色の駒が置かれているかを表す辞書
    disabled : bool
        ボタンを押せない
    '''
    assert turn == 0 or turn == 1, 'draw.setup の引数 turn は 0, 1 の値を取ります'
    _text1 = font.render(
        ('先' if turn == 0 else '後') + '攻の駒の配置を決めてね（↓自分側　↑相手側）',
        True, BLACK)
    _text2 = font.render(
        '左クリックで悪いおばけ（赤）、右クリックで良いおばけ（青）を配置するよ',
        True, BLACK)
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
    board : dict <- {(int, int): Piece}
        駒の位置とオブジェクト
    turn : int <- 0 | 1 | 2
        0 - 先攻の駒を開く, 1 - 後攻の駒を開く, 2 - 両方開く,
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
            if piece.side == 0:
                _piece(screen, RED if piece.color == 'R' else BLUE, pos)
            else:
                _piece(screen, RED if piece.color == 'R' else BLUE, pos, True)
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


def confirmation(screen, font, font_small, turn):
    '''
    手番交代の確認画面を表示する

    screen : pygame.display.set_mode
    font, font_small : pygame.font.SysFont
        フォント
    turn : int <- 0 | 1
        0 - 次は先攻, 1 - 次は後攻
    '''
    assert turn == 0 or turn == 1, 'draw.confirmation の引数 turn は 0, 1 の値を取ります'
    screen.fill(WHITE, (*MARGIN, 6*SQUARE_SIZE, 6*SQUARE_SIZE))
    _str1 = ('先' if turn == 0 else '後') + '攻のターンだよ'
    _str2 = '画面をクリックしてね'
    _str3 = '動かし終わったら Enter キーを押してね'
    _text1 = font.render(_str1, True, BLACK)
    _text2 = font.render(_str2, True, BLACK)
    _text3 = font_small.render(_str3, True, BLACK)
    screen.blit(_text1, DISP_SIZE/2-(len(_str1)*32/2, 32))
    screen.blit(_text2, DISP_SIZE/2-(len(_str2)*32/2, -32))
    screen.blit(_text3, DISP_SIZE/2-(16*10, -32*4))


def dest(screen, pos, board):
    '''
    駒の行先を円で表示する

    screen : pygame.display.set_mode
    pos : tuple <- (int, int)
        駒の位置
    board : dict <- {(int, int): Piece}
        駒の位置とオブジェクト
    '''
    for _pos in board[pos].covering_squares(pos):
        # 自分の駒を除外
        if not (tuple(_pos) in board and board[tuple(_pos)].side == board[pos].side):
            _coord = np.asarray(_pos)*SQUARE_SIZE + MARGIN + SQUARE_SIZE/2
            pygame.draw.circle(screen, LAWNGREEN, [int(c) for c in _coord], int(PIECE_SIZE/2))


def taken_pieces(screen, numbers):
    '''
    取った駒を盤面の端に描画する

    screen : pygame.display.set_mode
    numbers : list <- [{'R': int, 'B': int}]
        色と数の辞書のリスト
    '''
    # 先攻が取った駒
    for i in range(numbers[0]['R']):
        _coord = (10+i*PIECE_SIZE_SMALL, MARGIN[1]+6*SQUARE_SIZE+10)
        pygame.draw.polygon(screen, RED, _triangle_points(_coord, PIECE_SIZE_SMALL))
    for i in range(numbers[0]['B']):
        _coord = (10+(numbers[0]['R']+i)*PIECE_SIZE_SMALL, MARGIN[1]+6*SQUARE_SIZE+10)
        pygame.draw.polygon(screen, BLUE, _triangle_points(_coord, PIECE_SIZE_SMALL))
    # 後攻が取った駒
    for i in range(numbers[1]['R']):
        _coord = (10+i*PIECE_SIZE_SMALL, 10)
        pygame.draw.polygon(screen, RED, _triangle_points(_coord, PIECE_SIZE_SMALL))
    for i in range(numbers[1]['B']):
        _coord = (10+(numbers[1]['R']+i)*PIECE_SIZE_SMALL, 10)
        pygame.draw.polygon(screen, BLUE, _triangle_points(_coord, PIECE_SIZE_SMALL))


def win_message(screen, font, side):
    '''
    勝敗の結果を知らせるメッセージを表示する

    screen : pygame.display.set_mode
    font : pygame.font.SysFont
        フォント
    side : int <- 0 | 1
    '''
    assert side == 0 or side == 1, 'draw.win_message の引数 side は 0, 1 の値を取ります'
    _str = ('先' if side == 0 else '後') + '攻の勝ち！'
    _text = font.render(_str, True, BLACK)
    _margin = (DISP_SIZE-(3*SQUARE_SIZE, SQUARE_SIZE))/2
    screen.fill(WHITE, (*_margin, 3*SQUARE_SIZE, SQUARE_SIZE))
    screen.blit(_text, DISP_SIZE/2-(len(_str)*32/2, 32/2))
