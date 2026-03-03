import pygame
import math
from src.settings import *


class HallucinationMap:
    """Island map for Hallucination Land — dark, eerie version."""

    def __init__(self, save_data):
        self.save_data = save_data
        self.selected = 0
        self.wave_offset = 0
        self.font_big = None
        self.font_med = None
        self.font_small = None

    def _init_fonts(self):
        if self.font_big is None:
            self.font_big   = pygame.font.Font(None, 48)
            self.font_med   = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        """Returns:
           - ("play", island_index) to start playing
           - ("shop", island_index) to open the hallucination shop
           - None for no action
        """
        if event.type != pygame.KEYDOWN:
            return None

        max_sel = min(self.save_data.hallucination_island, 4)
        if event.key == pygame.K_RIGHT:
            if self.selected < max_sel:
                self.selected += 1
        elif event.key == pygame.K_LEFT:
            if self.selected > 0:
                self.selected -= 1
        elif event.key == pygame.K_RETURN:
            return ("play", self.selected)
        elif event.key == pygame.K_s:
            return ("shop", self.selected)
        return None

    def draw(self, screen):
        self._init_fonts()
        self.wave_offset += 0.03

        # Dark void background
        screen.fill((5, 0, 15))

        # Eerie mist at bottom
        for row in range(400, SCREEN_HEIGHT):
            depth = (row - 400) / (SCREEN_HEIGHT - 400)
            r = int(20 * depth)
            b = int(40 * depth)
            pygame.draw.line(screen, (r, 0, b), (0, row), (SCREEN_WIDTH, row))

        # Draw hallucination islands
        island_spacing = 140
        start_x = 80
        for i, island in enumerate(HALLUCINATION_ISLAND_DATA):
            ix = start_x + i * island_spacing
            iy = 340

            is_unlocked = i <= self.save_data.hallucination_island
            color = island["color"] if is_unlocked else (40, 20, 60)

            height = 70 + i * 12
            points = [
                (ix - 40, iy + 20),
                (ix - 30, iy - height // 2),
                (ix - 10, iy - height),
                (ix + 10, iy - height + 10),
                (ix + 30, iy - height // 2 - 5),
                (ix + 40, iy + 20),
            ]
            pygame.draw.polygon(screen, color, points)
            darker = (max(0, color[0]-20), max(0, color[1]-10), max(0, color[2]-20))
            pygame.draw.polygon(screen, darker, points, 3)

            name_text = self.font_small.render(island["name"], True, (200, 150, 220) if is_unlocked else (60, 40, 80))
            screen.blit(name_text, (ix - name_text.get_width() // 2, iy + 30))

            if not is_unlocked:
                lock_text = self.font_med.render("LOCKED", True, (80, 30, 80))
                screen.blit(lock_text, (ix - lock_text.get_width() // 2, iy - height - 30))

            if i == self.selected:
                bounce = math.sin(self.wave_offset * 3) * 5
                arrow_y = iy - height - 40 + bounce
                pygame.draw.polygon(screen, (180, 80, 255), [
                    (ix, arrow_y + 15),
                    (ix - 10, arrow_y),
                    (ix + 10, arrow_y),
                ])

        # Title
        title = self.font_big.render("HALLUCINATION LAND", True, (160, 80, 220))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        # Coin counter
        coin_text = self.font_med.render(f"Coins: {self.save_data.coins}", True, (200, 180, 255))
        screen.blit(coin_text, (20, 20))

        # Lives counter
        lives_color = (50, 200, 50) if self.save_data.hallucination_lives > 0 else (150, 50, 50)
        lives_text = self.font_med.render(f"Lives: {self.save_data.hallucination_lives}/10", True, lives_color)
        screen.blit(lives_text, (20, 50))

        # Hint
        ctrl_text = self.font_small.render("LEFT/RIGHT to select  |  ENTER to play  |  S for shop", True, (120, 90, 150))
        screen.blit(ctrl_text, (SCREEN_WIDTH // 2 - ctrl_text.get_width() // 2, SCREEN_HEIGHT - 30))
