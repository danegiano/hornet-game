import pygame
from src.settings import *
from src.save_data import HP_COST, MAX_HP_UPGRADES

TOTEM_COST = 500
TOTEM_PACK = 3


class Shop:
    """HP upgrade shop accessible from the island map."""

    def __init__(self, save_data):
        self.save_data = save_data
        self.font_big = None
        self.font_med = None
        self.font_small = None
        self.message = ""
        self.message_timer = 0
        self.selected = 0  # 0 = HP upgrade, 1 = Totem of Undying

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
        elif event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % 2
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % 2
        elif event.key == pygame.K_RETURN:
            if self.selected == 0:
                if self.save_data.buy_hp():
                    self.save_data.save()
                    self.message = "HP upgraded!"
                    self.message_timer = 90
                else:
                    if self.save_data.hp_upgrades >= MAX_HP_UPGRADES:
                        self.message = "Already at max HP!"
                    else:
                        self.message = "Not enough coins!"
                    self.message_timer = 90
            else:
                if self.save_data.buy_totems():
                    self.save_data.save()
                    self.message = f"Got {TOTEM_PACK} Totems of Undying!"
                    self.message_timer = 90
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
        screen.blit(coin_text, (SCREEN_WIDTH // 2 - coin_text.get_width() // 2, 95))

        # Nav hint
        nav_text = self.font_small.render("UP / DOWN to select  |  ENTER to buy", True, (140, 140, 160))
        screen.blit(nav_text, (SCREEN_WIDTH // 2 - nav_text.get_width() // 2, 128))

        # ── Item boxes ──────────────────────────────────────────────
        box_w = 280
        box_h = 210
        gap = 40
        total_w = box_w * 2 + gap
        start_x = SCREEN_WIDTH // 2 - total_w // 2
        box_y = 160

        # --- HP Upgrade box ---
        hp_x = start_x
        hp_selected = self.selected == 0
        border_color = (255, 220, 50) if hp_selected else (100, 80, 150)
        pygame.draw.rect(screen, (40, 35, 60), (hp_x, box_y, box_w, box_h))
        pygame.draw.rect(screen, border_color, (hp_x, box_y, box_w, box_h), 3)

        item_text = self.font_med.render("+1 Max HP", True, WHITE)
        screen.blit(item_text, (hp_x + box_w // 2 - item_text.get_width() // 2, box_y + 14))

        can_afford_hp = self.save_data.coins >= HP_COST
        at_max = self.save_data.hp_upgrades >= MAX_HP_UPGRADES
        price_color = (50, 200, 50) if can_afford_hp and not at_max else (200, 50, 50)
        price_text = self.font_med.render(f"Cost: {HP_COST} coins", True, price_color)
        screen.blit(price_text, (hp_x + box_w // 2 - price_text.get_width() // 2, box_y + 50))

        # Hearts row
        from src.settings import PLAYER_MAX_HP
        current_hp = PLAYER_MAX_HP + self.save_data.hp_upgrades
        total_hearts = PLAYER_MAX_HP + MAX_HP_UPGRADES
        heart_size = 14
        hearts_per_row = 13
        hx_start = hp_x + 18
        hearts_y = box_y + 95
        for h in range(total_hearts):
            hx = hx_start + (h % hearts_per_row) * (heart_size + 3)
            hy = hearts_y + (h // hearts_per_row) * (heart_size + 3)
            if h < PLAYER_MAX_HP:
                color = (200, 50, 50)
            elif h < current_hp:
                color = (50, 200, 50)
            else:
                color = (60, 60, 60)
            pygame.draw.rect(screen, color, (hx, hy, heart_size, heart_size))
            pygame.draw.rect(screen, (30, 30, 30), (hx, hy, heart_size, heart_size), 1)

        progress = self.font_small.render(
            f"{self.save_data.hp_upgrades} / {MAX_HP_UPGRADES} upgrades",
            True, (180, 180, 180)
        )
        screen.blit(progress, (hp_x + box_w // 2 - progress.get_width() // 2, box_y + 160))

        if at_max:
            prompt = self.font_small.render("MAX REACHED", True, (255, 220, 50))
        else:
            prompt = self.font_small.render("ENTER to buy", True, (200, 200, 200))
        screen.blit(prompt, (hp_x + box_w // 2 - prompt.get_width() // 2, box_y + 185))

        # --- Totem of Undying box ---
        totem_x = start_x + box_w + gap
        totem_selected = self.selected == 1
        border_color_t = (255, 220, 50) if totem_selected else (100, 80, 150)
        pygame.draw.rect(screen, (40, 35, 60), (totem_x, box_y, box_w, box_h))
        pygame.draw.rect(screen, border_color_t, (totem_x, box_y, box_w, box_h), 3)

        totem_title = self.font_med.render("Totem of Undying", True, (255, 180, 80))
        screen.blit(totem_title, (totem_x + box_w // 2 - totem_title.get_width() // 2, box_y + 14))

        can_afford_t = self.save_data.coins >= TOTEM_COST
        t_price_color = (50, 200, 50) if can_afford_t else (200, 50, 50)
        t_price = self.font_med.render(f"Cost: {TOTEM_COST} coins", True, t_price_color)
        screen.blit(t_price, (totem_x + box_w // 2 - t_price.get_width() // 2, box_y + 50))

        pack_text = self.font_small.render(f"→ get {TOTEM_PACK} totems", True, (200, 200, 200))
        screen.blit(pack_text, (totem_x + box_w // 2 - pack_text.get_width() // 2, box_y + 82))

        desc1 = self.font_small.render("Survive death once per totem.", True, (160, 160, 180))
        screen.blit(desc1, (totem_x + box_w // 2 - desc1.get_width() // 2, box_y + 108))
        desc2 = self.font_small.render("Respawn at last safe spot.", True, (160, 160, 180))
        screen.blit(desc2, (totem_x + box_w // 2 - desc2.get_width() // 2, box_y + 128))

        owned_color = (255, 220, 50) if self.save_data.totems > 0 else (130, 130, 130)
        owned_text = self.font_med.render(f"Owned: {self.save_data.totems}", True, owned_color)
        screen.blit(owned_text, (totem_x + box_w // 2 - owned_text.get_width() // 2, box_y + 158))

        t_prompt = self.font_small.render("ENTER to buy", True, (200, 200, 200))
        screen.blit(t_prompt, (totem_x + box_w // 2 - t_prompt.get_width() // 2, box_y + 185))

        # ── Feedback message ────────────────────────────────────────
        if self.message_timer > 0:
            self.message_timer -= 1
            ok = "upgraded" in self.message or "Totems" in self.message
            msg_color = (50, 200, 50) if ok else (200, 50, 50)
            msg_text = self.font_med.render(self.message, True, msg_color)
            screen.blit(msg_text, (SCREEN_WIDTH // 2 - msg_text.get_width() // 2, box_y + box_h + 20))

        # Close hint
        close_text = self.font_small.render("Press ESC or S to go back", True, (120, 120, 120))
        screen.blit(close_text, (SCREEN_WIDTH // 2 - close_text.get_width() // 2, SCREEN_HEIGHT - 30))
