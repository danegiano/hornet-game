import pygame, os
pygame.init()
os.makedirs("sprites", exist_ok=True)
W, H = 32, 32

def fly_frame(wing_down=False, dive=False):
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    BLACK = (30, 30, 30, 255)
    GRAY  = (80, 80, 80, 255)
    RED   = (200, 40, 40, 255)
    WING  = (200, 240, 255, 150)

    if dive:
        pygame.draw.ellipse(s, WING, (2, 16, 8, 4))
        pygame.draw.ellipse(s, WING, (22, 16, 8, 4))
        pygame.draw.ellipse(s, BLACK, (10, 14, 12, 10))
        pygame.draw.ellipse(s, GRAY,  (12, 16, 8,  6))
        pygame.draw.circle(s, RED, (13, 19), 2)
        pygame.draw.circle(s, RED, (20, 19), 2)
    elif wing_down:
        pygame.draw.ellipse(s, WING, (4, 12, 12, 6))
        pygame.draw.ellipse(s, WING, (16, 12, 12, 6))
        pygame.draw.ellipse(s, BLACK, (10, 12, 12, 10))
        pygame.draw.ellipse(s, GRAY,  (12, 14, 8,  6))
        pygame.draw.circle(s, RED, (12, 16), 2)
        pygame.draw.circle(s, RED, (20, 16), 2)
    else:
        pygame.draw.ellipse(s, WING, (6, 4, 10, 10))
        pygame.draw.ellipse(s, WING, (16, 4, 10, 10))
        pygame.draw.ellipse(s, BLACK, (10, 12, 12, 10))
        pygame.draw.ellipse(s, GRAY,  (12, 14, 8,  6))
        pygame.draw.circle(s, RED, (12, 16), 2)
        pygame.draw.circle(s, RED, (20, 16), 2)
    return s

pygame.image.save(fly_frame(False),     "sprites/fly_black_0.png")
pygame.image.save(fly_frame(True),      "sprites/fly_black_1.png")
pygame.image.save(fly_frame(dive=True), "sprites/fly_black_2.png")


def spider_frame(walk=False, attack=False):
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    BROWN_D = (80,  50, 20, 255)
    BROWN_L = (120, 75, 30, 255)
    BLACK   = (20,  20, 20, 255)
    RED     = (255, 50, 50, 255)

    leg_offset = 2 if walk else 0

    if attack:
        pygame.draw.lines(s, BROWN_D, False, [(16, 22), (8, 8),  (2, 2)],   2)
        pygame.draw.lines(s, BROWN_D, False, [(16, 22), (24, 8), (30, 2)],  2)
        pygame.draw.lines(s, BROWN_D, False, [(16, 22), (8, 24), (2, 30)],  2)
        pygame.draw.lines(s, BROWN_D, False, [(16, 22), (24, 24),(30, 30)], 2)
    else:
        pygame.draw.lines(s, BROWN_D, False, [(16, 20), (10, 16-leg_offset), (4, 24+leg_offset)], 2)
        pygame.draw.lines(s, BROWN_D, False, [(16, 20), (8,  20+leg_offset), (2, 28-leg_offset)], 2)
        pygame.draw.lines(s, BROWN_D, False, [(16, 20), (12, 24-leg_offset), (6, 30+leg_offset)], 2)
        pygame.draw.lines(s, BROWN_D, False, [(16, 20), (22, 16+leg_offset), (28, 24-leg_offset)], 2)
        pygame.draw.lines(s, BROWN_D, False, [(16, 20), (24, 20-leg_offset), (30, 28+leg_offset)], 2)
        pygame.draw.lines(s, BROWN_D, False, [(16, 20), (20, 24+leg_offset), (26, 30-leg_offset)], 2)

    body_y = 22 if attack else 14
    pygame.draw.ellipse(s, BROWN_D, (10, body_y,     12, 12))
    pygame.draw.ellipse(s, BROWN_L, (12, body_y + 2, 8,  8))
    pygame.draw.ellipse(s, BROWN_D, (12, body_y - 4, 8,  8))

    eye_y = body_y - 1
    pygame.draw.circle(s, RED, (14, eye_y), 1)
    pygame.draw.circle(s, RED, (18, eye_y), 1)
    pygame.draw.circle(s, RED, (12, eye_y + 2), 1)
    pygame.draw.circle(s, RED, (20, eye_y + 2), 1)
    return s

pygame.image.save(spider_frame(False),       "sprites/spider_brown_0.png")
pygame.image.save(spider_frame(True),        "sprites/spider_brown_1.png")
pygame.image.save(spider_frame(attack=True), "sprites/spider_brown_2.png")
print("Fly and spider sprites done (3 frames each)!")
