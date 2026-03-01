import pygame, os, math
pygame.init()
os.makedirs("sprites", exist_ok=True)
W,H = 800,600

# Level 3 (The Throne Room / Tower) Backgrounds

# Layer 1: Dark crimson castle wall with giant windows
s1 = pygame.Surface((W,H), pygame.SRCALPHA)
pygame.draw.rect(s1, (60, 20, 20), (0, 0, W, H)) # Dark red background
for x in range(100, W+200, 400):
    # Giant arched window
    pygame.draw.rect(s1, (30, 10, 10), (x, 100, 150, 400))
    pygame.draw.ellipse(s1, (30, 10, 10), (x, 20, 150, 160))
    # Window bars
    pygame.draw.line(s1, (10, 5, 5), (x+75, 20), (x+75, 500), 5)
    for y in range(150, 500, 100):
        pygame.draw.line(s1, (10, 5, 5), (x, y), (x+150, y), 5)
pygame.image.save(s1, "sprites/bg_tower_1.png")

# Layer 2: Massive Stone Pillars & Chains
s2 = pygame.Surface((W,H), pygame.SRCALPHA)
for px in range(50, W+200, 500):
    # Pillar
    pygame.draw.rect(s2, (50, 50, 50), (px, 0, 120, H))
    pygame.draw.rect(s2, (30, 30, 30), (px+80, 0, 40, H)) # Shadow
    # Pillar details (cracks/bricks)
    for y in range(0, H, 80):
        pygame.draw.line(s2, (20, 20, 20), (px, y), (px+120, y), 3)
# Hanging Chains
for cx in range(250, W+100, 300):
    for cy in range(0, 350, 20):
        pygame.draw.ellipse(s2, (70, 70, 70), (cx, cy, 10, 25), 3)
pygame.image.save(s2, "sprites/bg_tower_2.png")

# Layer 3: Foreground Red Fog / Glow
s3 = pygame.Surface((W,H), pygame.SRCALPHA)
for x in range(0, W+200, 200):
    for offset in range(3):
        fog_y = 500 + int(math.cos(x + offset*50)*40)
        pygame.draw.ellipse(s3, (150, 40, 20, 60), (x - 100, fog_y, 400, 200))
        pygame.draw.ellipse(s3, (200, 80, 20, 40), (x, fog_y + 50, 200, 150))
pygame.image.save(s3, "sprites/bg_tower_3.png")

print("Tower backgrounds generated!")
