import pygame
import os
from src.settings import *


class ParallaxBackground:
    """Parallax scrolling background. Pass a level_num (0,1,2) or a theme
    string like "swamp" to pick which sprite set to load."""

    # Maps theme names to (sky_color, sprite_prefix)
    THEMES = {
        "garden":  ((135, 200, 235), "bg_garden"),
        "hive":    ((110, 80, 20),   "bg_hive"),
        "tower":   ((60, 20, 20),    "bg_tower"),
        "swamp":   ((40, 60, 35),    "bg_swamp"),
        "cave":    ((20, 12, 40),    "bg_cave"),
        "volcano": ((80, 30, 10),    "bg_volcano"),
    }

    def __init__(self, level_or_theme):
        self.layers = []

        # If given a string, use it as a theme name directly
        if isinstance(level_or_theme, str):
            theme_key = level_or_theme
        else:
            # Old-style numeric: 0=garden, 1=hive, 2+=tower
            theme_key = {0: "garden", 1: "hive"}.get(level_or_theme, "tower")

        sky, prefix = self.THEMES.get(theme_key, self.THEMES["garden"])
        self.sky_color = sky
        try:
            l1 = pygame.image.load(os.path.join("sprites", f"{prefix}_1.png")).convert_alpha()
            l2 = pygame.image.load(os.path.join("sprites", f"{prefix}_2.png")).convert_alpha()
            l3 = pygame.image.load(os.path.join("sprites", f"{prefix}_3.png")).convert_alpha()
            self.layers = [(l1, 0.15), (l2, 0.4), (l3, 0.7)]
        except Exception:
            pass

    def draw(self, screen, camera_x):
        screen.fill(self.sky_color)
        for img, speed in self.layers:
            w = img.get_width()
            offset_x = (camera_x * speed) % w
            screen.blit(img, (-offset_x, 0))
            if offset_x > 0:
                screen.blit(img, (-offset_x + w, 0))

class Camera:
    def __init__(self):
        self.x = 0

    def update(self, player):
        # Camera follows player, keeping them in the left third of the screen
        target_x = player.rect.centerx - SCREEN_WIDTH // 3
        self.x += (target_x - self.x) * 0.1  # Smooth follow (lerp)
        if self.x < 0:
            self.x = 0  # Don't scroll left past the start of the world
