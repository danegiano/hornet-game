import pygame, math, os
pygame.init()
W,H = 32,32

def draw_hornet(state, frame):
    s = pygame.Surface((W,H), pygame.SRCALPHA)
    
    CLOAK_LIGHT = (220, 50, 60, 255)
    CLOAK_MID = (180, 30, 40, 255)
    CLOAK_DARK = (110, 15, 25, 255)
    MASK_LIGHT = (255, 255, 255, 255)
    MASK_DARK = (200, 200, 210, 255)
    BLACK = (20, 20, 20, 255)
    NEEDLE_LIGHT = (220, 220, 220, 255)
    NEEDLE_DARK = (100, 100, 100, 255)

    breath = 1 if (state == "idle" and frame == 1) else 0
    leg_shift = 0
    if state == "run":
        leg_shift = 3 if frame == 0 else -3
        breath = 1 if frame == 0 else 0
    
    atk_ext = 0
    if state == "attack":
        breath = 0
        leg_shift = 2

    # Shadow
    pygame.draw.ellipse(s, (0,0,0,80), (10, 28, 12, 4))

    # Cloak
    for y in range(15+breath, 29):
        width = 4 + int((y - 15) * 1.2)
        if state == "run":
            width -= 2
        tilt = 0
        if state == "run":
            tilt = int((y - 15) * 0.2)
            
        left = 16 - width//2 - tilt
        right = 16 + width//2 - tilt
        
        for x in range(left, right+1):
            color = CLOAK_MID
            if x < left + width//3:
                color = CLOAK_LIGHT
            elif x > right - width//3:
                color = CLOAK_DARK
            
            if (x - left) % 4 == 0 and x > left and x < right:
                color = CLOAK_DARK
                
            s.set_at((x, y), color)

    # Legs
    pygame.draw.line(s, BLACK, (14, 28), (14-leg_shift, 31), 2)
    pygame.draw.line(s, BLACK, (18, 28), (18+leg_shift, 31), 2)

    # Mask
    hx, hy = 16, 12 + breath
    
    # Horns
    pygame.draw.polygon(s, MASK_LIGHT, [(hx-4, hy-4), (hx-8, hy-11), (hx-1, hy-5)])
    pygame.draw.polygon(s, MASK_DARK, [(hx+4, hy-4), (hx+8, hy-11), (hx+1, hy-5)])

    for y in range(hy - 5, hy + 6):
        for x in range(hx - 7, hx + 8):
            dx = (x - hx)
            dy = (y - hy)
            if dx*dx/40 + dy*dy/25 <= 1.0:
                if x < hx + 1 and y < hy + 2:
                    color = MASK_LIGHT
                else:
                    color = MASK_DARK
                s.set_at((x,y), color)

    # Eyes
    pygame.draw.ellipse(s, BLACK, (hx-4, hy-1, 3, 4))
    pygame.draw.ellipse(s, BLACK, (hx+1, hy-1, 3, 4))

    # Needle
    ny = 16 + breath
    if state == "attack":
        pygame.draw.line(s, NEEDLE_DARK, (16, ny+2), (31, ny+2), 3)
        pygame.draw.line(s, NEEDLE_LIGHT, (16, ny+1), (31, ny+1), 1)
        pygame.draw.arc(s, (255,255,255,200), (14, ny-8, 16, 16), -1.2, 1.2, 2)
    else:
        pygame.draw.line(s, NEEDLE_DARK, (6, ny-4), (26, ny+6), 2)
        pygame.draw.line(s, NEEDLE_LIGHT, (6, ny-5), (26, ny+5), 1)

    return s

pygame.image.save(draw_hornet("idle", 0), "sprites/hornet_idle_0.png")
pygame.image.save(draw_hornet("idle", 1), "sprites/hornet_idle_1.png")
pygame.image.save(draw_hornet("run", 0), "sprites/hornet_run_0.png")
pygame.image.save(draw_hornet("run", 1), "sprites/hornet_run_1.png")
pygame.image.save(draw_hornet("attack", 0), "sprites/hornet_attack_0.png")

print("Hornet redesigned!")
