import os
import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, 5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (5, 0)}

def check_bound(rct, scr_rct):
    """
    [1] rct: こうかとん or 爆弾のRect
    [2] scr_rct: スクリーンのRect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if rct.left < scr_rct.left or scr_rct.right < rct.right:
        yoko = -1
    if rct.top < scr_rct.top or scr_rct.bottom < rct.bottom:
        tate = -1
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    bb_vx, bb_vy = +5, +5

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        """
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5
        """
        for key, move in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += move[0]
                sum_mv[1] += move[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct, screen.get_rect()) != (1, 1):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(bb_vx, bb_vy)
        yoko, tate = check_bound(bb_rct, screen.get_rect())
        if yoko == -1:
            bb_vx *= -1
        if tate == -1:
            bb_vy *= -1
        screen.blit(bb_img, bb_rct)

        colliderect = kk_rct.colliderect(bb_rct)
        if colliderect:
            print("GAME OVER")
            return

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
