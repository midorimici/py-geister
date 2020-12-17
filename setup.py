import sys

import pygame
from pygame.locals import *

from config import IVORY
import draw, mouse
from piece import Piece


_state = 0
_order = [{}, {}]


def _check_color(colors):
    '''
    駒がすべて配置済みで赤と青が半分ずつあるか
    -> bool

    colors : list <- [str]
        色のリスト
    '''
    return (len(colors) == 8
        and len([s for s in colors if s == 'R'])
            == len([s for s in colors if s == 'B']))


def _init_board(order1, order2):
    '''
    駒の配置から初期盤面を出力
    -> dict <- {(int, int): obj}

    order1, order2 : dict <- {(int, int): str}
        駒の初期配置. order1 が先攻
    '''
    return {**{(5-x, 3-y): Piece(s, 1) for (x, y), s in order2.items()},
        **{(x, y+2): Piece(s, 0) for (x, y), s in order1.items()}}


def main(screen, font, select_snd, decide_snd, forbid_snd):
    global _order, _state

    while True:
        satisfied = _check_color(list(_order[_state].values()))

        screen.fill(IVORY)
        draw.setup(screen, font, _state, _order[_state], not satisfied)
        pygame.display.update()

        # イベントハンドリング
        for event in pygame.event.get():
            # 閉じるボタン
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # マウスクリック
            if event.type == MOUSEBUTTONDOWN:
                # 左
                if event.button == 1:
                    _mouse_pos = event.pos
                    _square_pos = tuple(mouse.chcoord(_mouse_pos))

                    for i in range(1, 5):
                        for j in range(2, 4):
                            if _square_pos == (i, j):
                                select_snd.play()
                                _order[_state][(i, j)] = 'R'
                    
                    if mouse.on_area(*_mouse_pos, 500, 530, 80, 50):
                        if satisfied:
                            decide_snd.play()
                            if _state == 1: return _init_board(*_order)
                            _state += 1
                        else:
                            forbid_snd.play()
                # 右
                elif event.button == 3:
                    _mouse_pos = event.pos
                    _square_pos = tuple(mouse.chcoord(_mouse_pos))

                    for i in range(1, 5):
                        for j in range(2, 4):
                            if _square_pos == (i, j):
                                select_snd.play()
                                _order[_state][(i, j)] = 'B'
            # キー
            if event.type == KEYDOWN:
                # Esc キー
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
