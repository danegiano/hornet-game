from src.settings import *
from src.world.platforms import Platform
from src.entities.enemies import Wasp, Fly, Spider


def create_level(level_num):
    """Return (platforms, enemies) for the given level number (0-indexed)."""
    theme = LEVEL_THEMES[level_num]
    color = theme["platform"]

    if level_num == 0:  # The Garden
        platforms = [
            Platform(0, 540, 600, 60, color),
            Platform(250, 440, 150, 20, color),
            Platform(500, 380, 200, 20, color),
            Platform(750, 540, 400, 60, color),
            Platform(900, 440, 150, 20, color),
            Platform(1200, 540, 600, 60, color),
            Platform(1400, 420, 150, 20, color),
            Platform(1700, 540, 400, 60, color),
            Platform(2000, 540, 200, 60, color),
        ]
        enemies = [
            Wasp(300, 540 - 24, 250, 500),
            Wasp(800, 540 - 24, 750, 1050),
            Wasp(1300, 540 - 24, 1200, 1500),
            Wasp(1750, 540 - 24, 1700, 1950),
        ]
    elif level_num == 1:  # The Hive
        platforms = [
            Platform(0, 540, 300, 60, color),
            Platform(200, 420, 120, 20, color),
            Platform(400, 340, 120, 20, color),
            Platform(550, 450, 150, 20, color),
            Platform(750, 540, 200, 60, color),
            Platform(850, 380, 120, 20, color),
            Platform(1050, 300, 150, 20, color),
            Platform(1250, 420, 120, 20, color),
            Platform(1400, 540, 300, 60, color),
            Platform(1600, 380, 150, 20, color),
            Platform(1850, 540, 400, 60, color),
        ]
        enemies = [
            Wasp(100, 540 - 24, 50, 250),
            Wasp(800, 540 - 24, 750, 900),
            Fly(450, 280, 400, 600),
            Fly(900, 320, 850, 1100),
            Fly(1650, 320, 1600, 1850),
            Wasp(1500, 540 - 24, 1400, 1650),
        ]
    elif level_num == 2:  # The Throne Room
        platforms = [
            Platform(0, 540, 300, 60, color),
            Platform(200, 420, 100, 20, color),
            Platform(400, 350, 80, 20, color),
            Platform(550, 440, 100, 20, color),
            Platform(700, 540, 150, 60, color),
            Platform(900, 380, 100, 20, color),
            Platform(1050, 300, 100, 20, color),
            Platform(1200, 420, 80, 20, color),
            Platform(1350, 540, 200, 60, color),
            Platform(1500, 400, 100, 20, color),
            Platform(1700, 540, 800, 60, color),  # Boss arena
        ]
        enemies = [
            Wasp(100, 540 - 24, 50, 250),
            Spider(450, 350 - 28, 400, 530),
            Fly(600, 380, 550, 750),
            Wasp(750, 540 - 24, 700, 830),
            Spider(950, 380 - 28, 900, 1050),
            Fly(1100, 250, 1050, 1250),
            Wasp(1400, 540 - 24, 1350, 1530),
        ]
    else:
        platforms = []
        enemies = []

    return platforms, enemies


def check_level_complete(player, enemies):
    """Check if all enemies are dead and player reached end of level."""
    all_dead = all(not e.alive and e.death_timer <= 0 for e in enemies)
    # Player past the rightmost reasonable point
    past_end = player.rect.x > 1900
    return all_dead and past_end
