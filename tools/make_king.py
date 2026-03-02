import pygame
import os

pygame.init()
os.makedirs("sprites", exist_ok=True)

W, H = 120, 90

# Color palette
DARK_GOLD    = (180, 130,  10, 255)
MID_GOLD     = (220, 175,  20, 255)
BRIGHT_GOLD  = (255, 215,  60, 255)
BLACK        = ( 20,  20,  20, 255)
DEEP_BLACK   = (  5,   5,   5, 255)
CROWN_GOLD   = (255, 200,   0, 255)
RED_DARK     = (180,  20,  20, 255)
RED_BRIGHT   = (255,  80,  80, 255)
RED_CENTER   = (255, 220, 220, 255)
WING_BASE    = (190, 220, 255, 150)
WING_VEIN    = (120, 160, 220, 200)
STINGER      = ( 30,  30,  30, 255)


def draw_wing_veins(surf, rect_x, rect_y, rect_w, rect_h, flip=False):
    """Draw thin vein lines inside a wing ellipse."""
    cx = rect_x + rect_w // 2
    cy = rect_y + rect_h // 2
    # 4-5 veins radiating outward
    vein_ends = [
        (rect_x + 4,          rect_y + rect_h // 3),
        (rect_x + rect_w // 4, rect_y + 4),
        (cx,                   rect_y + 2),
        (rect_x + 3*rect_w//4, rect_y + 6),
        (rect_x + rect_w - 4, rect_y + rect_h // 3),
        (rect_x + rect_w - 6, cy + 4),
    ]
    start = (cx, cy + rect_h // 4)
    for end in vein_ends:
        pygame.draw.line(surf, WING_VEIN, start, end, 1)


def draw_king(flap=False):
    s = pygame.Surface((W, H), pygame.SRCALPHA)

    # --------------------------------------------------
    # WINGS  (drawn first so body sits on top)
    # --------------------------------------------------
    if flap:
        # Wings raised high overhead
        left_wing_rect  = (5,  2, 46, 60)
        right_wing_rect = (69, 2, 46, 60)
    else:
        # Wings spread horizontally at mid-body
        left_wing_rect  = (0,  28, 52, 28)
        right_wing_rect = (68, 28, 52, 28)

    # Fill wing ellipses
    pygame.draw.ellipse(s, WING_BASE, left_wing_rect)
    pygame.draw.ellipse(s, WING_BASE, right_wing_rect)

    # Vein lines on each wing
    draw_wing_veins(s, *left_wing_rect)
    draw_wing_veins(s, *right_wing_rect)

    # Wing outlines
    pygame.draw.ellipse(s, WING_VEIN, left_wing_rect, 1)
    pygame.draw.ellipse(s, WING_VEIN, right_wing_rect, 1)

    # --------------------------------------------------
    # STINGER  (thick downward point)
    # --------------------------------------------------
    pygame.draw.polygon(s, DEEP_BLACK, [
        (54, 78), (66, 78), (63, 90), (57, 90)
    ])
    pygame.draw.polygon(s, STINGER, [
        (56, 76), (64, 76), (60, 89)
    ])

    # --------------------------------------------------
    # ABDOMEN  (main body — large layered ellipses)
    # --------------------------------------------------
    # Outer shadow layer
    pygame.draw.ellipse(s, DEEP_BLACK,  (26, 32, 68, 52))
    # Main dark-gold body
    pygame.draw.ellipse(s, DARK_GOLD,   (28, 34, 64, 48))
    # Highlight/sheen
    pygame.draw.ellipse(s, MID_GOLD,    (32, 37, 56, 38))
    # Top bright streak
    pygame.draw.ellipse(s, BRIGHT_GOLD, (38, 38, 40, 16))

    # Black stripes across abdomen (3 thick lines)
    stripe_color = (15, 15, 15, 230)
    for sy in [49, 59, 69]:
        # Clip stripe to roughly the ellipse width at that height
        stripe_left  = 30
        stripe_right = 90
        stripe_surf = pygame.Surface((W, H), pygame.SRCALPHA)
        pygame.draw.line(stripe_surf, stripe_color,
                         (stripe_left, sy), (stripe_right, sy), 6)
        s.blit(stripe_surf, (0, 0))

    # Re-draw ellipse outline so stripes don't bleed outside body shape
    pygame.draw.ellipse(s, DEEP_BLACK, (26, 32, 68, 52), 3)

    # --------------------------------------------------
    # HEAD  (smaller ellipse above abdomen)
    # --------------------------------------------------
    pygame.draw.ellipse(s, DEEP_BLACK, (36, 14, 48, 34))   # shadow
    pygame.draw.ellipse(s, DARK_GOLD,  (38, 16, 44, 30))   # dark gold head
    pygame.draw.ellipse(s, MID_GOLD,   (41, 19, 36, 22))   # mid highlight

    # --------------------------------------------------
    # GLOWING RED EYES  (two circles with bright centers)
    # --------------------------------------------------
    # Left eye
    pygame.draw.circle(s, RED_DARK,   (47, 27), 7)
    pygame.draw.circle(s, RED_BRIGHT, (47, 27), 5)
    pygame.draw.circle(s, RED_CENTER, (47, 26), 2)

    # Right eye
    pygame.draw.circle(s, RED_DARK,   (73, 27), 7)
    pygame.draw.circle(s, RED_BRIGHT, (73, 27), 5)
    pygame.draw.circle(s, RED_CENTER, (73, 26), 2)

    # --------------------------------------------------
    # CROWN  (elaborate polygon on top of head)
    # --------------------------------------------------
    # Base band of the crown
    pygame.draw.polygon(s, CROWN_GOLD, [
        (40, 19), (80, 19), (78, 13), (42, 13)
    ])
    # Five crown points of varying heights
    points_crown = [
        # (base_left, base_right, tip_x, tip_y)
        (41, 47,  44,  2),   # far-left tall point
        (47, 52,  49,  7),   # second point
        (53, 67,  60,  0),   # center tallest
        (65, 70,  71,  7),   # fourth point
        (71, 76,  76,  2),   # far-right tall point
    ]
    for bl, br, tx, ty in points_crown:
        pygame.draw.polygon(s, CROWN_GOLD, [(bl, 13), (br, 13), (tx, ty)])
        # Bright highlight on each spike
        pygame.draw.polygon(s, BRIGHT_GOLD, [
            (bl + 1, 13), ((bl + br) // 2, 13), (tx, ty + 2)
        ])

    # Crown outline
    pygame.draw.polygon(s, DEEP_BLACK, [
        (40, 19), (80, 19), (78, 13),
        (76, 2), (71, 7), (65, 13),
        (60, 0), (53, 7),
        (49, 13), (47, 7),
        (44, 2), (42, 13)
    ], 2)

    # Crown gems — 3 small red dots on the base band
    for gem_x in [50, 60, 70]:
        pygame.draw.circle(s, RED_BRIGHT, (gem_x, 16), 3)
        pygame.draw.circle(s, RED_CENTER, (gem_x, 15), 1)

    return s


pygame.image.save(draw_king(False), "sprites/king_0.png")
pygame.image.save(draw_king(True),  "sprites/king_1.png")
print("Wasp King sprites generated: sprites/king_0.png, sprites/king_1.png")
