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

# Circus (boss rush) states
STATE_CIRCUS        = "circus"        # The circus lobby/intro screen
STATE_CIRCUS_BOSS   = "circus_boss"   # Fighting a circus boss
STATE_CIRCUS_FAIL   = "circus_fail"   # Died — show restart screen
STATE_CIRCUS_WIN    = "circus_win"    # Beat all 5 — portal appears

# Hallucination Land states
STATE_HALLUCINATION_MAP     = "hallucination_map"
STATE_HALLUCINATION_PLAYING = "hallucination_playing"
STATE_HALLUCINATION_SHOP    = "hallucination_shop"

# Island data — each island has a name, number of levels, and theme color
ISLAND_DATA = [
    {"name": "The Garden Isles",    "levels": 3, "color": (100, 180, 100), "bg": (135, 200, 235)},
    {"name": "The Swamp",           "levels": 4, "color": (80, 120, 60),   "bg": (60, 80, 40)},
    {"name": "The Crystal Caves",   "levels": 5, "color": (100, 80, 200),  "bg": (40, 30, 80)},
    {"name": "The Volcano",         "levels": 6, "color": (200, 80, 40),   "bg": (80, 30, 10)},
    {"name": "The Shadow Fortress", "levels": 7, "color": (80, 40, 120),   "bg": (30, 10, 40)},
]

# Circus — boss rush settings
# Bosses in order: island 0 → 1 → 2 → 3 → 4
CIRCUS_BOSS_ORDER = [0, 1, 2, 3, 4]   # island index for each circus fight
CIRCUS_HP_MULT    = 1.5   # bosses have 50% more HP
CIRCUS_SPEED_MULT = 1.25  # bosses move 25% faster
CIRCUS_DAMAGE_ADD = 1     # bosses deal +1 extra damage

# Hallucination Land — 5 islands, 4 levels each, 1 boss per level
HALLUCINATION_ISLAND_DATA = [
    {"name": "Shadow Wilds",    "levels": 4, "color": (80,  50, 120), "bg": (15, 5, 30)},
    {"name": "Phantom Swamp",   "levels": 4, "color": (40,  70,  40), "bg": (10, 20, 10)},
    {"name": "Void Crystals",   "levels": 4, "color": (60,  40, 140), "bg": (10, 5, 40)},
    {"name": "Ashen Volcano",   "levels": 4, "color": (120, 40,  20), "bg": (30, 5, 5)},
    {"name": "Eclipse Throne",  "levels": 4, "color": (40,  20,  80), "bg": (5, 0, 15)},
]

HALLUCINATION_LEVEL_THEMES = {
    0: [
        {"bg": (15, 5, 30),  "platform": (60, 30, 100), "name": "Shadow Wilds I"},
        {"bg": (13, 4, 27),  "platform": (60, 30, 100), "name": "Shadow Wilds II"},
        {"bg": (11, 3, 24),  "platform": (60, 30, 100), "name": "Shadow Wilds III"},
        {"bg": (9,  2, 21),  "platform": (60, 30, 100), "name": "Shadow Wilds Boss"},
    ],
    1: [
        {"bg": (10, 20, 10), "platform": (30, 60, 30),  "name": "Phantom Swamp I"},
        {"bg": (8,  17, 8),  "platform": (30, 60, 30),  "name": "Phantom Swamp II"},
        {"bg": (6,  14, 6),  "platform": (30, 60, 30),  "name": "Phantom Swamp III"},
        {"bg": (4,  11, 4),  "platform": (30, 60, 30),  "name": "Phantom Swamp Boss"},
    ],
    2: [
        {"bg": (10, 5, 40),  "platform": (50, 30, 110), "name": "Void Crystals I"},
        {"bg": (8,  4, 36),  "platform": (50, 30, 110), "name": "Void Crystals II"},
        {"bg": (6,  3, 32),  "platform": (50, 30, 110), "name": "Void Crystals III"},
        {"bg": (4,  2, 28),  "platform": (50, 30, 110), "name": "Void Crystals Boss"},
    ],
    3: [
        {"bg": (30, 5, 5),   "platform": (80, 30, 20),  "name": "Ashen Volcano I"},
        {"bg": (26, 4, 4),   "platform": (80, 30, 20),  "name": "Ashen Volcano II"},
        {"bg": (22, 3, 3),   "platform": (80, 30, 20),  "name": "Ashen Volcano III"},
        {"bg": (18, 2, 2),   "platform": (80, 30, 20),  "name": "Ashen Volcano Boss"},
    ],
    4: [
        {"bg": (5, 0, 15),   "platform": (30, 10, 60),  "name": "Eclipse Throne I"},
        {"bg": (4, 0, 13),   "platform": (30, 10, 60),  "name": "Eclipse Throne II"},
        {"bg": (3, 0, 11),   "platform": (30, 10, 60),  "name": "Eclipse Throne III"},
        {"bg": (2, 0, 9),    "platform": (30, 10, 60),  "name": "Eclipse Throne Boss"},
    ],
}

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
    # Island 2 — The Crystal Caves
    2: [
        {"bg": (30, 20, 60),   "platform": (80, 60, 140), "name": "Crystal Entrance"},
        {"bg": (25, 15, 55),   "platform": (80, 60, 140), "name": "Amethyst Tunnels"},
        {"bg": (20, 10, 50),   "platform": (80, 60, 140), "name": "Diamond Depths"},
        {"bg": (15, 8, 45),    "platform": (80, 60, 140), "name": "Sapphire Cavern"},
        {"bg": (10, 5, 40),    "platform": (80, 60, 140), "name": "Spider Queen's Web"},
    ],
    # Island 3 — The Volcano
    3: [
        {"bg": (80, 30, 10),  "platform": (100, 50, 30), "name": "Lava Flats"},
        {"bg": (70, 25, 8),   "platform": (100, 50, 30), "name": "Magma Tunnels"},
        {"bg": (60, 20, 5),   "platform": (100, 50, 30), "name": "Ember Caverns"},
        {"bg": (50, 15, 5),   "platform": (100, 50, 30), "name": "Inferno Pit"},
        {"bg": (40, 10, 5),   "platform": (100, 50, 30), "name": "Ash Wastes"},
        {"bg": (30, 5, 5),    "platform": (100, 50, 30), "name": "Moth's Furnace"},
    ],
    # Island 4 — The Shadow Fortress
    4: [
        {"bg": (20, 10, 30),  "platform": (50, 30, 70),  "name": "Shadow Gate"},
        {"bg": (18, 8, 28),   "platform": (50, 30, 70),  "name": "Dark Corridor"},
        {"bg": (15, 6, 25),   "platform": (50, 30, 70),  "name": "Phantom Hall"},
        {"bg": (12, 5, 22),   "platform": (50, 30, 70),  "name": "Nightmare Chamber"},
        {"bg": (10, 4, 20),   "platform": (50, 30, 70),  "name": "Void Passage"},
        {"bg": (8, 3, 18),    "platform": (50, 30, 70),  "name": "Eclipse Sanctum"},
        {"bg": (5, 2, 15),    "platform": (50, 30, 70),  "name": "Shadow Hornet's Throne"},
    ],
}

# Swamp platform color constant
SWAMP_GREEN = (60, 100, 50)

# Crystal cave platform color constant
CRYSTAL_PURPLE = (80, 60, 140)

# Volcano platform color constant
VOLCANO_BROWN = (100, 50, 30)

# Shadow fortress platform color constant
SHADOW_PURPLE = (50, 30, 70)

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
