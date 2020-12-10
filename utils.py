import pygame
from pygame.locals import *


# 色の設定
RED = (200, 0, 0)
BLUE = (0, 0, 200)



def draw_button(screen, font, coord, size, text):
    '''
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
    '''
    pygame.draw.rect(screen, (200, 180, 160), Rect(*coord, *size))
    _text = font.render(text, True, (0, 0, 0))
    screen.blit(_text, (coord[0]+size[0]/3, coord[1]+size[1]/3))


def draw_grid(screen, coord, col, row):
    '''
    各マス 90x90 のグリッドを描く

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
            (coord[0], coord[1]+90*i), (coord[0]+90*col, coord[1]+90*i), 2)
    for i in range(col+1):
        pygame.draw.line(screen, (0, 0, 0),
            (coord[0]+90*i, coord[1]), (coord[0]+90*i, coord[1]+90*row), 2)


def draw_piece(screen, color, pos):
    pygame.draw.rect(screen, color,
        Rect(90*pos[0]+30, 90*pos[1]+30, 60, 60))


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
    '''draw_grid(screen, (105, 105), 4, 2)

    for i in range(4):
        draw_piece(screen, RED, (i+1, 3))
    for i in range(4):
        draw_piece(screen, BLUE, (i+1, 4))

    draw_button(screen, font, (500, 540), (80, 50), 'OK')'''