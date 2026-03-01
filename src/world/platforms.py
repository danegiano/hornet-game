import pygame
import math
from src.settings import *


class Platform:
    def __init__(self, x, y, width, height, color=(100, 180, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_garden = (color == (100, 180, 100))
        self.is_hive = (color == (160, 120, 60))
        self.is_tower = (color == (80, 80, 80))

    def draw(self, screen, camera_x, time_ms=0):
        draw_rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(screen, self.color, draw_rect)
        pygame.draw.rect(screen, (30,50,30), draw_rect, 2)

        if self.is_garden:
            import math
            for gx in range(0, self.rect.width, 10):
                world_x = self.rect.x + gx
                wind = math.sin(time_ms / 300.0 + world_x / 50.0) * 8
                start_pos = (draw_rect.x + gx, draw_rect.y)
                end_pos = (draw_rect.x + gx + int(wind), draw_rect.y - 12)
                pygame.draw.line(screen, (60, 200, 60), start_pos, end_pos, 2)

        elif self.is_hive:
            import math
            # Draw honey comb pattern inside the platform
            for hx in range(10, self.rect.width, 30):
                pygame.draw.ellipse(screen, (180, 140, 40), (draw_rect.x + hx, draw_rect.y + 5, 20, 15))

            # Draw dripping honey off the bottom edge!
            for dx in range(15, self.rect.width, 40):
                world_x = self.rect.x + dx
                # Make honey drip down slowly over time and snap back
                drip_y = (time_ms / 20.0 + world_x * 7) % 30

                # A strand of honey connecting the drip
                pygame.draw.line(screen, (255, 200, 0), (draw_rect.x + dx, draw_rect.bottom), (draw_rect.x + dx, draw_rect.bottom + int(drip_y)), 3)
                # The actual drop
                pygame.draw.circle(screen, (255, 210, 50), (draw_rect.x + dx, draw_rect.bottom + int(drip_y)), 4)

        elif self.is_tower:
            import math
            # Draw stone bricks pattern
            for bx in range(0, self.rect.width, 40):
                pygame.draw.line(screen, (50, 50, 50), (draw_rect.x + bx, draw_rect.y), (draw_rect.x + bx, draw_rect.bottom), 2)
            for by in range(0, self.rect.height, 20):
                pygame.draw.line(screen, (50, 50, 50), (draw_rect.x, draw_rect.y + by), (draw_rect.right, draw_rect.y + by), 2)

            # Animated flickering torches along the top edge
            for tx in range(20, self.rect.width, 80):
                world_x = self.rect.x + tx
                flicker = math.sin(time_ms / 50.0 + world_x) * 4 + math.cos(time_ms / 100.0) * 2

                # Torch base
                pygame.draw.rect(screen, (60, 40, 20), (draw_rect.x + tx - 4, draw_rect.y - 15, 8, 15))
                # Flames
                flame_y = draw_rect.y - 15 - int(flicker)
                pygame.draw.circle(screen, (255, 100, 0), (draw_rect.x + tx, flame_y), 6 + int(flicker/2))
                pygame.draw.circle(screen, (255, 200, 0), (draw_rect.x + tx, flame_y + 2), 3 + int(flicker/3))
