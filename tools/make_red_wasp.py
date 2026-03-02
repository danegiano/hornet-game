import pygame, os
pygame.init()
os.makedirs("sprites", exist_ok=True)
W, H = 32, 32

def wasp_frame(wing_up=False, attack=False):
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    RED_L = (240, 60,  60,  255)
    RED_D = (180, 20,  20,  255)
    BLACK = (20,  20,  20,  255)
    GRAY  = (60,  60,  60,  255)
    EYE   = (255, 200, 0,   255)
    WING  = (255, 200, 200, 150)

    if attack:
        pygame.draw.ellipse(s, WING, (2, 10, 8, 5))
        pygame.draw.ellipse(s, WING, (18, 8, 8, 5))
        pygame.draw.ellipse(s, RED_D, (4,  13, 18, 12))
        pygame.draw.ellipse(s, RED_L, (5,  14, 16, 10))
        for x in range(7, 20, 3):
            pygame.draw.line(s, GRAY, (x, 15), (x, 24), 2)
        pygame.draw.ellipse(s, RED_D, (2,  10, 10, 8))
        pygame.draw.ellipse(s, RED_L, (3,  11, 8,  6))
        pygame.draw.circle(s, EYE, (6,  14), 1)
        pygame.draw.circle(s, EYE, (10, 14), 1)
        pygame.draw.polygon(s, BLACK, [(22, 17), (31, 15), (31, 19)])
        pygame.draw.line(s, GRAY, (22, 17), (31, 17), 1)
    else:
        if wing_up:
            pygame.draw.ellipse(s, WING, (6, 6,  10, 6))
            pygame.draw.ellipse(s, WING, (16, 6, 10, 6))
        else:
            pygame.draw.ellipse(s, WING, (5, 9,  12, 7))
            pygame.draw.ellipse(s, WING, (15, 9, 12, 7))
        pygame.draw.ellipse(s, RED_D, (8,  12, 16, 12))
        pygame.draw.ellipse(s, RED_L, (9,  13, 14, 10))
        for x in range(11, 21, 3):
            pygame.draw.line(s, GRAY, (x, 14), (x, 23), 2)
        pygame.draw.ellipse(s, RED_D, (9,  9, 10, 8))
        pygame.draw.ellipse(s, RED_L, (10, 10, 8,  6))
        pygame.draw.circle(s, EYE, (13, 13), 1)
        pygame.draw.circle(s, EYE, (17, 13), 1)
        pygame.draw.polygon(s, BLACK, [(24, 18), (31, 16), (31, 20)])

    return s

pygame.image.save(wasp_frame(False),       "sprites/wasp_red_0.png")
pygame.image.save(wasp_frame(True),        "sprites/wasp_red_1.png")
pygame.image.save(wasp_frame(attack=True), "sprites/wasp_red_2.png")
print("Red wasp done (3 frames)!")
