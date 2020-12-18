import sys

import pygame
from pygame.locals import *

from config import IVORY
import draw, mouse


def main(screen, font, orders, move_snd, chturn_snd):
    # ボード描画に渡すパラメータ
    # 0 - 先攻, 1 - 後攻
    _turn = 0
    # 次の番を確認する画面を表示するときに渡すパラメータ
    # 0 - 先攻, 1 - 後攻, 2 - なし
    _next = 0
    # ゲームボード {(int, int): Piece}
    _board = orders
    # 取った駒 [{'R': int, 'B': int}]
    _taken_pieces = [{'R': 0, 'B': 0}, {'R': 0, 'B': 0}]
    # マウス選択中の駒の位置
    _selecting_pos = None
    # 動かし終わった
    _move_finished = False

    while True:
        screen.fill(IVORY)
        draw.board(screen, _board, _turn)
        if _next == 0 or _next == 1:
            draw.confirmation(screen, font, _next)
        elif _selecting_pos is not None:
            draw.dest(screen, _selecting_pos, _board)
        draw.taken_pieces(screen, _taken_pieces)
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
                    if _move_finished: continue
                    # 駒
                    if _square_pos in _board and _board[_square_pos].side == _turn:
                        _selecting_pos = _square_pos
                    else:
                        # 行先を選択したとき
                        if (_selecting_pos in _board
                                and _square_pos in _board[_selecting_pos].covering_squares(_selecting_pos)):
                            # 行先が相手の駒のとき
                            if _square_pos in _board and _board[_square_pos].side != _turn:
                                _taken_pieces[_turn][_board[_square_pos].color] += 1
                            # 駒の移動
                            move_snd.play()
                            _board[_square_pos] = _board[_selecting_pos]
                            del _board[_selecting_pos]
                            # 移動完了
                            _move_finished = True
                        _selecting_pos = None
            # キー
            if event.type == KEYDOWN:
                # Esc キー
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Enter キー
                if event.key == K_RETURN:
                    if _move_finished:
                        # ターン交代
                        chturn_snd.play()
                        _turn = (_turn+1)%2
                        _next = _turn
                        _move_finished = False
