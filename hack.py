import sys, pygame

pygame.init()

W, H = 1020, 840
screen = pygame.display.set_mode((W, H))
black = (0, 0, 0)

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
    return surf

cell_w = W // 3
cell_h = H // 3
margin = 20

target_w = cell_w - 2 * margin
target_h = cell_h - 2 * margin

# Red workers (top third)
Rworker = make_worker(target_w, int(target_h * 0.55), color=(192,32,32))
Rcells = [pygame.Rect(i * cell_w, 0, cell_w, cell_h) for i in range(3)]
Rrects = [Rworker.get_rect(center=(c.left + c.width//2, c.top + c.height//2)) for c in Rcells]

# Blue workers (bottom third)
Bworker = make_worker(target_w, int(target_h * 0.55), color=(32,64,192))
Bcells = [pygame.Rect(i * cell_w, 2 * cell_h, cell_w, cell_h) for i in range(3)]
Brects = [Bworker.get_rect(center=(c.left + c.width//2, c.top + c.height//2)) for c in Bcells]

import time
start = time.time()

show_workers = False

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    if not show_workers and time.time() - start >= 2:
        show_workers = True

    screen.fill(black)

    if show_workers:
        for r in Rrects: screen.blit(Rworker, r)
        for r in Brects: screen.blit(Bworker, r)

    pygame.display.flip()