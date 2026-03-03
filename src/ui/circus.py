import pygame
import math
from src.settings import *


class CircusLobby:
    """The Circus intro screen — shows boss order, rules, lets player start."""

    BOSS_NAMES = [
        "Wasp King",
        "Swamp Beetle Lord",
        "Crystal Spider Queen",
        "Fire Moth",
        "Shadow Hornet",
    ]

    def __init__(self):
        self.font_big = None
        self.font_med = None
        self.font_small = None
        self.wave = 0

    def _init_fonts(self):
        if self.font_big is None:
            self.font_big   = pygame.font.Font(None, 56)
            self.font_med   = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        """Returns 'start' to begin, 'back' to go back to island map."""
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_RETURN:
            return "start"
        if event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, screen):
        self._init_fonts()
        self.wave += 0.03

        # Dark red background
        screen.fill((25, 5, 5))

        # Flashing title
        pulse = abs(math.sin(self.wave * 2))
        r = int(200 + pulse * 55)
        title = self.font_big.render("THE CIRCUS", True, (r, 60, 60))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        sub = self.font_med.render("BOSS RUSH", True, (200, 150, 150))
        screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 90))

        # Rules
        rules = [
            "Fight all 5 bosses — stronger than ever.",
            "One life. Die once and you start over.",
            "Beat them all to open the portal.",
        ]
        ry = 140
        for rule in rules:
            rt = self.font_small.render(rule, True, (200, 180, 180))
            screen.blit(rt, (SCREEN_WIDTH // 2 - rt.get_width() // 2, ry))
            ry += 26

        # Boss list
        by = 260
        list_title = self.font_med.render("BOSSES:", True, (220, 100, 100))
        screen.blit(list_title, (SCREEN_WIDTH // 2 - list_title.get_width() // 2, by))
        by += 36
        for i, name in enumerate(self.BOSS_NAMES):
            bt = self.font_small.render(f"{i+1}. {name}", True, (200, 160, 160))
            screen.blit(bt, (SCREEN_WIDTH // 2 - bt.get_width() // 2, by))
            by += 26

        # Prompt
        blink = int(self.wave * 3) % 2 == 0
        if blink:
            prompt = self.font_med.render("ENTER to begin  |  ESC to go back", True, (255, 200, 200))
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT - 50))


class CircusFail:
    """Screen shown when player dies in the circus."""

    def __init__(self, boss_reached):
        self.boss_reached = boss_reached  # 0-indexed, how far they got
        self.font_big = None
        self.font_med = None
        self.font_small = None

    def _init_fonts(self):
        if self.font_big is None:
            self.font_big   = pygame.font.Font(None, 56)
            self.font_med   = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        """Returns 'retry' or 'back'."""
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_RETURN:
            return "retry"
        if event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, screen):
        self._init_fonts()
        screen.fill((20, 0, 0))

        title = self.font_big.render("YOU FELL.", True, (200, 50, 50))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        msg = self.font_med.render(f"Reached boss {self.boss_reached + 1} of 5", True, (180, 130, 130))
        screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))

        sub = self.font_small.render("The circus starts over...", True, (150, 100, 100))
        screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 250))

        prompt = self.font_med.render("ENTER to try again  |  ESC to leave", True, (200, 160, 160))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT - 80))


class CircusWin:
    """Screen shown when player beats all 5 circus bosses."""

    def __init__(self):
        self.font_big = None
        self.font_med = None
        self.font_small = None
        self.wave = 0

    def _init_fonts(self):
        if self.font_big is None:
            self.font_big   = pygame.font.Font(None, 56)
            self.font_med   = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        """Returns 'enter_portal' or 'back'."""
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_RETURN:
            return "enter_portal"
        if event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, screen):
        self._init_fonts()
        self.wave += 0.03
        screen.fill((5, 0, 20))

        pulse = abs(math.sin(self.wave * 2))
        r = int(100 + pulse * 100)
        b = int(200 + pulse * 55)
        title = self.font_big.render("YOU CONQUERED THE CIRCUS!", True, (r, 50, b))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        msg = self.font_med.render("The portal to Hallucination Land is open.", True, (180, 150, 220))
        screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 210))

        prompt = self.font_med.render("ENTER to enter the portal", True, (200, 180, 255))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT - 80))
