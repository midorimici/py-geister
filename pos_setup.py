import sys

from utils import *


state = 0
order = [{}, {}]


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


def main():
    global order, state
    pygame.init()
    args = sys.argv
    _flag = FULLSCREEN if len(args) == 2 and args[1] == 'f' else 0
    screen = pygame.display.set_mode(DISP_SIZE, _flag)
    pygame.display.set_caption('Geister')
    font = pygame.font.SysFont('hg丸ｺﾞｼｯｸmpro', 16)

    while True:
        satisfied = _check_color(list(order[state].values()))

        screen.fill(IVORY)
        draw_setup(screen, font, state, order[state], not satisfied)
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
                                order[state][(i, j)] = 'R'
                    
                    if satisfied and on_area(*_mouse_pos, 500, 530, 80, 50):
                        state += 1
                # 右
                elif event.button == 3:
                    _mouse_pos = event.pos
                    _square_pos = tuple(chcoord(_mouse_pos))

                    for i in range(1, 5):
                        for j in range(2, 4):
                            if _square_pos == (i, j):
                                order[state][(i, j)] = 'B'
            # キー
            if event.type == KEYDOWN:
                # Esc キー
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
