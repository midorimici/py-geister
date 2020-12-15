import sys

import pygame
from pygame.locals import *

from config import IVORY
import draw


def main(screen, orders):
    while True:
        screen.fill(IVORY)
        draw.board(screen, orders, 0)
        pygame.display.update()

        # イベントハンドリング
        for event in pygame.event.get():
            # 閉じるボタン
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # キー
            if event.type == KEYDOWN:
                # Esc キー
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
