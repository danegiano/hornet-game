import pygame, math, os
pygame.init()
W, H = 32, 32

def draw_hornet(state, frame=0):
    s = pygame.Surface((W, H), pygame.SRCALPHA)

    CLOAK_LIGHT = (220, 50, 60, 255)
    CLOAK_MID   = (180, 30, 40, 255)
    CLOAK_DARK  = (110, 15, 25, 255)
    MASK_LIGHT  = (255, 255, 255, 255)
    MASK_DARK   = (200, 200, 210, 255)
    BLACK       = (20, 20, 20, 255)
    NEEDLE_L    = (220, 220, 220, 255)
    NEEDLE_D    = (100, 100, 100, 255)
    WING        = (200, 240, 255, 120)

    breath     = 0
    body_lean  = 0

    if state == "idle":
        breath = 2 if frame == 1 else 0

    elif state == "run":
        breath    = 1 if frame == 0 else 0
        body_lean = -3

    elif state == "attack":
        body_lean = 3
        breath    = 0

    elif state == "jump":
        body_lean = -1
        breath    = 0

    if state != "attack":
        pygame.draw.ellipse(s, (0, 0, 0, 80), (10, 28, 12, 4))

    cloak_top = 15 + breath
    for y in range(cloak_top, 30):
        rel = y - cloak_top
        if state == "attack":
            width = 3 + int(rel * 0.9)
            tilt  = int(rel * 0.6)
            left  = 18 - width // 2 + tilt
        elif state == "run":
            width = 3 + int(rel * 1.0)
            tilt  = int(rel * 0.4)
            left  = 16 - width // 2 - tilt + body_lean
        elif state == "jump":
            width = 3 + int(rel * 0.7)
            left  = 16 - width // 2
        else:
            width = 4 + int(rel * 1.2)
            left  = 16 - width // 2
        right = left + width
        for x in range(left, right + 1):
            if x < 0 or x >= W:
                continue
            frac = (x - left) / max(1, width)
            if frac < 0.33:
                color = CLOAK_LIGHT
            elif frac > 0.67:
                color = CLOAK_DARK
            else:
                color = CLOAK_MID
            if (x - left) % 4 == 0 and 0 < (x - left) < width:
                color = CLOAK_DARK
            s.set_at((x, y), color)

    if state == "run":
        ls = 3 if frame == 0 else -3
    elif state == "attack":
        ls = 4
    else:
        ls = 0
    lx = 16 + (2 if state == "attack" else 0)
    pygame.draw.line(s, BLACK, (lx - 2, 28), (lx - 2 - ls, 31), 2)
    pygame.draw.line(s, BLACK, (lx + 2, 28), (lx + 2 + ls, 31), 2)

    hx = 16 + body_lean
    hy = 12 + breath

    pygame.draw.polygon(s, MASK_LIGHT, [(hx-4, hy-4), (hx-8, hy-11), (hx-1, hy-5)])
    pygame.draw.polygon(s, MASK_DARK,  [(hx+4, hy-4), (hx+8, hy-11), (hx+1, hy-5)])

    for y in range(hy - 5, hy + 6):
        for x in range(hx - 7, hx + 8):
            dx = x - hx; dy = y - hy
            if dx*dx/40 + dy*dy/25 <= 1.0:
                c = MASK_LIGHT if (x < hx + 1 and y < hy + 2) else MASK_DARK
                if 0 <= x < W and 0 <= y < H:
                    s.set_at((x, y), c)

    pygame.draw.ellipse(s, BLACK, (hx-4, hy-1, 3, 4))
    pygame.draw.ellipse(s, BLACK, (hx+1, hy-1, 3, 4))

    ny = 16 + breath
    if state == "attack":
        pygame.draw.line(s, NEEDLE_D, (hx,   ny),   (31, ny),   3)
        pygame.draw.line(s, NEEDLE_L, (hx,   ny-1), (31, ny-1), 1)
        pygame.draw.arc(s, (255, 255, 255, 220), (20, ny-7, 10, 14), -1.0, 1.0, 2)
    elif state == "run":
        pygame.draw.line(s, NEEDLE_D, (hx+2, ny+2), (hx-12, ny+8), 2)
        pygame.draw.line(s, NEEDLE_L, (hx+2, ny+1), (hx-12, ny+7), 1)
    elif state == "jump":
        pygame.draw.line(s, NEEDLE_D, (hx,   ny+2), (hx+2, ny+13), 2)
        pygame.draw.line(s, NEEDLE_L, (hx-1, ny+2), (hx+1, ny+13), 1)
    else:
        pygame.draw.line(s, NEEDLE_D, (6, ny-4), (26, ny+6), 2)
        pygame.draw.line(s, NEEDLE_L, (6, ny-5), (26, ny+5), 1)

    if state == "jump":
        pygame.draw.ellipse(s, WING, (0,  4, 14, 10))
        pygame.draw.ellipse(s, WING, (18, 4, 14, 10))

    return s


def draw_hurt():
    base = draw_hornet("idle", 0)
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 210))
    result = pygame.Surface((W, H), pygame.SRCALPHA)
    result.blit(base, (0, 0))
    result.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return result


os.makedirs("sprites", exist_ok=True)
pygame.image.save(draw_hornet("idle",   0), "sprites/hornet_idle_0.png")
pygame.image.save(draw_hornet("idle",   1), "sprites/hornet_idle_1.png")
pygame.image.save(draw_hornet("run",    0), "sprites/hornet_run_0.png")
pygame.image.save(draw_hornet("run",    1), "sprites/hornet_run_1.png")
pygame.image.save(draw_hornet("attack", 0), "sprites/hornet_attack_0.png")
pygame.image.save(draw_hornet("jump",   0), "sprites/hornet_jump_0.png")
pygame.image.save(draw_hurt(),              "sprites/hornet_hurt_0.png")
print("Done: idle x2, run x2, attack x1, jump x1, hurt x1")
