import pygame
from pygame.locals import *
import sys

from utils import IVORY, draw_board

def main(screen):
    while True:
        screen.fill(IVORY)
        draw_board(screen)
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
