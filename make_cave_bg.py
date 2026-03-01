"""Generate 3 parallax background layers for the Crystal Caves island."""
import pygame, os, math, random
pygame.init()
os.makedirs("sprites", exist_ok=True)
W, H = 800, 600

# Seed for consistent results
random.seed(99)

# Layer 1: Deep cave walls with stalactites (moves slow)
s1 = pygame.Surface((W, H), pygame.SRCALPHA)
# Dark cave gradient background
for y in range(H):
    depth = y / H
    r = int(15 + depth * 10)
    g = int(8 + depth * 5)
    b = int(35 + depth * 15)
    pygame.draw.line(s1, (r, g, b), (0, y), (W, y))
# Stalactites hanging from ceiling
for x in range(20, W, 60):
    stala_len = random.randint(60, 150)
    stala_w = random.randint(8, 18)
    # Draw as a triangle
    pts = [
        (x - stala_w // 2, 0),
        (x + stala_w // 2, 0),
        (x, stala_len),
    ]
    pygame.draw.polygon(s1, (40, 25, 70), pts)
    pygame.draw.polygon(s1, (50, 35, 85), pts, 2)
    # Crystal highlight on stalactite
    pygame.draw.line(s1, (80, 60, 130), (x - 2, 10), (x - 2, stala_len - 20), 1)
# Cave ceiling rocky edge
for x in range(0, W, 4):
    rock_h = random.randint(10, 30)
    pygame.draw.rect(s1, (25, 15, 50), (x, 0, 4, rock_h))
pygame.image.save(s1, "sprites/bg_cave_1.png")

# Layer 2: Crystal formations glowing in the mid-ground (moves medium)
s2 = pygame.Surface((W, H), pygame.SRCALPHA)
# Crystal clusters on the ground and walls
for x in range(40, W, 120):
    # Ground crystal cluster
    base_y = H - random.randint(20, 80)
    num_crystals = random.randint(3, 6)
    for i in range(num_crystals):
        cx = x + random.randint(-20, 20)
        crystal_h = random.randint(30, 70)
        crystal_w = random.randint(6, 14)
        # Crystal as a tall diamond
        pts = [
            (cx, base_y),
            (cx + crystal_w // 2, base_y - crystal_h),
            (cx + crystal_w, base_y),
        ]
        # Vary crystal colors: purple, blue, or pink
        colors = [
            (100, 50, 180), (60, 60, 200), (150, 50, 150),
            (80, 40, 160), (90, 70, 200),
        ]
        c = random.choice(colors)
        pygame.draw.polygon(s2, c, pts)
        # Glow highlight
        pygame.draw.line(s2, (min(255, c[0] + 80), min(255, c[1] + 80), min(255, c[2] + 60)),
                         (cx + crystal_w // 2 - 1, base_y - crystal_h + 5),
                         (cx + crystal_w // 2 - 1, base_y - 10), 1)

# Wall crystals (on the sides)
for y in range(50, H - 100, 80):
    # Left wall crystal
    cw = random.randint(15, 35)
    ch = random.randint(8, 15)
    pts = [(0, y), (cw, y + ch // 2), (0, y + ch)]
    pygame.draw.polygon(s2, (100, 60, 180), pts)
    pygame.draw.polygon(s2, (140, 100, 220), pts, 1)
    # Right wall crystal
    cw2 = random.randint(15, 35)
    ch2 = random.randint(8, 15)
    ry = y + random.randint(-20, 20)
    pts2 = [(W, ry), (W - cw2, ry + ch2 // 2), (W, ry + ch2)]
    pygame.draw.polygon(s2, (80, 50, 160), pts2)
    pygame.draw.polygon(s2, (120, 80, 200), pts2, 1)

# Dim glowing spots (like bioluminescence)
for _ in range(15):
    gx = random.randint(50, W - 50)
    gy = random.randint(100, H - 50)
    gr = random.randint(3, 8)
    gc = random.choice([(100, 80, 200, 80), (80, 60, 180, 60), (120, 100, 220, 70)])
    pygame.draw.circle(s2, gc, (gx, gy), gr)
    pygame.draw.circle(s2, (gc[0] + 40, gc[1] + 40, min(255, gc[2] + 40), 40), (gx, gy), gr + 4)
pygame.image.save(s2, "sprites/bg_cave_2.png")

# Layer 3: Near rocks and stalagmites (moves fastest)
s3 = pygame.Surface((W, H), pygame.SRCALPHA)
# Stalagmites rising from the ground
for x in range(15, W, 45):
    stag_h = random.randint(40, 120)
    stag_w = random.randint(10, 22)
    base_y = H - 20
    pts = [
        (x - stag_w // 2, base_y),
        (x, base_y - stag_h),
        (x + stag_w // 2, base_y),
    ]
    pygame.draw.polygon(s3, (35, 20, 60), pts)
    pygame.draw.polygon(s3, (50, 30, 80), pts, 2)
    # Highlight line
    pygame.draw.line(s3, (60, 40, 100),
                     (x + 2, base_y - stag_h + 10),
                     (x + 2, base_y - 5), 1)

# Rocky ground at bottom
for y in range(H - 25, H):
    depth = (y - (H - 25)) / 25
    c = (int(20 + depth * 15), int(12 + depth * 8), int(40 + depth * 20))
    pygame.draw.line(s3, c, (0, y), (W, y))

# A few loose rocks scattered on the ground
for x in range(30, W, 70):
    rock_w = random.randint(12, 25)
    rock_h = random.randint(8, 15)
    rock_y = H - 25 - rock_h // 2 + random.randint(-3, 3)
    pygame.draw.ellipse(s3, (30, 18, 55), (x, rock_y, rock_w, rock_h))
    pygame.draw.ellipse(s3, (40, 25, 70), (x, rock_y, rock_w, rock_h), 1)

# Ceiling rocks hanging down (near layer)
for x in range(25, W, 80):
    rock_h = random.randint(15, 40)
    rock_w = random.randint(12, 25)
    pygame.draw.polygon(s3, (30, 18, 55), [
        (x - rock_w // 2, 0), (x + rock_w // 2, 0), (x, rock_h)
    ])
pygame.image.save(s3, "sprites/bg_cave_3.png")

print("Cave backgrounds generated!")
