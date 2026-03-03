# =============================================================================
# POWERS SYSTEM
# =============================================================================
# Tracks the 5 powers the hornet can unlock by defeating island bosses.
# Each island boss drops a different power when defeated.
# =============================================================================

# Power name constants — use these everywhere instead of raw strings
POWER_DOUBLE_JUMP = "double_jump"
POWER_DASH = "dash"
POWER_WALL_CLIMB = "wall_climb"
POWER_SHIELD = "shield"
POWER_STINGER_UPGRADE = "stinger_upgrade"

# Shadow powers — unlocked in Hallucination Land shops
SHADOW_VEIL         = "shadow_veil"        # Island 1: become untouchable for 3 sec
SHADOW_DASH         = "shadow_dash"        # Island 2: dash ignores damage
SHADOW_STINGER      = "shadow_stinger"     # Island 3: attacks ignore armor, +1 vs shadow
SHADOW_WINGS        = "shadow_wings"       # Island 4: unlimited hover
SHADOW_FORM         = "shadow_form"        # Island 5: take half damage always

ALL_SHADOW_POWERS = [
    SHADOW_VEIL,
    SHADOW_DASH,
    SHADOW_STINGER,
    SHADOW_WINGS,
    SHADOW_FORM,
]

# Which hallucination island sells which shadow power
HALLUCINATION_ISLAND_POWER = {
    0: SHADOW_VEIL,
    1: SHADOW_DASH,
    2: SHADOW_STINGER,
    3: SHADOW_WINGS,
    4: SHADOW_FORM,
}

# Cost of each shadow power in the hallucination shop
SHADOW_POWER_COST = {
    SHADOW_VEIL:    200,
    SHADOW_DASH:    300,
    SHADOW_STINGER: 400,
    SHADOW_WINGS:   500,
    SHADOW_FORM:    800,
}

SHADOW_POWER_DESC = {
    SHADOW_VEIL:    "Go untouchable for 3 seconds (30s cooldown)",
    SHADOW_DASH:    "Dash through enemies without taking damage",
    SHADOW_STINGER: "Attacks ignore armor. +1 damage vs shadow enemies",
    SHADOW_WINGS:   "Hover forever — never run out of hover time",
    SHADOW_FORM:    "Always take half damage from all attacks",
}

# All 5 powers in a list (handy for looping)
ALL_POWERS = [
    POWER_DOUBLE_JUMP,
    POWER_DASH,
    POWER_WALL_CLIMB,
    POWER_SHIELD,
    POWER_STINGER_UPGRADE,
]

# Which island boss gives which power (0-indexed)
# Island 0 boss -> double jump, Island 1 boss -> dash, etc.
ISLAND_POWER = {
    0: POWER_DOUBLE_JUMP,
    1: POWER_DASH,
    2: POWER_WALL_CLIMB,
    3: POWER_SHIELD,
    4: POWER_STINGER_UPGRADE,
}
