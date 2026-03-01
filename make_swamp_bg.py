"""Generate 3 parallax background layers for the Swamp island."""
import pygame, os, math, random
pygame.init()
os.makedirs("sprites", exist_ok=True)
W, H = 800, 600

# Seed for consistent results
random.seed(42)

# Layer 1: Murky fog / distant swamp trees (moves slow)
s1 = pygame.Surface((W, H), pygame.SRCALPHA)
# Fog bands
for y in range(0, H, 40):
    alpha = max(0, min(80, 80 - y // 8))
    fog_color = (60, 80, 50, alpha)
    pygame.draw.rect(s1, fog_color, (0, y, W, 40))
# Distant dead tree silhouettes
for x in range(50, W, 200):
    trunk_h = random.randint(200, 350)
    trunk_y = H - trunk_h
    # Trunk
    pygame.draw.rect(s1, (30, 40, 25), (x, trunk_y, 12, trunk_h))
    # Bare branches
    for bh in range(trunk_y + 30, trunk_y + trunk_h // 2, 50):
        branch_len = random.randint(30, 60)
        side = random.choice([-1, 1])
        pygame.draw.line(s1, (35, 45, 30),
                         (x + 6, bh), (x + 6 + side * branch_len, bh - 20), 3)
        # Sub-branch
        pygame.draw.line(s1, (35, 45, 30),
                         (x + 6 + side * branch_len, bh - 20),
                         (x + 6 + side * (branch_len + 15), bh - 35), 2)
pygame.image.save(s1, "sprites/bg_swamp_1.png")

# Layer 2: Mid-ground dead trees with hanging vines (moves medium)
s2 = pygame.Surface((W, H), pygame.SRCALPHA)
for x in range(30, W, 150):
    trunk_h = random.randint(250, 400)
    trunk_y = H - trunk_h
    # Thicker trunk
    pygame.draw.rect(s2, (40, 50, 30), (x - 3, trunk_y, 18, trunk_h))
    # Knots on trunk
    for ky in range(trunk_y + 50, trunk_y + trunk_h - 50, 80):
        pygame.draw.ellipse(s2, (50, 60, 35), (x, ky, 12, 8))
    # Branches with hanging vines
    for bh in range(trunk_y + 20, trunk_y + trunk_h // 3, 60):
        branch_len = random.randint(40, 80)
        side = random.choice([-1, 1])
        bx_end = x + 6 + side * branch_len
        pygame.draw.line(s2, (45, 55, 35), (x + 6, bh), (bx_end, bh - 15), 4)
        # Hanging vines from the branch
        for vx in range(min(x + 6, bx_end) + 10, max(x + 6, bx_end), 20):
            vine_len = random.randint(30, 80)
            for vy in range(0, vine_len, 5):
                sway = int(math.sin(vy / 15.0 + vx) * 3)
                pygame.draw.line(s2, (30, 90, 30),
                                 (vx + sway, bh - 15 + vy),
                                 (vx + sway, bh - 15 + vy + 5), 2)
# Swamp water at bottom
for y in range(H - 60, H):
    depth = (y - (H - 60)) / 60
    c = (int(20 + depth * 10), int(50 + depth * 10), int(30 - depth * 10))
    pygame.draw.line(s2, c, (0, y), (W, y))
pygame.image.save(s2, "sprites/bg_swamp_2.png")

# Layer 3: Foreground reeds and lily pads (moves fastest)
s3 = pygame.Surface((W, H), pygame.SRCALPHA)
# Reeds
for x in range(10, W, 25):
    reed_h = random.randint(40, 100)
    sway = int(math.sin(x / 30.0) * 5)
    base_y = H - 40
    # Reed stalk
    pygame.draw.line(s3, (40, 110, 40),
                     (x, base_y), (x + sway, base_y - reed_h), 3)
    # Reed top tuft
    pygame.draw.ellipse(s3, (60, 80, 40),
                        (x + sway - 4, base_y - reed_h - 8, 8, 12))
# Lily pads at the water line
for x in range(40, W, 130):
    pad_w = random.randint(25, 40)
    pad_y = H - 30 + random.randint(-5, 5)
    pygame.draw.ellipse(s3, (30, 100, 40), (x, pad_y, pad_w, 12))
    # Flower on some pads
    if random.random() > 0.5:
        pygame.draw.circle(s3, (180, 120, 180), (x + pad_w // 2, pad_y - 3), 5)
        pygame.draw.circle(s3, (200, 150, 200), (x + pad_w // 2, pad_y - 3), 3)
# Murky water at bottom
for y in range(H - 45, H):
    alpha = min(200, 100 + (y - (H - 45)) * 5)
    pygame.draw.line(s3, (15, 40, 25, alpha), (0, y), (W, y))
pygame.image.save(s3, "sprites/bg_swamp_3.png")

print("Swamp backgrounds generated!")
