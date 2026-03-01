import pygame
from src.settings import *
from src.save_data import HP_COST, MAX_HP_UPGRADES


class Shop:
    """HP upgrade shop accessible from the island map."""

    def __init__(self, save_data):
        self.save_data = save_data
        self.font_big = None
        self.font_med = None
        self.font_small = None
        self.message = ""
        self.message_timer = 0

    def _init_fonts(self):
        if self.font_big is None:
            self.font_big = pygame.font.Font(None, 48)
            self.font_med = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        """Handle input. Returns "close" to go back to island map, None otherwise."""
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_ESCAPE or event.key == pygame.K_s:
            return "close"
        elif event.key == pygame.K_RETURN:
            if self.save_data.buy_hp():
                self.save_data.save()
                self.message = "HP upgraded!"
                self.message_timer = 90  # show for 1.5 seconds
            else:
                if self.save_data.hp_upgrades >= MAX_HP_UPGRADES:
                    self.message = "Already at max HP!"
                else:
                    self.message = "Not enough coins!"
                self.message_timer = 90
        return None

    def draw(self, screen):
        """Draw the shop screen."""
        self._init_fonts()

        # Dark background
        screen.fill((20, 15, 30))

        # Title
        title = self.font_big.render("SHOP", True, (255, 220, 50))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

        # Coin counter
        coin_text = self.font_med.render(f"Your Coins: {self.save_data.coins}", True, (255, 220, 50))
        screen.blit(coin_text, (SCREEN_WIDTH // 2 - coin_text.get_width() // 2, 110))

        # HP upgrade section
        box_x = SCREEN_WIDTH // 2 - 150
        box_y = 170
        box_w = 300
        box_h = 200

        # Box background
        pygame.draw.rect(screen, (40, 35, 60), (box_x, box_y, box_w, box_h))
        pygame.draw.rect(screen, (100, 80, 150), (box_x, box_y, box_w, box_h), 3)

        # Item name
        item_text = self.font_med.render("+1 Max HP", True, WHITE)
        screen.blit(item_text, (box_x + box_w // 2 - item_text.get_width() // 2, box_y + 15))

        # Price
        can_afford = self.save_data.coins >= HP_COST
        at_max = self.save_data.hp_upgrades >= MAX_HP_UPGRADES
        price_color = (50, 200, 50) if can_afford and not at_max else (200, 50, 50)
        price_text = self.font_med.render(f"Cost: {HP_COST} coins", True, price_color)
        screen.blit(price_text, (box_x + box_w // 2 - price_text.get_width() // 2, box_y + 55))

        # Hearts showing HP upgrades
        from src.settings import PLAYER_MAX_HP
        hearts_y = box_y + 100
        total_hearts = PLAYER_MAX_HP + MAX_HP_UPGRADES  # max possible
        current_hp = PLAYER_MAX_HP + self.save_data.hp_upgrades

        heart_size = 16
        hearts_per_row = 13
        start_x = box_x + 20

        for h in range(total_hearts):
            hx = start_x + (h % hearts_per_row) * (heart_size + 4)
            hy = hearts_y + (h // hearts_per_row) * (heart_size + 4)

            if h < PLAYER_MAX_HP:
                # Base HP - red
                color = (200, 50, 50)
            elif h < current_hp:
                # Purchased HP - bright green
                color = (50, 200, 50)
            else:
                # Not yet purchased - dark gray
                color = (60, 60, 60)

            pygame.draw.rect(screen, color, (hx, hy, heart_size, heart_size))
            pygame.draw.rect(screen, (30, 30, 30), (hx, hy, heart_size, heart_size), 1)

        # Progress text
        progress = self.font_small.render(
            f"{self.save_data.hp_upgrades} / {MAX_HP_UPGRADES} upgrades purchased",
            True, (180, 180, 180)
        )
        screen.blit(progress, (box_x + box_w // 2 - progress.get_width() // 2, box_y + 155))

        # Buy prompt
        if at_max:
            prompt_text = self.font_med.render("MAX HP REACHED!", True, (255, 220, 50))
        else:
            prompt_text = self.font_med.render("Press ENTER to buy", True, WHITE)
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, 400))

        # Message (feedback after buying)
        if self.message_timer > 0:
            self.message_timer -= 1
            msg_color = (50, 200, 50) if "upgraded" in self.message else (200, 50, 50)
            msg_text = self.font_med.render(self.message, True, msg_color)
            screen.blit(msg_text, (SCREEN_WIDTH // 2 - msg_text.get_width() // 2, 440))

        # Close hint
        close_text = self.font_small.render("Press ESC or S to go back", True, (120, 120, 120))
        screen.blit(close_text, (SCREEN_WIDTH // 2 - close_text.get_width() // 2, SCREEN_HEIGHT - 30))
