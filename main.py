import sys

import pygame
from pygame.locals import *

from config import DISP_SIZE
import setup, game


if __name__ == '__main__':
    pygame.init()
    # 音声の設定
    snd = pygame.mixer.Sound
    select_snd = snd('./sounds/select.wav')
    decide_snd = snd('./sounds/decide.wav')
    forbid_snd = snd('./sounds/forbid.wav')
    move_snd = snd('./sounds/move.wav')
    chturn_snd = snd('./sounds/chturn.wav')

    # コマンドライン引数
    args = sys.argv
    # [f] フルスクリーン
    _flag = FULLSCREEN if len(args) >= 2 and 'f' in args[1:] else 0
    screen = pygame.display.set_mode(DISP_SIZE, _flag)
    # [m] ミュート
    if len(args) >= 2 and 'm' in args[1:]:
        select_snd.set_volume(0)
        decide_snd.set_volume(0)
        forbid_snd.set_volume(0)
        move_snd.set_volume(0)
        chturn_snd.set_volume(0)
    
    pygame.display.set_caption('Geister')
    font = pygame.font.SysFont('hg丸ｺﾞｼｯｸmpro', 16)
    font2 = pygame.font.SysFont('hg丸ｺﾞｼｯｸmpro', 32)

    orders = setup.main(screen, font, select_snd, decide_snd, forbid_snd)
    game.main(screen, font2, orders, move_snd, chturn_snd)
