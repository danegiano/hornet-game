import pygame
import math
from src.settings import *


class IslandMap:
    """Side-scrolling island selection screen."""

    def __init__(self, save_data):
        self.save_data = save_data
        self.selected = 0
        self.wave_offset = 0
        self.font_big = None
        self.font_med = None
        self.font_small = None

    def _init_fonts(self):
        """Initialize fonts (must be called after pygame.init)."""
        if self.font_big is None:
            self.font_big = pygame.font.Font(None, 48)
            self.font_med = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        """Handle input. Returns:
           - ("play", island_index) to start playing an island
           - "shop" to open the shop
           - "circus" to enter The Circus boss rush
           - None for no action
        """
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_RIGHT:
            max_sel = 5 if self.save_data.circus_unlocked else min(self.save_data.max_island_unlocked, 4)
            if self.selected < max_sel:
                self.selected += 1
        elif event.key == pygame.K_LEFT:
            if self.selected > 0:
                self.selected -= 1
        elif event.key == pygame.K_RETURN:
            if self.selected == 5:
                return "circus"
            return ("play", self.selected)
        elif event.key == pygame.K_s:
            return "shop"
        return None

    def draw(self, screen):
        """Draw the island map."""
        self._init_fonts()
        self.wave_offset += 0.03

        # Sky gradient
        screen.fill((40, 60, 120))

        # Draw water at bottom
        water_y = 400
        for row in range(water_y, SCREEN_HEIGHT):
            # Darker blue as it goes deeper
            depth = (row - water_y) / (SCREEN_HEIGHT - water_y)
            r = int(20 + depth * 10)
            g = int(80 - depth * 30)
            b = int(180 - depth * 60)
            pygame.draw.line(screen, (r, g, b), (0, row), (SCREEN_WIDTH, row))

        # Animated wave on top of water
        wave_points = []
        for x in range(0, SCREEN_WIDTH + 10, 5):
            wy = water_y + math.sin(self.wave_offset + x * 0.02) * 8
            wave_points.append((x, wy))
        wave_points.append((SCREEN_WIDTH, SCREEN_HEIGHT))
        wave_points.append((0, SCREEN_HEIGHT))
        pygame.draw.polygon(screen, (30, 90, 170), wave_points)

        # Draw islands
        island_spacing = 150
        start_x = 80
        for i, island in enumerate(ISLAND_DATA):
            ix = start_x + i * island_spacing
            iy = 340  # base y for islands

            # Island landmass (a bumpy triangle shape)
            is_unlocked = i <= self.save_data.max_island_unlocked
            color = island["color"] if is_unlocked else (80, 80, 80)

            # Island shape - a mound
            height = 60 + i * 15  # taller islands for harder ones
            points = [
                (ix - 40, iy + 20),
                (ix - 30, iy - height // 2),
                (ix - 10, iy - height),
                (ix + 10, iy - height + 10),
                (ix + 30, iy - height // 2 - 5),
                (ix + 40, iy + 20),
            ]
            pygame.draw.polygon(screen, color, points)
            # Darker outline
            darker = (max(0, color[0]-30), max(0, color[1]-30), max(0, color[2]-30))
            pygame.draw.polygon(screen, darker, points, 3)

            # Island name below
            name_text = self.font_small.render(island["name"], True, WHITE if is_unlocked else (100, 100, 100))
            screen.blit(name_text, (ix - name_text.get_width() // 2, iy + 30))

            # Level count
            completed = len(self.save_data.completed_levels.get(str(i), []))
            total = island["levels"]
            progress_text = self.font_small.render(f"{completed}/{total}", True, (200, 200, 200) if is_unlocked else (80, 80, 80))
            screen.blit(progress_text, (ix - progress_text.get_width() // 2, iy + 50))

            # Lock icon on locked islands
            if not is_unlocked:
                lock_text = self.font_med.render("LOCKED", True, (150, 50, 50))
                screen.blit(lock_text, (ix - lock_text.get_width() // 2, iy - height - 30))

            # Selection cursor (hornet icon / arrow)
            if i == self.selected:
                # Bouncing arrow above selected island
                bounce = math.sin(self.wave_offset * 3) * 5
                arrow_y = iy - height - 40 + bounce
                # Draw a little yellow triangle pointing down
                pygame.draw.polygon(screen, (255, 220, 50), [
                    (ix, arrow_y + 15),
                    (ix - 10, arrow_y),
                    (ix + 10, arrow_y),
                ])

        # Draw The Circus (slot 5) if unlocked
        if self.save_data.circus_unlocked:
            ix = start_x + 5 * island_spacing
            iy = 340
            height = 90
            color = (220, 80, 80)  # circus red
            points = [
                (ix - 40, iy + 20),
                (ix - 30, iy - height // 2),
                (ix - 10, iy - height),
                (ix + 10, iy - height + 10),
                (ix + 30, iy - height // 2 - 5),
                (ix + 40, iy + 20),
            ]
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, (160, 40, 40), points, 3)
            name_t = self.font_small.render("THE CIRCUS", True, WHITE)
            screen.blit(name_t, (ix - name_t.get_width() // 2, iy + 30))
            sub_t = self.font_small.render("BOSS RUSH", True, (220, 180, 180))
            screen.blit(sub_t, (ix - sub_t.get_width() // 2, iy + 50))

            if self.selected == 5:
                bounce = math.sin(self.wave_offset * 3) * 5
                arrow_y = iy - height - 40 + bounce
                pygame.draw.polygon(screen, (255, 80, 80), [
                    (ix, arrow_y + 15),
                    (ix - 10, arrow_y),
                    (ix + 10, arrow_y),
                ])

        # Title
        title = self.font_big.render("ISLAND MAP", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        # Coin counter
        coin_text = self.font_med.render(f"Coins: {self.save_data.coins}", True, (255, 220, 50))
        screen.blit(coin_text, (20, 20))

        # Shop hint
        shop_text = self.font_small.render("Press S for Shop", True, (180, 180, 180))
        screen.blit(shop_text, (20, 55))

        # Controls hint
        ctrl_text = self.font_small.render("LEFT/RIGHT to select, ENTER to play", True, (150, 150, 150))
        screen.blit(ctrl_text, (SCREEN_WIDTH // 2 - ctrl_text.get_width() // 2, SCREEN_HEIGHT - 30))

        # Powers bar at bottom
        from src.systems.powers import ALL_POWERS
        powers_y = SCREEN_HEIGHT - 60
        power_names = ["Dbl Jump", "Dash", "Wall Climb", "Shield", "Stinger+"]
        px = 200
        for j, (power_id, power_label) in enumerate(zip(ALL_POWERS, power_names)):
            has_it = self.save_data.has_power(power_id)
            color = (255, 220, 50) if has_it else (80, 80, 80)
            label = power_label if has_it else "???"
            pt = self.font_small.render(f"[{label}]", True, color)
            screen.blit(pt, (px + j * 120, powers_y))
