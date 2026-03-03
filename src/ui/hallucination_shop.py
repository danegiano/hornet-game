import pygame
from src.settings import *
from src.systems.powers import (
    HALLUCINATION_ISLAND_POWER,
    SHADOW_POWER_COST,
    SHADOW_POWER_DESC,
)

HSHOP_LIFE_COST  = 100
HSHOP_LIFE_STOCK = 10


class HallucinationShop:
    """Special shop in Hallucination Land. Sells lives + shadow powers."""

    def __init__(self, save_data, island_index):
        self.save_data = save_data
        self.island_index = island_index
        self.font_big = None
        self.font_med = None
        self.font_small = None
        self.message = ""
        self.message_timer = 0
        self.selected = 0   # 0 = lives, 1 = shadow power

        self.shadow_power = HALLUCINATION_ISLAND_POWER.get(island_index)

    def _init_fonts(self):
        if self.font_big is None:
            self.font_big   = pygame.font.Font(None, 48)
            self.font_med   = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        """Returns "close" to go back, None otherwise."""
        if event.type != pygame.KEYDOWN:
            return None
        if event.key in (pygame.K_ESCAPE, pygame.K_s):
            return "close"
        elif event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % 2
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % 2
        elif event.key == pygame.K_RETURN:
            if self.selected == 0:
                self._buy_life()
            else:
                self._buy_shadow_power()
        return None

    def _buy_life(self):
        if self.save_data.hallucination_lives >= HSHOP_LIFE_STOCK:
            self.message = "Already at max lives!"
        elif self.save_data.coins < HSHOP_LIFE_COST:
            self.message = "Not enough coins!"
        else:
            self.save_data.coins -= HSHOP_LIFE_COST
            self.save_data.hallucination_lives += 1
            self.save_data.save()
            self.message = "Got 1 extra life!"
        self.message_timer = 90

    def _buy_shadow_power(self):
        if self.shadow_power is None:
            return
        if self.save_data.has_shadow_power(self.shadow_power):
            self.message = "Already have this power!"
        elif self.save_data.coins < SHADOW_POWER_COST[self.shadow_power]:
            self.message = "Not enough coins!"
        else:
            self.save_data.coins -= SHADOW_POWER_COST[self.shadow_power]
            self.save_data.unlock_shadow_power(self.shadow_power)
            self.save_data.save()
            self.message = "Shadow power unlocked!"
        self.message_timer = 90

    def draw(self, screen):
        self._init_fonts()
        screen.fill((5, 0, 20))

        title = self.font_big.render("SHADOW SHOP", True, (160, 80, 220))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        coin_t = self.font_med.render(f"Coins: {self.save_data.coins}", True, (200, 180, 255))
        screen.blit(coin_t, (SCREEN_WIDTH // 2 - coin_t.get_width() // 2, 80))

        nav = self.font_small.render("UP/DOWN to select  |  ENTER to buy  |  ESC to go back", True, (120, 90, 160))
        screen.blit(nav, (SCREEN_WIDTH // 2 - nav.get_width() // 2, 112))

        box_w, box_h = 280, 220
        gap = 40
        total_w = box_w * 2 + gap
        start_x = SCREEN_WIDTH // 2 - total_w // 2
        box_y = 148

        # --- Lives box ---
        lx = start_x
        lc = (180, 100, 255) if self.selected == 0 else (70, 40, 100)
        pygame.draw.rect(screen, (20, 10, 40), (lx, box_y, box_w, box_h))
        pygame.draw.rect(screen, lc, (lx, box_y, box_w, box_h), 3)

        lt = self.font_med.render("+1 Life", True, WHITE)
        screen.blit(lt, (lx + box_w//2 - lt.get_width()//2, box_y + 14))

        can_afford = self.save_data.coins >= HSHOP_LIFE_COST
        at_max = self.save_data.hallucination_lives >= HSHOP_LIFE_STOCK
        pc = (50, 200, 50) if can_afford and not at_max else (200, 50, 50)
        pt = self.font_med.render(f"Cost: {HSHOP_LIFE_COST} coins", True, pc)
        screen.blit(pt, (lx + box_w//2 - pt.get_width()//2, box_y + 50))

        owned_t = self.font_small.render(
            f"Lives: {self.save_data.hallucination_lives} / {HSHOP_LIFE_STOCK}",
            True, (200, 180, 255)
        )
        screen.blit(owned_t, (lx + box_w//2 - owned_t.get_width()//2, box_y + 90))

        desc_t = self.font_small.render("Respawn once in Hallucination Land", True, (160, 140, 200))
        screen.blit(desc_t, (lx + box_w//2 - desc_t.get_width()//2, box_y + 115))

        if at_max:
            pr_t = self.font_small.render("MAX LIVES", True, (255, 220, 50))
        else:
            pr_t = self.font_small.render("ENTER to buy", True, (180, 160, 220))
        screen.blit(pr_t, (lx + box_w//2 - pr_t.get_width()//2, box_y + 190))

        # --- Shadow power box ---
        sx = start_x + box_w + gap
        sc = (180, 100, 255) if self.selected == 1 else (70, 40, 100)
        pygame.draw.rect(screen, (20, 10, 40), (sx, box_y, box_w, box_h))
        pygame.draw.rect(screen, sc, (sx, box_y, box_w, box_h), 3)

        if self.shadow_power:
            power_name = self.shadow_power.replace("_", " ").upper()
            cost = SHADOW_POWER_COST[self.shadow_power]
            desc = SHADOW_POWER_DESC[self.shadow_power]
            already_have = self.save_data.has_shadow_power(self.shadow_power)

            spt = self.font_med.render(power_name, True, (200, 150, 255))
            screen.blit(spt, (sx + box_w//2 - spt.get_width()//2, box_y + 14))

            sp_cost_c = (50, 200, 50) if self.save_data.coins >= cost and not already_have else (200, 50, 50)
            sp_ct = self.font_med.render(f"Cost: {cost} coins", True, sp_cost_c)
            screen.blit(sp_ct, (sx + box_w//2 - sp_ct.get_width()//2, box_y + 50))

            # Simple word-wrap for description
            words = desc.split()
            line, lines_out = "", []
            for w in words:
                if len(line) + len(w) < 30:
                    line += w + " "
                else:
                    lines_out.append(line)
                    line = w + " "
            lines_out.append(line)
            for k, ln in enumerate(lines_out):
                ln_t = self.font_small.render(ln, True, (160, 140, 200))
                screen.blit(ln_t, (sx + box_w//2 - ln_t.get_width()//2, box_y + 90 + k * 22))

            if already_have:
                owned_sp = self.font_small.render("OWNED", True, (255, 220, 50))
                screen.blit(owned_sp, (sx + box_w//2 - owned_sp.get_width()//2, box_y + 190))
            else:
                buy_sp = self.font_small.render("ENTER to buy", True, (180, 160, 220))
                screen.blit(buy_sp, (sx + box_w//2 - buy_sp.get_width()//2, box_y + 190))

        # Feedback message
        if self.message_timer > 0:
            self.message_timer -= 1
            ok = "Got" in self.message or "unlocked" in self.message
            mc = (50, 200, 50) if ok else (200, 50, 50)
            mt = self.font_med.render(self.message, True, mc)
            screen.blit(mt, (SCREEN_WIDTH // 2 - mt.get_width() // 2, box_y + box_h + 20))

        close_t = self.font_small.render("ESC or S to go back", True, (100, 80, 130))
        screen.blit(close_t, (SCREEN_WIDTH // 2 - close_t.get_width() // 2, SCREEN_HEIGHT - 30))
