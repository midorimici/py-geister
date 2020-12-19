import sys

import pygame
from pygame.locals import *

from config import IVORY
import draw, mouse


def win_req(taken, board, side, moved):
    '''
    side が勝利条件を満たすか
    -> bool

    taken : list <- [{'R': int, 'B': int}]
        取った駒
    board : dict <- {(int, int): Piece}
        ゲームボード
    side : int <- 0 | 1
        先攻(0), 後攻(1)
    moved : bool
        side が今駒を動かしたか
    '''
    assert side == 0 or side == 1, 'game.win_req の引数 side は 0, 1 の値を取ります'
    if not moved:
        # 赤を4つ取らせた
        if taken[(side+1)%2]['R'] == 4:
            return True
    else:
        # 青を4つ取った
        if taken[side]['B'] == 4:
            return True
        # 青が盤外に出た
        if side == 0 and ((0, -1) in board or (5, -1) in board):
            return True
        if side == 1 and ((0, 6) in board or (5, 6) in board):
            return True


def main(screen, font, font_small, orders, move_snd, chturn_snd, win_snd):
    # ボード描画に渡すパラメータ
    # 0 - 先攻, 1 - 後攻, 2 - 終了後
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
    # 勝者
    # 0 - 先攻, 1 - 後攻
    _winner = -1

    while True:
        screen.fill(IVORY)
        # 盤面
        draw.board(screen, _board, _turn)
        if _next == 0 or _next == 1:
            # 交代確認画面
            draw.confirmation(screen, font, font_small, _next)
        elif _selecting_pos is not None:
            # 行先
            draw.dest(screen, _selecting_pos, _board)
        # 取られた駒
        draw.taken_pieces(screen, _taken_pieces)
        # 勝敗
        if _winner == 0 or _winner == 1:
            draw.win_message(screen, font, _winner)
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
                            # 勝利判定
                            if win_req(_taken_pieces, _board, _turn, True):
                                win_snd.play()
                                _winner = _turn
                            if win_req(_taken_pieces, _board, (_turn+1)%2, False):
                                win_snd.play()
                                _winner = (_turn+1)%2
                        _selecting_pos = None
            # キー
            if event.type == KEYDOWN:
                # Esc キー
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Enter キー
                if event.key == K_RETURN:
                    if _winner == 0 or _winner == 1:
                        # 開示
                        _winner = 2
                        _turn = 2
                    elif _move_finished:
                        # ターン交代
                        chturn_snd.play()
                        _turn = (_turn+1)%2
                        _next = _turn
                        _move_finished = False
