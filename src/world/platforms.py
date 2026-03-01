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
        self.is_swamp = (color == (60, 100, 50))
        self.is_crystal = (color == (80, 60, 140))
        self.is_volcano = (color == (100, 50, 30))
        self.is_shadow = (color == (50, 30, 70))

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

        elif self.is_swamp:
            import math
            # Mossy top edge — a wavy green line
            for mx in range(0, self.rect.width, 6):
                world_x = self.rect.x + mx
                moss_h = int(math.sin(world_x / 15.0) * 3 + 4)
                pygame.draw.rect(screen, (40, 130, 40),
                                 (draw_rect.x + mx, draw_rect.y - moss_h, 6, moss_h))

            # Bubbles rising from the platform (animated)
            for bx in range(25, self.rect.width, 50):
                world_x = self.rect.x + bx
                # Each bubble rises over time, then resets
                bubble_cycle = (time_ms / 15.0 + world_x * 3) % 40
                bubble_y = draw_rect.y - int(bubble_cycle)
                bubble_r = max(2, 4 - int(bubble_cycle / 12))
                if bubble_cycle < 35:
                    pygame.draw.circle(screen, (80, 160, 80), (draw_rect.x + bx, bubble_y), bubble_r)
                    pygame.draw.circle(screen, (120, 200, 100), (draw_rect.x + bx - 1, bubble_y - 1), max(1, bubble_r - 1))

            # Hanging vines from bottom edge
            for vx in range(10, self.rect.width, 35):
                world_x = self.rect.x + vx
                vine_sway = math.sin(time_ms / 400.0 + world_x / 30.0) * 5
                vine_len = 8 + (world_x % 12)
                start = (draw_rect.x + vx, draw_rect.bottom)
                end = (draw_rect.x + vx + int(vine_sway), draw_rect.bottom + vine_len)
                pygame.draw.line(screen, (30, 90, 30), start, end, 2)

        elif self.is_crystal:
            import math, random
            # Glowing purple edges
            edge_color = (120, 80, 200)
            pygame.draw.rect(screen, edge_color, draw_rect, 2)

            # Crystal spikes on top (small triangles along the top edge)
            for sx in range(5, self.rect.width - 5, 18):
                world_x = self.rect.x + sx
                # Vary spike height based on world position (deterministic)
                spike_h = 6 + (world_x * 7 % 5)
                pts = [
                    (draw_rect.x + sx - 4, draw_rect.y),
                    (draw_rect.x + sx, draw_rect.y - spike_h),
                    (draw_rect.x + sx + 4, draw_rect.y),
                ]
                pygame.draw.polygon(screen, (130, 100, 200), pts)
                pygame.draw.polygon(screen, (180, 150, 255), pts, 1)

            # Sparkling/twinkling dots that flash bright
            for tx in range(8, self.rect.width, 15):
                world_x = self.rect.x + tx
                # Use time + position to make sparkles blink
                sparkle = math.sin(time_ms / 200.0 + world_x * 1.7) * 0.5 + 0.5
                if sparkle > 0.7:
                    brightness = int(150 + sparkle * 105)
                    spark_y = draw_rect.y + 3 + (world_x * 13 % max(1, self.rect.height - 6))
                    pygame.draw.circle(screen, (brightness, brightness, 255),
                                       (draw_rect.x + tx, spark_y), 2)
                    # Tiny highlight
                    pygame.draw.circle(screen, (255, 255, 255),
                                       (draw_rect.x + tx, spark_y), 1)

        elif self.is_volcano:
            import math
            # Dark cracked surface — jagged lines across the top
            for cx in range(0, self.rect.width, 25):
                world_x = self.rect.x + cx
                # Deterministic crack pattern based on world position
                crack_end_x = cx + 12 + (world_x * 3 % 10)
                crack_dip = 3 + (world_x * 7 % 4)
                pygame.draw.line(screen, (50, 25, 15),
                                 (draw_rect.x + cx, draw_rect.y + 2),
                                 (draw_rect.x + min(crack_end_x, self.rect.width),
                                  draw_rect.y + crack_dip), 2)

            # Red/orange lava glow along the bottom edge
            glow_h = min(6, self.rect.height - 2)
            glow_pulse = math.sin(time_ms / 300.0) * 0.3 + 0.7
            glow_r = int(200 * glow_pulse)
            glow_g = int(60 * glow_pulse)
            for gx in range(0, self.rect.width, 4):
                world_x = self.rect.x + gx
                # Vary the glow intensity along the edge
                intensity = math.sin(world_x / 20.0 + time_ms / 500.0) * 0.3 + 0.7
                r = int(glow_r * intensity)
                g = int(glow_g * intensity)
                pygame.draw.rect(screen, (min(255, r), min(255, g), 0),
                                 (draw_rect.x + gx, draw_rect.bottom - glow_h, 4, glow_h))

            # Floating embers/sparks rising up from the platform
            for ex in range(15, self.rect.width, 40):
                world_x = self.rect.x + ex
                # Each ember rises over time, then resets
                ember_cycle = (time_ms / 10.0 + world_x * 5) % 50
                ember_y = draw_rect.y - int(ember_cycle)
                ember_size = max(1, 3 - int(ember_cycle / 18))
                if ember_cycle < 45:
                    # Orange-yellow ember
                    pygame.draw.circle(screen, (255, 150 + int(ember_cycle * 2), 0),
                                       (draw_rect.x + ex, ember_y), ember_size)

        elif self.is_shadow:
            import math
            # Dark purple brick pattern
            for bx in range(0, self.rect.width, 35):
                pygame.draw.line(screen, (30, 15, 45),
                                 (draw_rect.x + bx, draw_rect.y),
                                 (draw_rect.x + bx, draw_rect.bottom), 2)
            for by in range(0, self.rect.height, 18):
                pygame.draw.line(screen, (30, 15, 45),
                                 (draw_rect.x, draw_rect.y + by),
                                 (draw_rect.right, draw_rect.y + by), 2)

            # Glowing purple cracks across the surface
            for cx in range(8, self.rect.width, 30):
                world_x = self.rect.x + cx
                crack_len = 10 + (world_x * 3 % 8)
                crack_dip = 2 + (world_x * 5 % 4)
                glow_pulse = math.sin(time_ms / 400.0 + world_x * 0.1) * 0.4 + 0.6
                glow_r = int(120 * glow_pulse)
                glow_g = int(40 * glow_pulse)
                glow_b = int(180 * glow_pulse)
                pygame.draw.line(screen, (glow_r, glow_g, glow_b),
                                 (draw_rect.x + cx, draw_rect.y + 3),
                                 (draw_rect.x + min(cx + crack_len, self.rect.width),
                                  draw_rect.y + crack_dip), 2)

            # Purple spark/lightning effects (occasional flickers)
            for sx in range(20, self.rect.width, 50):
                world_x = self.rect.x + sx
                spark_chance = math.sin(time_ms / 100.0 + world_x * 2.3) * 0.5 + 0.5
                if spark_chance > 0.85:
                    spark_y = draw_rect.y + (world_x * 7 % max(1, self.rect.height - 4))
                    # Bright purple spark
                    pygame.draw.circle(screen, (180, 80, 255),
                                       (draw_rect.x + sx, spark_y), 3)
                    pygame.draw.circle(screen, (255, 200, 255),
                                       (draw_rect.x + sx, spark_y), 1)

            # Shadowy wisps floating off the top edge
            for wx in range(12, self.rect.width, 35):
                world_x = self.rect.x + wx
                wisp_cycle = (time_ms / 12.0 + world_x * 4) % 35
                wisp_y = draw_rect.y - int(wisp_cycle)
                wisp_size = max(1, 3 - int(wisp_cycle / 12))
                if wisp_cycle < 30:
                    wisp_alpha = int(150 * (1.0 - wisp_cycle / 30.0))
                    wisp_surf = pygame.Surface((wisp_size * 2, wisp_size * 2), pygame.SRCALPHA)
                    wisp_surf.fill((80, 30, 120, wisp_alpha))
                    screen.blit(wisp_surf, (draw_rect.x + wx - wisp_size, wisp_y - wisp_size))
