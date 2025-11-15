import time
import pygame
import sys

W, H = 1020, 840
screen = pygame.display.set_mode((W, H))
black = (0, 0, 0)

state = "menu"

font = pygame.font.SysFont(None, 48)

# buttons
show_btn = pygame.Rect(200, 300, 250, 80)
exit_btn = pygame.Rect(570, 300, 250, 80)


Rworker = make_worker(target_w, int(target_h * 0.55), color=(192,32,32))
Rcells = [pygame.Rect(i * cell_w, 0, cell_w, cell_h) for i in range(3)]
Rrects = [Rworker.get_rect(center=(c.left + c.width//2, c.top + c.height//2)) for c in Rcells]

# Blue workers (bottom third)
Bworker = make_worker(target_w, int(target_h * 0.55), color=(32,64,192))
Bcells = [pygame.Rect(i * cell_w, 2 * cell_h, cell_w, cell_h) for i in range(3)]
Brects = [Bworker.get_rect(center=(c.left + c.width//2, c.top + c.height//2)) for c in Bcells]



def make_worker(w, h, grey=(180,180,180), color=(192,32,32), outline=8):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    bar_h = int(h * 0.45)
    bar_w = int(w * 0.70)
    stub_w = int((w - bar_w) // 2)
    stub_h = int(h * 0.90)
    cx, cy = w // 2, h // 2



    center = pygame.Rect(0, 0, bar_w, bar_h); center.center = (cx, cy)
    left   = pygame.Rect(center.left - stub_w, (h - stub_h)//2, stub_w, stub_h)
    right  = pygame.Rect(center.right,         (h - stub_h)//2, stub_w, stub_h)

    for r in (center, left, right):
        pygame.draw.rect(surf, grey, r)
        pygame.draw.rect(surf, color, r, outline)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if state == "menu" and e.type == pygame.MOUSEBUTTONDOWN:
            if show_btn.collidepoint(e.pos):
                state = "workers"
            elif exit_btn.collidepoint(e.pos):
                pygame.quit(); sys.exit()

    screen.fill(black)

    if state == "menu":
        txt = font.render("Choose an option:", True, (255,255,255))
        screen.blit(txt, (W//2 - txt.get_width()//2, 150))

        pygame.draw.rect(screen, (80,80,80), show_btn)
        pygame.draw.rect(screen, (80,80,80), exit_btn)

        t1 = font.render("Show Workers", True, (255,255,255))
        t2 = font.render("Exit", True, (255,255,255))
        screen.blit(t1, (show_btn.centerx - t1.get_width()//2,
                         show_btn.centery - t1.get_height()//2))
        screen.blit(t2, (exit_btn.centerx - t2.get_width()//2,
                         exit_btn.centery - t2.get_height()//2))

    elif state == "workers":
        for r in Rrects: screen.blit(Rworker, r)
        for r in Brects: screen.blit(Bworker, r)

    pygame.display.flip()