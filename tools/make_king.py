import pygame, os
pygame.init()
os.makedirs("sprites", exist_ok=True)
W,H = 120,90

def draw_king(flap=False):
    s = pygame.Surface((W,H), pygame.SRCALPHA)
    Y1 = (255, 220, 0, 255)
    Y2 = (200, 160, 0, 255)
    BLACK = (20, 20, 20, 255)
    RED = (255, 50, 50, 255)
    WING = (200, 230, 255, 180)
    GOLD = (255, 200, 0, 255)

    if flap:
        pygame.draw.ellipse(s, WING, (10, 5, 40, 70))
        pygame.draw.ellipse(s, WING, (70, 5, 40, 70))
    else:
        pygame.draw.ellipse(s, WING, (0, 30, 60, 30))
        pygame.draw.ellipse(s, WING, (60, 30, 60, 30))

    pygame.draw.polygon(s, BLACK, [(55, 75), (65, 75), (60, 90)])

    pygame.draw.ellipse(s, Y2, (30, 30, 60, 50))
    pygame.draw.ellipse(s, Y1, (35, 35, 50, 40))
    
    pygame.draw.line(s, BLACK, (35, 45), (85, 45), 6)
    pygame.draw.line(s, BLACK, (32, 55), (88, 55), 6)
    pygame.draw.line(s, BLACK, (35, 65), (85, 65), 6)

    pygame.draw.ellipse(s, BLACK, (40, 20, 40, 30))
    pygame.draw.ellipse(s, Y2, (45, 25, 30, 20))

    pygame.draw.polygon(s, RED, [(48, 25), (55, 30), (50, 35)])
    pygame.draw.polygon(s, RED, [(72, 25), (65, 30), (70, 35)])

    pygame.draw.polygon(s, GOLD, [(45, 20), (40, 5), (50, 15), (60, 5), (70, 15), (80, 5), (75, 20)])
    
    pygame.draw.lines(s, BLACK, False, [(50, 45), (45, 55), (55, 60)], 3)
    pygame.draw.lines(s, BLACK, False, [(70, 45), (75, 55), (65, 60)], 3)

    return s

pygame.image.save(draw_king(False), "sprites/king_0.png")
pygame.image.save(draw_king(True), "sprites/king_1.png")
print("Wasp King generated!")
