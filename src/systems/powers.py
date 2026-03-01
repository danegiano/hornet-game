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
