from src.settings import *
from src.world.platforms import Platform
from src.entities.enemies import Wasp, Fly, Spider


def scale_enemies(enemies, hp_multiplier, speed_multiplier=1.0):
    """Scale enemy stats for harder islands. Multiplies HP and optionally speed."""
    for e in enemies:
        e.hp = max(1, round(e.hp * hp_multiplier))
        if hasattr(e, 'speed'):
            e.speed *= speed_multiplier
    return enemies


def create_level(island, level):
    """Return (platforms, enemies) for the given island and level-within-island.

    island 0 = The Garden Isles (3 levels)
    island 1 = The Swamp (4 levels)
    """
    theme = LEVEL_THEMES[island][level]
    color = theme["platform"]

    # =========================================================================
    # ISLAND 0 — The Garden Isles
    # =========================================================================
    if island == 0:
        if level == 0:  # The Garden
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

        elif level == 1:  # The Hive
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

        elif level == 2:  # The Throne Room
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

    # =========================================================================
    # ISLAND 1 — The Swamp
    # =========================================================================
    elif island == 1:
        if level == 0:  # Murky Shallows — intro to swamp, mostly wasps
            platforms = [
                Platform(0, 540, 500, 60, color),
                Platform(300, 440, 120, 20, color),
                Platform(550, 480, 100, 20, color),
                Platform(700, 540, 300, 60, color),
                Platform(850, 420, 150, 20, color),
                Platform(1100, 540, 400, 60, color),
                Platform(1250, 400, 120, 20, color),
                Platform(1500, 540, 300, 60, color),
                Platform(1650, 440, 100, 20, color),
                Platform(1850, 540, 400, 60, color),
                Platform(2100, 480, 150, 20, color),
                Platform(2300, 540, 300, 60, color),
            ]
            enemies = scale_enemies([
                Wasp(200, 540 - 24, 100, 450),
                Wasp(750, 540 - 24, 700, 950),
                Fly(900, 360, 850, 1100),
                Wasp(1200, 540 - 24, 1100, 1450),
                Wasp(1600, 540 - 24, 1500, 1800),
                Fly(1700, 380, 1650, 1900),
                Wasp(2350, 540 - 24, 2300, 2550),
            ], hp_multiplier=1.5)

        elif level == 1:  # Twisted Roots — wasps + flies + spiders, more vertical
            platforms = [
                Platform(0, 540, 400, 60, color),
                Platform(200, 420, 100, 20, color),
                Platform(350, 320, 120, 20, color),
                Platform(500, 440, 150, 20, color),
                Platform(650, 540, 250, 60, color),
                Platform(800, 380, 100, 20, color),
                Platform(950, 280, 120, 20, color),
                Platform(1100, 400, 100, 20, color),
                Platform(1250, 540, 300, 60, color),
                Platform(1400, 420, 120, 20, color),
                Platform(1550, 320, 100, 20, color),
                Platform(1700, 440, 150, 20, color),
                Platform(1900, 540, 350, 60, color),
                Platform(2100, 380, 120, 20, color),
                Platform(2300, 540, 400, 60, color),
                Platform(2550, 440, 100, 20, color),
                Platform(2700, 540, 200, 60, color),
            ]
            enemies = scale_enemies([
                Wasp(150, 540 - 24, 50, 350),
                Fly(400, 260, 350, 550),
                Spider(550, 440 - 28, 500, 650),
                Wasp(700, 540 - 24, 650, 850),
                Fly(1000, 220, 950, 1150),
                Spider(1300, 540 - 28, 1250, 1500),
                Wasp(1450, 420 - 24, 1400, 1600),
                Fly(1600, 260, 1550, 1750),
                Spider(1950, 540 - 28, 1900, 2200),
                Wasp(2150, 380 - 24, 2100, 2350),
                Fly(2400, 380, 2300, 2600),
            ], hp_multiplier=1.5)

        elif level == 2:  # Poison Bog — hardest regular level, tricky layouts
            platforms = [
                Platform(0, 540, 300, 60, color),
                Platform(180, 430, 80, 20, color),
                Platform(350, 350, 100, 20, color),
                Platform(500, 540, 150, 60, color),
                Platform(600, 420, 80, 20, color),
                Platform(750, 300, 100, 20, color),
                Platform(900, 400, 80, 20, color),
                Platform(1050, 540, 200, 60, color),
                Platform(1200, 380, 100, 20, color),
                Platform(1350, 280, 120, 20, color),
                Platform(1500, 420, 80, 20, color),
                Platform(1650, 540, 250, 60, color),
                Platform(1800, 380, 100, 20, color),
                Platform(1950, 280, 80, 20, color),
                Platform(2100, 400, 120, 20, color),
                Platform(2300, 540, 300, 60, color),
                Platform(2500, 420, 100, 20, color),
                Platform(2650, 320, 80, 20, color),
                Platform(2800, 540, 300, 60, color),
                Platform(3000, 440, 100, 20, color),
                Platform(3150, 540, 200, 60, color),
            ]
            enemies = scale_enemies([
                Wasp(100, 540 - 24, 50, 250),
                Spider(400, 350 - 28, 350, 500),
                Fly(550, 360, 500, 650),
                Wasp(650, 540 - 24, 500, 700),
                Spider(800, 300 - 28, 750, 900),
                Fly(950, 340, 900, 1100),
                Wasp(1100, 540 - 24, 1050, 1250),
                Spider(1250, 380 - 28, 1200, 1400),
                Fly(1400, 220, 1350, 1550),
                Wasp(1700, 540 - 24, 1650, 1880),
                Spider(1850, 380 - 28, 1800, 2000),
                Fly(2000, 220, 1950, 2150),
                Wasp(2350, 540 - 24, 2300, 2550),
                Spider(2550, 420 - 28, 2500, 2700),
                Fly(2700, 260, 2650, 2850),
                Wasp(2900, 540 - 24, 2800, 3050),
            ], hp_multiplier=1.5)

        elif level == 3:  # Beetle Lord's Lair — boss arena at the end
            platforms = [
                Platform(0, 540, 400, 60, color),
                Platform(250, 420, 100, 20, color),
                Platform(450, 350, 120, 20, color),
                Platform(600, 460, 100, 20, color),
                Platform(750, 540, 200, 60, color),
                Platform(950, 380, 100, 20, color),
                Platform(1100, 300, 80, 20, color),
                Platform(1250, 420, 100, 20, color),
                Platform(1400, 540, 200, 60, color),
                # Boss arena — wide flat area
                Platform(1700, 540, 1000, 60, color),
            ]
            enemies = scale_enemies([
                Wasp(200, 540 - 24, 100, 350),
                Fly(500, 290, 450, 650),
                Spider(800, 540 - 28, 750, 920),
                Wasp(1000, 380 - 24, 950, 1150),
                Fly(1150, 240, 1100, 1300),
                Wasp(1450, 540 - 24, 1400, 1580),
            ], hp_multiplier=1.5)
        else:
            platforms = []
            enemies = []

    # =========================================================================
    # Fallback for unbuilt islands
    # =========================================================================
    else:
        platforms = []
        enemies = []

    return platforms, enemies


def check_level_complete(player, enemies, island=0, level=0):
    """Check if all enemies are dead and player reached end of level."""
    all_dead = all(not e.alive and e.death_timer <= 0 for e in enemies)
    # Swamp levels are longer, so the end-of-level threshold needs to be further right
    if island == 1 and level == 2:
        end_x = 3050  # Poison Bog is the longest
    elif island == 1:
        end_x = 2200  # Other swamp levels
    else:
        end_x = 1900  # Island 0 levels
    past_end = player.rect.x > end_x
    return all_dead and past_end
