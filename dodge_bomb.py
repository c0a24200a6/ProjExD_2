import os
import sys
import random
import pygame as pg
import time


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

def gameover(screen: pg.Surface) -> None:
    
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(180)  
    screen.blit(overlay, (0, 0))

    font = pg.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
    screen.blit(text, text_rect)

    kk_go_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    kk_w = kk_go_img.get_width()
    kk_h = kk_go_img.get_height()

    left_pos = (WIDTH//2 - 250, HEIGHT//2 + 50)
    screen.blit(kk_go_img, kk_go_img.get_rect(center=left_pos))

    right_pos = (WIDTH//2 + 250, HEIGHT//2 + 50)
    screen.blit(kk_go_img, kk_go_img.get_rect(center=right_pos))

    pg.display.update()
    time.sleep(5)

    #pg.time.wait(5000)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
        bb_accs.append(random.randint(1, 10))
    return bb_imgs, bb_accs

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    img = pg.image.load("fig/3.png")
    img_r = pg.transform.flip(img, True, False)

    kk_dict = {
        (0, 0): pg.transform.rotozoom(img, 0, 0.9),      
        (0, -5): pg.transform.rotozoom(img_r, 90, 0.9),     
        (0, 5): pg.transform.rotozoom(img_r, -90, 0.9),    
        (-5, 0): pg.transform.rotozoom(img, 0, 0.9),    
        (5, 0): pg.transform.flip(img, True, False),    
        (-5, -5): pg.transform.rotozoom(img, -45, 0.9),   
        (5, -5): pg.transform.rotozoom(img_r, 45, 0.9),   
        (-5, 5): pg.transform.rotozoom(img, 45, 0.9),   
        (5, 5): pg.transform.rotozoom(img_r, -45, 0.9),   
    }
    return kk_dict

"""
def calc_orientation(org: pg.Rect, dst: pg.Rect, current_xy: tuple[float, float]) -> tuple[float, float]:
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery

    distance = (dx**2 + dy**2) ** 0.5

    if distance == 0:
        return current_xy

    if distance < 300:
        return current_xy

    norm_dx = dx / distance
    norm_dy = dy / distance

    speed = (50) ** 0.5  # √50 ≒ 7.07
    vx = norm_dx * speed
    vy = norm_dy * speed

    return vx, vy
"""


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

    bb_imgs, bb_accs = init_bb_imgs()
    kk_dict = get_kk_imgs()

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

        if tmr % 500 == 0 and tmr // 500 < 10:
            idx = tmr // 500
            old_center = bb_rct.center  

            bb_img = bb_imgs[idx]       
            bb_rct = bb_img.get_rect()
            bb_rct.center = old_center  

            acc = bb_accs[idx]
            bb_vx = (bb_vx / abs(bb_vx)) * (5 + acc)
            bb_vy = (bb_vy / abs(bb_vy)) * (5 + acc)

        for key, move in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += move[0]
                sum_mv[1] += move[1]
        
        kk_rct.move_ip(sum_mv)
        kk_img = kk_dict[tuple(sum_mv)]

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
            gameover(screen)
            print("GAME OVER")
            return
        
        #calc_orientation(kk_rct, bb_rct, kk_rct.center)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
