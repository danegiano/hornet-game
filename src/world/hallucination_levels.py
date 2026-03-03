from src.settings import *
from src.world.levels import create_level


def create_hallucination_level(island, level):
    """Return (platforms, enemies) for a Hallucination Land level.

    Reuses the normal level platforms but:
    - All enemies are shadow form (trait added)
    - Enemies have 2x HP and 1.25x speed
    - Platform colors use the hallucination theme
    """
    # Map hallucination island 0-4 to normal island 0-4
    normal_island = island
    normal_level = min(level, ISLAND_DATA[normal_island]["levels"] - 1)

    platforms, enemies = create_level(normal_island, normal_level)

    # Override platform colors to hallucination theme
    theme_color = HALLUCINATION_LEVEL_THEMES[island][level]["platform"]
    for p in platforms:
        p.color = theme_color

    # Make all enemies shadow + stronger
    for e in enemies:
        if "shadow" not in e.traits:
            e.traits.append("shadow")
        e.hp = max(1, e.hp * 2)
        if hasattr(e, 'speed'):
            e.speed *= 1.25

    return platforms, enemies
