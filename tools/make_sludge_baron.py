import pygame
import os
import math

pygame.init()
os.makedirs("sprites", exist_ok=True)

W, H = 100, 80

# Color palette — dark swampy greens
BODY_DARK    = ( 30,  70,  20, 255)   # deep army green
BODY_MID     = ( 45,  95,  28, 255)   # mid green
BODY_LIGHT   = ( 60, 120,  38, 255)   # highlight green
SHADOW       = ( 15,  40,  10, 255)   # deep shadow
SHELL_LINE   = ( 22,  55,  14, 255)   # shell crack lines
HORN         = ( 20,  55,  15, 255)   # horn color
HORN_EDGE    = ( 10,  30,   8, 255)   # horn outline
LEG          = ( 25,  60,  18, 255)   # leg color
EYE_OUTER    = ( 80, 200,  40, 255)   # glowing green eye
EYE_INNER    = (160, 255,  60, 255)   # bright yellow-green
EYE_CENTER   = (230, 255, 180, 255)   # near-white center
UNDERBELLY   = ( 20,  50,  14, 255)


def draw_thick_arc(surf, color, cx, cy, rx, ry, start_angle, end_angle, width, steps=30):
    """Draw a thick arc as a series of thick line segments."""
    prev = None
    for i in range(steps + 1):
        t = start_angle + (end_angle - start_angle) * i / steps
        x = int(cx + rx * math.cos(t))
        y = int(cy + ry * math.sin(t))
        if prev:
            pygame.draw.line(surf, color, prev, (x, y), width)
        prev = (x, y)


def draw_baron(rolling=False):
    s = pygame.Surface((W, H), pygame.SRCALPHA)

    if rolling:
        # Frame 1: shell slightly raised, legs spread wider
        body_rect    = pygame.Rect(5,  18, 90, 56)
        shell_rect   = pygame.Rect(8,  14, 84, 48)
        leg_spread   = 18   # extra spread for rolling legs
        horn_offset  = -4   # horns tilt back more
    else:
        # Frame 0: standing normally
        body_rect    = pygame.Rect(5,  22, 90, 52)
        shell_rect   = pygame.Rect(8,  18, 84, 44)
        leg_spread   = 0
        horn_offset  = 0

    # --------------------------------------------------
    # LEGS  (3 on each side, angled downward) — drawn first
    # --------------------------------------------------
    leg_y_base = body_rect.centery + 10
    leg_xs_left  = [body_rect.left + 12, body_rect.left + 26, body_rect.left + 40]
    leg_xs_right = [body_rect.right - 12, body_rect.right - 26, body_rect.right - 40]

    for i, lx in enumerate(leg_xs_left):
        angle_offset = (i - 1) * 6 + leg_spread
        end_x = lx - 18 - leg_spread
        end_y = leg_y_base + 18 + abs(i - 1) * 4
        pygame.draw.line(s, SHADOW, (lx, leg_y_base), (end_x, end_y), 5)
        pygame.draw.line(s, LEG,    (lx, leg_y_base), (end_x, end_y), 3)
        # Foot
        pygame.draw.circle(s, SHADOW, (end_x, end_y), 3)

    for i, lx in enumerate(leg_xs_right):
        end_x = lx + 18 + leg_spread
        end_y = leg_y_base + 18 + abs(i - 1) * 4
        pygame.draw.line(s, SHADOW, (lx, leg_y_base), (end_x, end_y), 5)
        pygame.draw.line(s, LEG,    (lx, leg_y_base), (end_x, end_y), 3)
        pygame.draw.circle(s, SHADOW, (end_x, end_y), 3)

    # --------------------------------------------------
    # UNDERBELLY  (flat bottom visible under the shell)
    # --------------------------------------------------
    pygame.draw.ellipse(s, UNDERBELLY, (
        body_rect.x + 5, body_rect.y + body_rect.height // 2,
        body_rect.width - 10, body_rect.height // 2 + 4
    ))

    # --------------------------------------------------
    # MAIN BODY / SHELL  (layered ellipses for depth)
    # --------------------------------------------------
    # Shadow drop
    pygame.draw.ellipse(s, SHADOW,     (shell_rect.x + 3, shell_rect.y + 4,
                                        shell_rect.width, shell_rect.height))
    # Dark outer shell
    pygame.draw.ellipse(s, BODY_DARK,  shell_rect)
    # Mid layer
    mid = pygame.Rect(shell_rect.x + 6, shell_rect.y + 4,
                      shell_rect.width - 12, shell_rect.height - 8)
    pygame.draw.ellipse(s, BODY_MID, mid)
    # Top highlight
    hi = pygame.Rect(mid.x + 8, mid.y + 4, mid.width - 24, mid.height // 2 - 2)
    pygame.draw.ellipse(s, BODY_LIGHT, hi)

    # --------------------------------------------------
    # SHELL CRACKS / SEGMENT LINES
    # --------------------------------------------------
    cx = shell_rect.centerx
    cy = shell_rect.centery

    # Central spine line
    pygame.draw.line(s, SHELL_LINE, (cx, shell_rect.top + 4), (cx, shell_rect.bottom - 6), 2)

    # Three horizontal segment arcs (simple lines)
    for frac in [0.3, 0.55, 0.75]:
        sy = int(shell_rect.top + shell_rect.height * frac)
        half_w = int((shell_rect.width / 2) * math.sqrt(1 - (frac - 0.5) ** 2 * 4) * 0.9)
        pygame.draw.line(s, SHELL_LINE,
                         (cx - half_w, sy),
                         (cx + half_w, sy), 2)

    # A few diagonal crack lines
    pygame.draw.line(s, SHELL_LINE, (cx - 10, cy - 8), (cx - 22, cy + 4), 1)
    pygame.draw.line(s, SHELL_LINE, (cx + 10, cy - 8), (cx + 22, cy + 4), 1)
    pygame.draw.line(s, SHELL_LINE, (cx - 5,  cy + 2), (cx - 14, cy + 12), 1)

    # Shell outline
    pygame.draw.ellipse(s, SHADOW, shell_rect, 3)

    # --------------------------------------------------
    # HEAD  (front of the beetle, slightly protruding)
    # --------------------------------------------------
    head_x = shell_rect.x + shell_rect.width // 2 - 20
    head_y = shell_rect.y + 2
    head_w = 40
    head_h = 32
    pygame.draw.ellipse(s, SHADOW,    (head_x - 2, head_y + 2, head_w + 4, head_h))
    pygame.draw.ellipse(s, BODY_DARK, (head_x,     head_y,     head_w,     head_h))
    pygame.draw.ellipse(s, BODY_MID,  (head_x + 4, head_y + 3, head_w - 8, head_h - 6))

    # --------------------------------------------------
    # HORNS  (two large curved arcs on the head, pointing upward)
    # --------------------------------------------------
    hcx = head_x + head_w // 2   # head center x
    htop = head_y + 4             # top of head

    # Left horn — curves up and to the left
    draw_thick_arc(s, HORN_EDGE,
                   hcx - 10 + horn_offset, htop + 4, 14, 20,
                   math.radians(190), math.radians(310), 6)
    draw_thick_arc(s, HORN,
                   hcx - 10 + horn_offset, htop + 4, 14, 20,
                   math.radians(190), math.radians(310), 4)

    # Right horn — mirrors left, curves up and to the right
    draw_thick_arc(s, HORN_EDGE,
                   hcx + 10 - horn_offset, htop + 4, 14, 20,
                   math.radians(230), math.radians(350), 6)
    draw_thick_arc(s, HORN,
                   hcx + 10 - horn_offset, htop + 4, 14, 20,
                   math.radians(230), math.radians(350), 4)

    # --------------------------------------------------
    # GLOWING EYES  (two large circles with bright centers)
    # --------------------------------------------------
    eye_y = head_y + head_h // 3 + 2
    left_eye_x  = head_x + head_w // 3 - 2
    right_eye_x = head_x + 2 * head_w // 3 + 2

    for ex in [left_eye_x, right_eye_x]:
        pygame.draw.circle(s, SHADOW,     (ex, eye_y), 9)
        pygame.draw.circle(s, EYE_OUTER,  (ex, eye_y), 7)
        pygame.draw.circle(s, EYE_INNER,  (ex, eye_y), 4)
        pygame.draw.circle(s, EYE_CENTER, (ex, eye_y - 1), 2)

    return s


pygame.image.save(draw_baron(False), "sprites/sludge_baron_0.png")
pygame.image.save(draw_baron(True),  "sprites/sludge_baron_1.png")
print("Sludge Baron sprites generated: sprites/sludge_baron_0.png, sprites/sludge_baron_1.png")
