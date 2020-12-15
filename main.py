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

    args = sys.argv
    _flag = FULLSCREEN if len(args) == 2 and args[1] == 'f' else 0
    screen = pygame.display.set_mode(DISP_SIZE, _flag)
    pygame.display.set_caption('Geister')
    font = pygame.font.SysFont('hg丸ｺﾞｼｯｸmpro', 16)

    orders = setup.main(screen, font, select_snd, decide_snd, forbid_snd)
    game.main(screen, orders)
