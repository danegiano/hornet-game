# Hornet Platformer — Game Design

## Overview

A Pygame platformer where you play as a hornet fighting through 3 levels of enemies to defeat the Wasp King. The hornet can run, jump, hover briefly, and attack with a melee stinger.

**Engine:** Pygame (Python)
**Art style:** Simple colored rectangles (gameplay first, art later)
**Structure:** Single-file `main.py` to start, split into modules when it grows

## Player — The Hornet

**Movement:**
- Left/right with arrow keys or A/D
- Jump with spacebar
- Hover: hold spacebar in the air to slow fall for ~1 second
- Hover meter refills when touching the ground

**Attack:**
- Press Z or X to stab forward with the stinger
- Short range melee — must be close to the enemy
- Small cooldown between attacks

**Health:**
- 5 hit points
- Brief invincibility flash after getting hit
- Lose all health = game over, restart the current level

**Visual:** Yellow rectangle (body) with a small triangle on the front (stinger)

## Enemies

### Regular Enemies

1. **Beetle** — Red rectangle. Walks back and forth on platforms. Slow, 2 hits to kill.
2. **Fly** — Green rectangle. Floats in a sine-wave pattern. Fast, 1 hit to kill.
3. **Spider** — Purple rectangle. Sits still, lunges when player is close. 1 hit to kill.

All enemies deal 1 damage on contact. Killed enemies disappear with a brief flash.

### Boss: The Wasp King

- Big orange rectangle, 3x the hornet's size
- 10 hit points
- Attack patterns cycle, getting faster as health drops:
  - **Charge:** Rushes at the player (dodge by jumping)
  - **Slam:** Jumps up and slams down, shockwave on the ground (hover to avoid)
  - **Summon:** Spawns 2 flies

## Levels

Each level is a horizontal series of platforms with enemy placements. Camera follows the player.

### Level 1: The Garden
- Flat terrain, simple platforms, lots of ground
- Enemies: Beetles only
- Purpose: Teaches movement, jumping, hovering, attacking
- Colors: Green platforms, light blue background

### Level 2: The Hive
- Vertical — tall platforms, gaps that need hovering
- Enemies: Beetles + Flies
- Purpose: Tests jumping/hovering, introduces aerial enemies
- Colors: Orange/brown platforms, dark yellow background

### Level 3: The Throne Room
- Trickiest platforming — moving platforms, narrow ledges
- Enemies: All three types, then boss fight in a flat arena at the end
- Purpose: Ultimate challenge before the boss
- Colors: Dark gray platforms, dark red background

### Between Levels
- Transition screen: "Level X: Name" with "Press ENTER to continue"
- Health fully restores between levels

## Game Flow

1. **Title screen** — "HORNET" title, "Press ENTER to start"
2. **Playing** — gameplay with enemies and platforms
3. **Level transition** — brief screen between levels
4. **Boss fight** — same as playing, boss health bar shown
5. **Game over** — "Press ENTER to retry" (restarts current level)
6. **Victory** — "You defeated the Wasp King!" screen

## HUD

- Health bar: top-left
- Hover meter: below health bar
- Level name: top-right
- Boss health bar: top-center (during boss fight only)

## Controls

| Action     | Key                |
|------------|--------------------|
| Move left  | Left arrow or A    |
| Move right | Right arrow or D   |
| Jump       | Spacebar           |
| Hover      | Hold space in air  |
| Attack     | Z or X             |

## Technical

- 60 FPS game loop
- 800x600 pixel window
- Rectangle-based collision detection
- Horizontal camera follow
