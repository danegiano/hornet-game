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
    # ISLAND 2 — The Crystal Caves
    # =========================================================================
    elif island == 2:
        if level == 0:  # Crystal Entrance — intro to caves, spiders + wasps
            platforms = [
                Platform(0, 540, 400, 60, color),
                Platform(250, 440, 100, 20, color),
                Platform(420, 360, 80, 20, color),
                Platform(550, 460, 120, 20, color),
                Platform(700, 540, 250, 60, color),
                Platform(800, 420, 80, 20, color),
                Platform(950, 340, 100, 20, color),
                Platform(1100, 440, 80, 20, color),
                Platform(1250, 540, 300, 60, color),
                Platform(1400, 400, 100, 20, color),
                Platform(1550, 320, 80, 20, color),
                Platform(1700, 440, 120, 20, color),
                Platform(1850, 540, 350, 60, color),
                Platform(2100, 460, 100, 20, color),
                Platform(2250, 540, 300, 60, color),
            ]
            enemies = scale_enemies([
                Spider(300, 440 - 28, 250, 400),
                Wasp(600, 460 - 24, 550, 750),
                Spider(850, 420 - 28, 800, 950),
                Wasp(1000, 340 - 24, 950, 1150),
                Spider(1300, 540 - 28, 1250, 1500),
                Wasp(1450, 400 - 24, 1400, 1600),
                Spider(1750, 440 - 28, 1700, 1900),
                Wasp(1950, 540 - 24, 1850, 2150),
                Spider(2300, 540 - 28, 2250, 2500),
            ], hp_multiplier=2.25, speed_multiplier=1.1)

        elif level == 1:  # Amethyst Tunnels — vertical, spiders + flies, tight
            platforms = [
                Platform(0, 540, 300, 60, color),
                Platform(150, 430, 80, 20, color),
                Platform(300, 330, 80, 20, color),
                Platform(180, 250, 80, 20, color),
                Platform(400, 460, 100, 20, color),
                Platform(550, 540, 200, 60, color),
                Platform(600, 380, 80, 20, color),
                Platform(750, 280, 80, 20, color),
                Platform(900, 380, 80, 20, color),
                Platform(850, 480, 100, 20, color),
                Platform(1050, 540, 200, 60, color),
                Platform(1100, 400, 80, 20, color),
                Platform(1250, 300, 80, 20, color),
                Platform(1400, 400, 80, 20, color),
                Platform(1350, 500, 100, 20, color),
                Platform(1550, 540, 250, 60, color),
                Platform(1650, 420, 80, 20, color),
                Platform(1800, 320, 80, 20, color),
                Platform(1950, 440, 100, 20, color),
                Platform(2100, 540, 300, 60, color),
                Platform(2300, 460, 80, 20, color),
                Platform(2450, 540, 200, 60, color),
            ]
            enemies = scale_enemies([
                Spider(200, 430 - 28, 150, 350),
                Fly(350, 270, 300, 500),
                Spider(450, 460 - 28, 400, 550),
                Fly(650, 320, 600, 800),
                Spider(900, 380 - 28, 850, 1000),
                Fly(1150, 240, 1100, 1300),
                Spider(1300, 540 - 28, 1250, 1450),
                Fly(1450, 340, 1400, 1600),
                Spider(1700, 420 - 28, 1650, 1850),
                Fly(1850, 260, 1800, 2000),
                Spider(2150, 540 - 28, 2100, 2350),
                Fly(2350, 400, 2300, 2500),
            ], hp_multiplier=2.25, speed_multiplier=1.1)

        elif level == 2:  # Diamond Depths — mix of all enemies, long + tricky
            platforms = [
                Platform(0, 540, 300, 60, color),
                Platform(200, 430, 80, 20, color),
                Platform(350, 350, 80, 20, color),
                Platform(500, 450, 80, 20, color),
                Platform(630, 540, 200, 60, color),
                Platform(700, 380, 80, 20, color),
                Platform(850, 290, 80, 20, color),
                Platform(1000, 380, 80, 20, color),
                Platform(1100, 480, 100, 20, color),
                Platform(1250, 540, 200, 60, color),
                Platform(1350, 400, 80, 20, color),
                Platform(1500, 310, 100, 20, color),
                Platform(1650, 420, 80, 20, color),
                Platform(1800, 540, 200, 60, color),
                Platform(1900, 380, 80, 20, color),
                Platform(2050, 280, 80, 20, color),
                Platform(2200, 400, 100, 20, color),
                Platform(2350, 500, 80, 20, color),
                Platform(2500, 540, 250, 60, color),
                Platform(2650, 420, 80, 20, color),
                Platform(2800, 320, 80, 20, color),
                Platform(2950, 440, 100, 20, color),
                Platform(3100, 540, 300, 60, color),
                Platform(3300, 460, 80, 20, color),
                Platform(3450, 540, 200, 60, color),
            ]
            enemies = scale_enemies([
                Spider(250, 430 - 28, 200, 400),
                Wasp(400, 350 - 24, 350, 550),
                Fly(550, 390, 500, 700),
                Spider(750, 380 - 28, 700, 900),
                Wasp(900, 290 - 24, 850, 1050),
                Fly(1050, 420, 1000, 1200),
                Spider(1300, 540 - 28, 1250, 1450),
                Wasp(1400, 400 - 24, 1350, 1550),
                Fly(1550, 250, 1500, 1700),
                Spider(1850, 540 - 28, 1800, 2000),
                Wasp(1950, 380 - 24, 1900, 2100),
                Fly(2100, 220, 2050, 2250),
                Spider(2400, 500 - 28, 2350, 2550),
                Wasp(2550, 540 - 24, 2500, 2700),
                Fly(2700, 260, 2650, 2850),
                Spider(3000, 440 - 28, 2950, 3150),
                Wasp(3150, 540 - 24, 3100, 3350),
                Fly(3350, 400, 3300, 3500),
            ], hp_multiplier=2.25, speed_multiplier=1.1)

        elif level == 3:  # Sapphire Cavern — hard, lots of lunging spiders
            platforms = [
                Platform(0, 540, 250, 60, color),
                Platform(150, 440, 80, 20, color),
                Platform(300, 360, 80, 20, color),
                Platform(450, 450, 80, 20, color),
                Platform(580, 540, 180, 60, color),
                Platform(650, 380, 80, 20, color),
                Platform(800, 290, 80, 20, color),
                Platform(950, 400, 80, 20, color),
                Platform(1050, 500, 100, 20, color),
                Platform(1200, 540, 180, 60, color),
                Platform(1300, 400, 80, 20, color),
                Platform(1450, 300, 80, 20, color),
                Platform(1600, 400, 80, 20, color),
                Platform(1700, 500, 100, 20, color),
                Platform(1850, 540, 200, 60, color),
                Platform(1950, 380, 80, 20, color),
                Platform(2100, 280, 80, 20, color),
                Platform(2250, 400, 80, 20, color),
                Platform(2400, 500, 100, 20, color),
                Platform(2550, 540, 200, 60, color),
                Platform(2700, 420, 80, 20, color),
                Platform(2850, 320, 80, 20, color),
                Platform(3000, 440, 80, 20, color),
                Platform(3100, 540, 250, 60, color),
            ]
            enemies = scale_enemies([
                Spider(200, 440 - 28, 150, 350),
                Spider(350, 360 - 28, 300, 500),
                Wasp(500, 450 - 24, 450, 620),
                Spider(700, 380 - 28, 650, 850),
                Spider(850, 290 - 28, 800, 950),
                Fly(1000, 340, 950, 1100),
                Spider(1250, 540 - 28, 1200, 1380),
                Spider(1350, 400 - 28, 1300, 1500),
                Wasp(1500, 300 - 24, 1450, 1650),
                Spider(1650, 400 - 28, 1600, 1750),
                Spider(1900, 540 - 28, 1850, 2050),
                Fly(2000, 320, 1950, 2150),
                Spider(2150, 280 - 28, 2100, 2300),
                Spider(2300, 400 - 28, 2250, 2450),
                Wasp(2600, 540 - 24, 2550, 2750),
                Spider(2750, 420 - 28, 2700, 2900),
                Spider(2900, 320 - 28, 2850, 3050),
                Spider(3050, 440 - 28, 3000, 3200),
            ], hp_multiplier=2.25, speed_multiplier=1.15)

        elif level == 4:  # Spider Queen's Web — regular enemies + boss arena
            platforms = [
                Platform(0, 540, 350, 60, color),
                Platform(200, 430, 80, 20, color),
                Platform(400, 350, 100, 20, color),
                Platform(550, 460, 80, 20, color),
                Platform(700, 540, 200, 60, color),
                Platform(800, 380, 80, 20, color),
                Platform(1000, 300, 80, 20, color),
                Platform(1150, 420, 80, 20, color),
                Platform(1300, 540, 200, 60, color),
                Platform(1500, 400, 100, 20, color),
                # Boss arena — wide flat area
                Platform(1800, 540, 1000, 60, color),
            ]
            enemies = scale_enemies([
                Spider(250, 430 - 28, 200, 400),
                Wasp(450, 350 - 24, 400, 600),
                Spider(600, 460 - 28, 550, 720),
                Fly(850, 320, 800, 1050),
                Spider(1050, 300 - 28, 1000, 1200),
                Wasp(1200, 420 - 24, 1150, 1350),
                Spider(1350, 540 - 28, 1300, 1500),
            ], hp_multiplier=2.25, speed_multiplier=1.1)
        else:
            platforms = []
            enemies = []

    # =========================================================================
    # ISLAND 3 — The Volcano
    # =========================================================================
    elif island == 3:
        if level == 0:  # Lava Flats — intro level, wasps and flies, lava gaps
            platforms = [
                Platform(0, 540, 400, 60, color),
                Platform(250, 440, 120, 20, color),
                # Gap! No platform below = death
                Platform(550, 540, 300, 60, color),
                Platform(700, 420, 100, 20, color),
                Platform(900, 540, 200, 60, color),
                # Wide lava gap
                Platform(1200, 540, 350, 60, color),
                Platform(1350, 420, 120, 20, color),
                Platform(1550, 480, 100, 20, color),
                Platform(1700, 540, 300, 60, color),
                # Another gap
                Platform(2100, 540, 250, 60, color),
                Platform(2200, 420, 100, 20, color),
                Platform(2400, 540, 400, 60, color),
            ]
            enemies = scale_enemies([
                Wasp(200, 540 - 24, 100, 350),
                Fly(600, 360, 550, 800),
                Wasp(700, 540 - 24, 550, 850),
                Fly(1000, 400, 900, 1150),
                Wasp(1300, 540 - 24, 1200, 1500),
                Fly(1400, 360, 1350, 1600),
                Wasp(1800, 540 - 24, 1700, 1950),
                Fly(2150, 360, 2100, 2350),
                Wasp(2500, 540 - 24, 2400, 2700),
            ], hp_multiplier=3.375, speed_multiplier=1.2)

        elif level == 1:  # Magma Tunnels — more enemies, tighter platforms, vertical
            platforms = [
                Platform(0, 540, 300, 60, color),
                Platform(180, 430, 80, 20, color),
                Platform(320, 340, 80, 20, color),
                Platform(460, 440, 100, 20, color),
                # Gap
                Platform(620, 540, 200, 60, color),
                Platform(680, 380, 80, 20, color),
                Platform(830, 280, 100, 20, color),
                Platform(980, 400, 80, 20, color),
                Platform(1100, 540, 250, 60, color),
                # Ascending section
                Platform(1250, 460, 80, 20, color),
                Platform(1380, 380, 80, 20, color),
                Platform(1500, 300, 100, 20, color),
                Platform(1650, 400, 80, 20, color),
                # Gap
                Platform(1800, 540, 200, 60, color),
                Platform(1950, 420, 100, 20, color),
                Platform(2100, 340, 80, 20, color),
                Platform(2250, 460, 100, 20, color),
                Platform(2400, 540, 300, 60, color),
                Platform(2600, 420, 80, 20, color),
                Platform(2750, 540, 200, 60, color),
            ]
            enemies = scale_enemies([
                Wasp(100, 540 - 24, 50, 250),
                Fly(370, 280, 320, 520),
                Wasp(650, 540 - 24, 620, 800),
                Spider(880, 280 - 28, 830, 980),
                Fly(1030, 340, 980, 1200),
                Wasp(1150, 540 - 24, 1100, 1300),
                Fly(1430, 320, 1380, 1550),
                Spider(1550, 300 - 28, 1500, 1650),
                Wasp(1850, 540 - 24, 1800, 1980),
                Fly(2000, 360, 1950, 2150),
                Spider(2150, 340 - 28, 2100, 2300),
                Wasp(2450, 540 - 24, 2400, 2650),
            ], hp_multiplier=3.375, speed_multiplier=1.2)

        elif level == 2:  # Ember Caverns — hard mix, long level, lots of spiders
            platforms = [
                Platform(0, 540, 250, 60, color),
                Platform(150, 440, 80, 20, color),
                Platform(300, 360, 80, 20, color),
                # Gap
                Platform(450, 540, 200, 60, color),
                Platform(550, 400, 80, 20, color),
                Platform(700, 300, 100, 20, color),
                Platform(850, 420, 80, 20, color),
                Platform(1000, 540, 200, 60, color),
                # Gap
                Platform(1300, 540, 180, 60, color),
                Platform(1350, 400, 80, 20, color),
                Platform(1500, 300, 80, 20, color),
                Platform(1650, 400, 80, 20, color),
                Platform(1800, 540, 200, 60, color),
                # Gap
                Platform(2100, 480, 100, 20, color),
                Platform(2250, 540, 200, 60, color),
                Platform(2350, 400, 80, 20, color),
                Platform(2500, 300, 100, 20, color),
                Platform(2650, 420, 80, 20, color),
                Platform(2800, 540, 250, 60, color),
                # Gap
                Platform(3150, 540, 200, 60, color),
                Platform(3250, 420, 80, 20, color),
                Platform(3400, 540, 300, 60, color),
            ]
            enemies = scale_enemies([
                Spider(200, 440 - 28, 150, 350),
                Spider(350, 360 - 28, 300, 450),
                Wasp(500, 540 - 24, 450, 650),
                Spider(600, 400 - 28, 550, 750),
                Fly(750, 240, 700, 900),
                Spider(900, 420 - 28, 850, 1050),
                Wasp(1050, 540 - 24, 1000, 1200),
                Spider(1400, 400 - 28, 1350, 1550),
                Spider(1550, 300 - 28, 1500, 1700),
                Fly(1700, 340, 1650, 1850),
                Wasp(1850, 540 - 24, 1800, 2000),
                Spider(2150, 480 - 28, 2100, 2300),
                Spider(2400, 400 - 28, 2350, 2550),
                Fly(2550, 240, 2500, 2700),
                Spider(2700, 420 - 28, 2650, 2850),
                Wasp(2850, 540 - 24, 2800, 3050),
                Spider(3200, 540 - 28, 3150, 3350),
                Spider(3450, 540 - 28, 3400, 3650),
            ], hp_multiplier=3.375, speed_multiplier=1.2)

        elif level == 3:  # Inferno Pit — very hard, dense enemies, tricky jumps
            platforms = [
                Platform(0, 540, 200, 60, color),
                Platform(130, 440, 70, 20, color),
                Platform(270, 350, 70, 20, color),
                # Gap
                Platform(420, 540, 150, 60, color),
                Platform(500, 400, 70, 20, color),
                Platform(640, 300, 80, 20, color),
                # Gap
                Platform(800, 540, 150, 60, color),
                Platform(870, 420, 70, 20, color),
                Platform(1010, 320, 80, 20, color),
                Platform(1150, 440, 70, 20, color),
                Platform(1280, 540, 180, 60, color),
                # Ascending gauntlet
                Platform(1400, 460, 70, 20, color),
                Platform(1530, 380, 70, 20, color),
                Platform(1660, 300, 80, 20, color),
                Platform(1800, 400, 70, 20, color),
                # Gap
                Platform(1950, 540, 180, 60, color),
                Platform(2050, 420, 80, 20, color),
                Platform(2200, 340, 70, 20, color),
                Platform(2350, 460, 80, 20, color),
                Platform(2500, 540, 200, 60, color),
                # Gap
                Platform(2800, 540, 200, 60, color),
                Platform(2900, 400, 80, 20, color),
                Platform(3050, 540, 250, 60, color),
            ]
            enemies = scale_enemies([
                Wasp(80, 540 - 24, 50, 180),
                Spider(180, 440 - 28, 130, 300),
                Fly(320, 290, 270, 470),
                Wasp(450, 540 - 24, 420, 570),
                Spider(550, 400 - 28, 500, 690),
                Fly(690, 240, 640, 850),
                Wasp(830, 540 - 24, 800, 950),
                Spider(920, 420 - 28, 870, 1060),
                Spider(1060, 320 - 28, 1010, 1200),
                Wasp(1300, 540 - 24, 1280, 1450),
                Fly(1450, 400, 1400, 1580),
                Spider(1580, 380 - 28, 1530, 1710),
                Fly(1710, 240, 1660, 1850),
                Wasp(1980, 540 - 24, 1950, 2100),
                Spider(2100, 420 - 28, 2050, 2250),
                Spider(2250, 340 - 28, 2200, 2400),
                Wasp(2400, 460 - 24, 2350, 2550),
                Fly(2550, 480, 2500, 2750),
                Spider(2850, 540 - 28, 2800, 3000),
                Wasp(3100, 540 - 24, 3050, 3250),
            ], hp_multiplier=3.375, speed_multiplier=1.2)

        elif level == 4:  # Ash Wastes — gauntlet level, many enemies in sequence
            platforms = [
                Platform(0, 540, 350, 60, color),
                Platform(200, 440, 100, 20, color),
                # Gap
                Platform(450, 540, 250, 60, color),
                Platform(550, 400, 100, 20, color),
                Platform(750, 540, 250, 60, color),
                Platform(850, 420, 80, 20, color),
                # Gap
                Platform(1050, 540, 300, 60, color),
                Platform(1150, 400, 100, 20, color),
                Platform(1350, 540, 250, 60, color),
                Platform(1450, 420, 80, 20, color),
                # Gap
                Platform(1650, 540, 250, 60, color),
                Platform(1750, 380, 100, 20, color),
                Platform(1950, 540, 250, 60, color),
                Platform(2050, 440, 80, 20, color),
                # Gap
                Platform(2250, 540, 300, 60, color),
                Platform(2400, 400, 100, 20, color),
                Platform(2600, 540, 300, 60, color),
                Platform(2750, 420, 80, 20, color),
                Platform(2900, 540, 250, 60, color),
                # Gap
                Platform(3250, 540, 250, 60, color),
                Platform(3400, 440, 100, 20, color),
                Platform(3550, 540, 200, 60, color),
            ]
            enemies = scale_enemies([
                Wasp(100, 540 - 24, 50, 300),
                Wasp(250, 440 - 24, 200, 400),
                Spider(500, 540 - 28, 450, 700),
                Fly(600, 340, 550, 750),
                Wasp(800, 540 - 24, 750, 950),
                Spider(900, 420 - 28, 850, 1000),
                Wasp(1100, 540 - 24, 1050, 1300),
                Fly(1200, 340, 1150, 1400),
                Spider(1400, 540 - 28, 1350, 1550),
                Wasp(1500, 420 - 24, 1450, 1600),
                Fly(1700, 320, 1650, 1850),
                Spider(1800, 380 - 28, 1750, 1950),
                Wasp(2000, 540 - 24, 1950, 2150),
                Spider(2100, 440 - 28, 2050, 2200),
                Fly(2300, 340, 2250, 2500),
                Wasp(2450, 400 - 24, 2400, 2600),
                Spider(2650, 540 - 28, 2600, 2850),
                Wasp(2800, 420 - 24, 2750, 2950),
                Fly(2950, 480, 2900, 3150),
                Spider(3300, 540 - 28, 3250, 3450),
                Wasp(3450, 440 - 24, 3400, 3600),
                Fly(3550, 480, 3500, 3700),
            ], hp_multiplier=3.375, speed_multiplier=1.2)

        elif level == 5:  # Moth's Furnace — regular enemies + boss arena at end
            platforms = [
                Platform(0, 540, 350, 60, color),
                Platform(200, 430, 100, 20, color),
                Platform(400, 350, 80, 20, color),
                # Gap
                Platform(580, 540, 200, 60, color),
                Platform(650, 400, 80, 20, color),
                Platform(830, 300, 100, 20, color),
                Platform(1000, 420, 80, 20, color),
                Platform(1150, 540, 200, 60, color),
                # Gap
                Platform(1450, 540, 200, 60, color),
                Platform(1550, 400, 100, 20, color),
                Platform(1750, 540, 200, 60, color),
                # Boss arena — wide flat area (the volcano crater)
                Platform(2050, 540, 1200, 60, color),
            ]
            enemies = scale_enemies([
                Wasp(150, 540 - 24, 50, 300),
                Fly(450, 290, 400, 600),
                Spider(620, 540 - 28, 580, 770),
                Wasp(700, 400 - 24, 650, 850),
                Fly(880, 240, 830, 1050),
                Spider(1050, 420 - 28, 1000, 1200),
                Wasp(1200, 540 - 24, 1150, 1350),
                Fly(1500, 340, 1450, 1650),
                Wasp(1600, 540 - 24, 1550, 1750),
            ], hp_multiplier=3.375, speed_multiplier=1.2)

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
    # Each island/level can have a different end-of-level threshold
    if island == 1 and level == 2:
        end_x = 3050  # Poison Bog is the longest
    elif island == 1:
        end_x = 2200  # Other swamp levels
    elif island == 2 and level == 2:
        end_x = 3350  # Diamond Depths is long
    elif island == 2 and level == 3:
        end_x = 3050  # Sapphire Cavern
    elif island == 2:
        end_x = 2350  # Other crystal cave levels
    elif island == 3 and level == 2:
        end_x = 3300  # Ember Caverns is long
    elif island == 3 and level == 3:
        end_x = 2950  # Inferno Pit
    elif island == 3 and level == 4:
        end_x = 3450  # Ash Wastes gauntlet is the longest
    elif island == 3:
        end_x = 2300  # Other volcano levels
    else:
        end_x = 1900  # Island 0 levels
    past_end = player.rect.x > end_x
    return all_dead and past_end
