import pygame, os, math
pygame.init()
os.makedirs("sprites", exist_ok=True)
W,H = 800,600

# Layer 1: Distant Mountains (moves slow)
s1 = pygame.Surface((W,H), pygame.SRCALPHA)
pygame.draw.polygon(s1, (90, 130, 160), [(0, 600), (150, 300), (400, 600)])
pygame.draw.polygon(s1, (70, 110, 140), [(250, 600), (450, 200), (700, 600)])
pygame.draw.polygon(s1, (80, 120, 150), [(550, 600), (750, 280), (900, 600)])
# Tile the first mountain to make it seamless
pygame.draw.polygon(s1, (90, 130, 160), [(800, 600), (950, 300), (1200, 600)])
pygame.image.save(s1, "sprites/bg_garden_1.png")

# Layer 2: Pine Trees (moves medium)
s2 = pygame.Surface((W,H), pygame.SRCALPHA)
for x in range(20, 800, 120):
    pygame.draw.rect(s2, (50, 30, 20), (x, 350, 20, 250)) # Trunk
    pygame.draw.polygon(s2, (30, 80, 40), [(x-40, 450), (x+10, 250), (x+60, 450)]) # Leaves
    pygame.draw.polygon(s2, (40, 90, 50), [(x-30, 350), (x+10, 180), (x+50, 350)])
pygame.image.save(s2, "sprites/bg_garden_2.png")

# Layer 3: Foreground Bushes (moves fastest)
s3 = pygame.Surface((W,H), pygame.SRCALPHA)
for x in range(0, 800, 90):
    y_off = int(math.sin(x)*10)
    pygame.draw.circle(s3, (20, 60, 30), (x, 550 + y_off), 80)
    pygame.draw.circle(s3, (30, 70, 40), (x+45, 530 - y_off), 60)
pygame.image.save(s3, "sprites/bg_garden_3.png")

print("Garden backgrounds generated!")
