import sys

import pygame
from pygame.locals import *

from config import IVORY
import draw, mouse


# ボード描画に渡すパラメータ
# 0 - 先攻, 1 - 後攻
_turn = 0
# 次の番を確認する画面を表示するときに渡すパラメータ
# 0 - 先攻, 1 - 後攻, 2 - なし
_next = 0


def main(screen, font, orders):
    global _turn, _next
    _board = orders
    while True:
        screen.fill(IVORY)
        draw.board(screen, _board, _turn)
        if _next == 0 or _next == 1:
            draw.confirmation(screen, font, _next)
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
                    # 確認画面のクリック
                    if _next == 0 or _next == 1:
                        _next = 2
                        continue
                    # 駒
                    if _square_pos in _board:
                        print(_board[_square_pos])
            # キー
            if event.type == KEYDOWN:
                # Esc キー
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
