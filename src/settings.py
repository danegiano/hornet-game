# =============================================================================
# HORNET - Game Settings & Constants
# =============================================================================
# All the numbers and colors that control how the game looks and feels.
# Change values here to tweak the game without digging through code.
# =============================================================================

# Screen / window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "HORNET"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 50)
DARK_YELLOW = (200, 170, 0)
ORANGE = (230, 150, 30)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
PURPLE = (150, 50, 200)

# Wasp (yellow) sprite colors
WASP_YELLOW = (255, 220, 50)
WASP_YELLOW_DARK = (200, 170, 0)

# Game states
STATE_TITLE = "title"
STATE_PLAYING = "playing"
STATE_LEVEL_TRANSITION = "transition"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"

# New game states for island system
STATE_ISLAND_MAP = "island_map"
STATE_LEVEL_SELECT = "level_select"

# Island data — each island has a name, number of levels, and theme color
ISLAND_DATA = [
    {"name": "The Garden Isles",    "levels": 3, "color": (100, 180, 100), "bg": (135, 200, 235)},
    {"name": "The Swamp",           "levels": 4, "color": (80, 120, 60),   "bg": (60, 80, 40)},
    {"name": "The Crystal Caves",   "levels": 5, "color": (100, 80, 200),  "bg": (40, 30, 80)},
    {"name": "The Volcano",         "levels": 6, "color": (200, 80, 40),   "bg": (80, 30, 10)},
    {"name": "The Shadow Fortress", "levels": 7, "color": (80, 40, 120),   "bg": (30, 10, 40)},
]

# Level themes — background color, platform color, and display name
# Organized by island: LEVEL_THEMES[island_index][level_index]
LEVEL_THEMES = {
    # Island 0 — The Garden Isles
    0: [
        {"bg": (135, 200, 235), "platform": (100, 180, 100), "name": "The Garden"},
        {"bg": (180, 160, 80),  "platform": (160, 120, 60),  "name": "The Hive"},
        {"bg": (100, 40, 40),   "platform": (80, 80, 80),    "name": "The Throne Room"},
    ],
    # Island 1 — The Swamp
    1: [
        {"bg": (50, 70, 35),  "platform": (60, 100, 50), "name": "Murky Shallows"},
        {"bg": (40, 60, 30),  "platform": (60, 100, 50), "name": "Twisted Roots"},
        {"bg": (35, 50, 25),  "platform": (60, 100, 50), "name": "Poison Bog"},
        {"bg": (30, 40, 20),  "platform": (60, 100, 50), "name": "Beetle Lord's Lair"},
    ],
}

# Swamp platform color constant
SWAMP_GREEN = (60, 100, 50)

# Player constants
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
PLAYER_SPEED = 5
GRAVITY = 0.8
JUMP_POWER = -15

HOVER_MAX = 60        # Frames of hover time (~1 second at 60fps)
HOVER_GRAVITY = 0.15  # Much slower fall while hovering

ATTACK_RANGE = 50
ATTACK_WIDTH = 10
ATTACK_DURATION = 10   # Frames the attack hitbox is active
ATTACK_COOLDOWN = 20   # Frames before you can attack again

PLAYER_MAX_HP = 5
INVINCIBILITY_FRAMES = 60  # 1 second of invincibility after hit
