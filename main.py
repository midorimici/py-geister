import sys

from utils import *

# ウィンドウサイズ
DISP_W = 600
DISP_H = 600

# 色の設定
IVORY = (240, 227, 206)


def main():
    pygame.init()
    args = sys.argv
    _flag = FULLSCREEN if len(args) == 2 and args[1] == 'f' else 0
    screen = pygame.display.set_mode((DISP_W, DISP_H), _flag)
    pygame.display.set_caption('Geister')
    font = pygame.font.SysFont('hg丸ｺﾞｼｯｸmpro', 16)

    while True:
        screen.fill(IVORY)
        draw_setup(screen, font, 1)
        pygame.display.update()

        # イベントハンドリング
        for event in pygame.event.get():
            # 閉じるボタン
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # マウスクリック
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                _mousepos = event.pos
                print(_mousepos)
            # キー
            if event.type == KEYDOWN:
                # Esc キー
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__': main()