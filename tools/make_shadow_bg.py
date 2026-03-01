"""Generate 3 parallax background layers for the Shadow Fortress island."""
import pygame, os, math, random
pygame.init()
os.makedirs("sprites", exist_ok=True)
W, H = 800, 600

# Seed for consistent results
random.seed(55)

# Layer 1: Dark fortress walls with towers, purple sky (moves slow)
s1 = pygame.Surface((W, H), pygame.SRCALPHA)
# Dark purple sky gradient
for y in range(H):
    depth = y / H
    r = int(20 - depth * 15)
    g = int(8 - depth * 6)
    b = int(35 - depth * 20)
    pygame.draw.line(s1, (max(0, r), max(0, g), max(0, b)), (0, y), (W, y))

# Distant fortress towers
towers = [
    (30, 180, 50, 300),
    (150, 140, 60, 340),
    (300, 200, 45, 280),
    (420, 120, 70, 360),
    (560, 160, 55, 320),
    (680, 190, 50, 290),
    (760, 150, 40, 330),
]
for tx, ty, tw, th in towers:
    # Tower body
    pygame.draw.rect(s1, (25, 12, 35), (tx, ty, tw, th))
    pygame.draw.rect(s1, (35, 18, 48), (tx, ty, tw, th), 2)
    # Battlements on top
    for bx in range(tx, tx + tw, 12):
        pygame.draw.rect(s1, (30, 15, 42), (bx, ty - 10, 8, 10))
    # Glowing purple window
    win_y = ty + th // 3
    pygame.draw.rect(s1, (100, 40, 150), (tx + tw // 2 - 4, win_y, 8, 12))
    pygame.draw.rect(s1, (150, 80, 200), (tx + tw // 2 - 2, win_y + 2, 4, 8))

# Dark clouds/fog at top
for x in range(0, W, 4):
    fog_h = random.randint(20, 50)
    fog_alpha = random.randint(15, 40)
    pygame.draw.rect(s1, (30, 10, 50, fog_alpha), (x, 0, 4, fog_h))

# Faint purple aurora streaks in the sky
for i in range(5):
    ax = random.randint(50, W - 50)
    ay = random.randint(20, 100)
    aw = random.randint(60, 150)
    pygame.draw.line(s1, (60, 20, 90, 40), (ax, ay), (ax + aw, ay + random.randint(-20, 20)), 2)

pygame.image.save(s1, "sprites/bg_shadow_1.png")

# Layer 2: Pillars and archways, floating shadow particles (moves medium)
s2 = pygame.Surface((W, H), pygame.SRCALPHA)

# Stone pillars
for x in range(40, W, 120):
    pillar_h = random.randint(150, 350)
    pillar_w = random.randint(20, 35)
    base_y = H - random.randint(10, 30)
    # Pillar body
    pygame.draw.rect(s2, (35, 18, 50), (x - pillar_w // 2, base_y - pillar_h, pillar_w, pillar_h))
    pygame.draw.rect(s2, (45, 25, 65), (x - pillar_w // 2, base_y - pillar_h, pillar_w, pillar_h), 2)
    # Pillar cap
    pygame.draw.rect(s2, (40, 22, 58), (x - pillar_w // 2 - 5, base_y - pillar_h - 8, pillar_w + 10, 8))
    # Purple glowing rune on pillar
    rune_y = base_y - pillar_h // 2
    pygame.draw.circle(s2, (80, 30, 120), (x, rune_y), 5)
    pygame.draw.circle(s2, (130, 60, 180), (x, rune_y), 3)

# Archways between some pillars
for x in range(100, W, 240):
    arch_w = 80
    arch_h = 40
    arch_y = H - 200
    # Arch curve (simplified as lines)
    pts = [
        (x, arch_y + arch_h),
        (x + arch_w // 4, arch_y),
        (x + arch_w * 3 // 4, arch_y),
        (x + arch_w, arch_y + arch_h),
    ]
    pygame.draw.lines(s2, (45, 25, 65), False, pts, 3)

# Floating shadow particles
for _ in range(30):
    px = random.randint(10, W - 10)
    py = random.randint(80, H - 60)
    pr = random.randint(2, 5)
    pygame.draw.circle(s2, (60, 20, 90, 80), (px, py), pr)
    pygame.draw.circle(s2, (90, 40, 130, 40), (px, py), pr + 2)

pygame.image.save(s2, "sprites/bg_shadow_2.png")

# Layer 3: Near walls with cracks, purple torches, shadow tendrils (moves fastest)
s3 = pygame.Surface((W, H), pygame.SRCALPHA)

# Wall sections rising from ground
for x in range(15, W, 55):
    wall_h = random.randint(40, 120)
    wall_w = random.randint(18, 35)
    base_y = H - 15
    pygame.draw.rect(s3, (30, 15, 42), (x - wall_w // 2, base_y - wall_h, wall_w, wall_h))
    pygame.draw.rect(s3, (42, 22, 58), (x - wall_w // 2, base_y - wall_h, wall_w, wall_h), 2)
    # Cracks in the wall
    crack_y = base_y - wall_h // 2
    pygame.draw.line(s3, (60, 25, 80), (x - 5, crack_y), (x + 8, crack_y + 10), 2)
    # Purple glowing crack
    pygame.draw.line(s3, (100, 40, 150), (x - 3, crack_y + 1), (x + 6, crack_y + 9), 1)

# Purple torches along the walls
for x in range(50, W, 100):
    torch_x = x + random.randint(-10, 10)
    torch_y = H - random.randint(60, 120)
    # Torch bracket
    pygame.draw.rect(s3, (40, 20, 55), (torch_x - 3, torch_y, 6, 15))
    # Purple flame
    flame_pts = [
        (torch_x - 5, torch_y),
        (torch_x, torch_y - 14),
        (torch_x + 5, torch_y),
    ]
    pygame.draw.polygon(s3, (120, 40, 180), flame_pts)
    pygame.draw.polygon(s3, (180, 80, 255), flame_pts, 1)
    # Inner bright core
    pygame.draw.circle(s3, (200, 120, 255), (torch_x, torch_y - 6), 3)

# Shadow tendrils (dark wispy lines reaching up from ground)
for x in range(30, W, 70):
    tendril_x = x + random.randint(-15, 15)
    tendril_h = random.randint(30, 80)
    for i in range(tendril_h):
        sway = int(math.sin(i / 10.0) * 5)
        alpha = max(10, 80 - i)
        pygame.draw.rect(s3, (20, 5, 35, alpha),
                         (tendril_x + sway, H - 20 - i, 3, 1))

# Ground edge
for y in range(H - 18, H):
    depth = (y - (H - 18)) / 18
    c = (int(25 + depth * 15), int(10 + depth * 8), int(38 + depth * 12))
    pygame.draw.line(s3, c, (0, y), (W, y))

# Ceiling stalactites (dark stone hanging from top)
for x in range(25, W, 60):
    rock_h = random.randint(15, 50)
    rock_w = random.randint(10, 25)
    pygame.draw.polygon(s3, (22, 10, 32), [
        (x - rock_w // 2, 0), (x + rock_w // 2, 0), (x, rock_h)
    ])
    # Purple drip
    if random.random() > 0.5:
        pygame.draw.line(s3, (80, 30, 120), (x, rock_h), (x, rock_h + 8), 2)
        pygame.draw.circle(s3, (120, 50, 170), (x, rock_h + 10), 2)

pygame.image.save(s3, "sprites/bg_shadow_3.png")

print("Shadow fortress backgrounds generated!")
