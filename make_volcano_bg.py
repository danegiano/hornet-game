"""Generate 3 parallax background layers for the Volcano island."""
import pygame, os, math, random
pygame.init()
os.makedirs("sprites", exist_ok=True)
W, H = 800, 600

# Seed for consistent results
random.seed(42)

# Layer 1: Distant volcanic mountains, red sky (moves slow)
s1 = pygame.Surface((W, H), pygame.SRCALPHA)
# Red/dark sky gradient
for y in range(H):
    depth = y / H
    r = int(80 - depth * 40)
    g = int(20 - depth * 15)
    b = int(8 - depth * 5)
    pygame.draw.line(s1, (max(0, r), max(0, g), max(0, b)), (0, y), (W, y))
# Distant volcanic mountains
mountains = [
    (0, 250, 120, 120),
    (100, 200, 200, 180),
    (280, 230, 150, 150),
    (420, 180, 220, 200),
    (600, 220, 180, 160),
    (720, 240, 120, 140),
]
for mx, my, mw, mh in mountains:
    pts = [
        (mx, H),
        (mx + mw // 2, my),
        (mx + mw, H),
    ]
    pygame.draw.polygon(s1, (50, 20, 10), pts)
    pygame.draw.polygon(s1, (60, 25, 12), pts, 2)
    # Crater glow on top of some mountains
    if random.random() > 0.5:
        pygame.draw.circle(s1, (200, 60, 10), (mx + mw // 2, my + 5), 8)
        pygame.draw.circle(s1, (255, 100, 20), (mx + mw // 2, my + 5), 4)
# Hazy smoke at the top
for x in range(0, W, 3):
    smoke_h = random.randint(30, 60)
    smoke_alpha = random.randint(20, 50)
    pygame.draw.rect(s1, (100, 50, 30, smoke_alpha), (x, 0, 3, smoke_h))
pygame.image.save(s1, "sprites/bg_volcano_1.png")

# Layer 2: Lava rivers and rocky formations (moves medium)
s2 = pygame.Surface((W, H), pygame.SRCALPHA)
# Rocky formations in the mid-ground
for x in range(30, W, 100):
    rock_h = random.randint(80, 200)
    rock_w = random.randint(30, 60)
    base_y = H - random.randint(10, 40)
    pts = [
        (x - rock_w // 2, base_y),
        (x - rock_w // 4, base_y - rock_h),
        (x + rock_w // 4, base_y - rock_h + random.randint(-10, 10)),
        (x + rock_w // 2, base_y),
    ]
    pygame.draw.polygon(s2, (60, 30, 15), pts)
    pygame.draw.polygon(s2, (80, 40, 20), pts, 2)

# Lava rivers (glowing orange streams on the ground)
lava_y = H - 30
for x in range(0, W, 5):
    wave = math.sin(x / 40.0) * 8
    lava_h = 12 + int(wave)
    pygame.draw.rect(s2, (200, 60, 0), (x, lava_y + int(wave), 5, lava_h))
    # Bright center of lava
    pygame.draw.rect(s2, (255, 140, 20), (x + 1, lava_y + int(wave) + 3, 3, lava_h - 6))

# Scattered embers (small glowing dots)
for _ in range(25):
    ex = random.randint(20, W - 20)
    ey = random.randint(100, H - 60)
    er = random.randint(1, 3)
    pygame.draw.circle(s2, (255, 150, 0, 150), (ex, ey), er)
    pygame.draw.circle(s2, (255, 220, 50, 80), (ex, ey), er + 2)
pygame.image.save(s2, "sprites/bg_volcano_2.png")

# Layer 3: Near volcanic rocks, steam vents, embers (moves fastest)
s3 = pygame.Surface((W, H), pygame.SRCALPHA)
# Jagged volcanic rocks rising from ground
for x in range(10, W, 50):
    rock_h = random.randint(30, 100)
    rock_w = random.randint(15, 30)
    base_y = H - 15
    pts = [
        (x - rock_w // 2, base_y),
        (x - rock_w // 3, base_y - rock_h),
        (x + rock_w // 4, base_y - rock_h + random.randint(5, 15)),
        (x + rock_w // 2, base_y),
    ]
    pygame.draw.polygon(s3, (45, 22, 10), pts)
    pygame.draw.polygon(s3, (70, 35, 18), pts, 2)
    # Lava crack on rock
    crack_y = base_y - rock_h // 2
    pygame.draw.line(s3, (200, 60, 0), (x - 3, crack_y), (x + 5, crack_y + 8), 2)

# Steam vents (white/gray wisps rising up)
for x in range(60, W, 130):
    vent_x = x + random.randint(-10, 10)
    # Draw vent base
    pygame.draw.rect(s3, (60, 30, 15), (vent_x - 5, H - 20, 10, 20))
    # Steam wisps
    for i in range(5):
        sy = H - 25 - i * 15
        sw = 4 + i * 2
        steam_alpha = max(10, 80 - i * 15)
        pygame.draw.circle(s3, (180, 180, 180, steam_alpha),
                           (vent_x + random.randint(-5, 5), sy), sw)

# Rocky ground at bottom
for y in range(H - 18, H):
    depth = (y - (H - 18)) / 18
    c = (int(40 + depth * 20), int(18 + depth * 10), int(8 + depth * 5))
    pygame.draw.line(s3, c, (0, y), (W, y))

# Ceiling rocks (volcanic cave ceiling)
for x in range(20, W, 70):
    rock_h = random.randint(15, 45)
    rock_w = random.randint(15, 30)
    pygame.draw.polygon(s3, (40, 20, 8), [
        (x - rock_w // 2, 0), (x + rock_w // 2, 0), (x, rock_h)
    ])
    # Dripping lava from some ceiling rocks
    if random.random() > 0.6:
        pygame.draw.line(s3, (200, 60, 0), (x, rock_h), (x, rock_h + 10), 2)
        pygame.draw.circle(s3, (255, 100, 0), (x, rock_h + 12), 3)
pygame.image.save(s3, "sprites/bg_volcano_3.png")

print("Volcano backgrounds generated!")
