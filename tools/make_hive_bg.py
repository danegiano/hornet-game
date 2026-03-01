import pygame, os, math
pygame.init()
os.makedirs("sprites", exist_ok=True)
W,H = 800,600

# Level 2 (The Hive) Backgrounds

# Layer 1: Distant Amber Cave Wall (moves slow)
s1 = pygame.Surface((W,H), pygame.SRCALPHA)
pygame.draw.rect(s1, (110, 80, 20), (0, 0, W, H)) # Dark amber base
# Hexagon pattern (faded)
hex_w = 120
hex_h = 100
for y in range(-50, H+50, hex_h):
    for x in range(-50, W+100, hex_w):
        offset = (y // hex_h) % 2 * (hex_w // 2)
        cx = x + offset
        cy = y
        pts = [(cx, cy-40), (cx+50, cy-20), (cx+50, cy+20), (cx, cy+40), (cx-50, cy+20), (cx-50, cy-20)]
        pygame.draw.polygon(s1, (90, 60, 10), pts, 4)
pygame.image.save(s1, "sprites/bg_hive_1.png")

# Layer 2: Hanging Honeycombs & Pillars (moves medium)
s2 = pygame.Surface((W,H), pygame.SRCALPHA)
# Pillars
for px in range(100, W+200, 300):
    pygame.draw.rect(s2, (150, 110, 30), (px, 0, 80, H))
    pygame.draw.rect(s2, (120, 80, 20), (px+50, 0, 30, H)) # shadow
# Honeycombs hanging from ceiling
for hx in range(50, W+150, 200):
    drop_h = 150 + int(math.sin(hx)*50)
    pygame.draw.polygon(s2, (200, 150, 40), [(hx, 0), (hx+120, 0), (hx+60, drop_h)])
    pygame.draw.polygon(s2, (160, 110, 20), [(hx+60, 0), (hx+120, 0), (hx+60, drop_h)])
pygame.image.save(s2, "sprites/bg_hive_2.png")

# Layer 3: Foreground Dripping Honey & Wax (moves fast)
s3 = pygame.Surface((W,H), pygame.SRCALPHA)
for bx in range(0, W+200, 150):
    # Wax mounds at bottom
    mound_y = 500 + int(math.cos(bx)*30)
    pygame.draw.ellipse(s3, (220, 170, 50), (bx, mound_y, 200, 150))
    pygame.draw.ellipse(s3, (255, 200, 80), (bx+20, mound_y+10, 160, 80)) # highlight
pygame.image.save(s3, "sprites/bg_hive_3.png")

print("Hive backgrounds generated!")
