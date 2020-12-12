import sys

from utils import *


def check_color(colors):
    '''
    駒がすべて配置済みで赤と青が半分ずつあるか
    -> bool

    colors : list <- [str]
        色のリスト
    '''
    return (len(colors) == 8
        and len([s for s in colors if s == 'R'])
            == len([s for s in colors if s == 'B']))


def main():
    pygame.init()
    args = sys.argv
    _flag = FULLSCREEN if len(args) == 2 and args[1] == 'f' else 0
    screen = pygame.display.set_mode(DISP_SIZE, _flag)
    pygame.display.set_caption('Geister')
    font = pygame.font.SysFont('hg丸ｺﾞｼｯｸmpro', 16)
    order = {}

    while True:
        screen.fill(IVORY)
        draw_setup(screen, font, 1, order, not check_color(list(order.values())))
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
                    _square_pos = tuple(chcoord(_mouse_pos))

                    for i in range(1, 5):
                        for j in range(2, 4):
                            if _square_pos == (i, j):
                                order[(i, j)] = 'R'
                # 右
                elif event.button == 3:
                    _mouse_pos = event.pos
                    _square_pos = tuple(chcoord(_mouse_pos))

                    for i in range(1, 5):
                        for j in range(2, 4):
                            if _square_pos == (i, j):
                                order[(i, j)] = 'B'
            # キー
            if event.type == KEYDOWN:
                # Esc キー
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__': main()