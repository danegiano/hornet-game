# Island Progression System Design

## Overview

Transform Hornet from a 3-level game into a 5-island adventure with boss powers, coins, an HP shop, and a save system. Also refactor the codebase from a single main.py into a proper folder structure.

## Part 1: Code Refactor

Split `main.py` (1190 lines) into a folder-based structure:

```
hornet-game/
  main.py                  <- tiny entry point
  src/
    __init__.py
    settings.py            <- all constants
    game.py                <- main game loop + state machine
    save_data.py           <- save/load progress to JSON

    entities/
      __init__.py
      player.py            <- Player class
      enemies.py           <- Enemy, Wasp, Fly, Spider
      bosses.py            <- WaspKing + 4 new bosses

    world/
      __init__.py
      levels.py            <- level data for all 25 levels
      platforms.py         <- Platform class
      camera.py            <- Camera + ParallaxBackground

    systems/
      __init__.py
      combat.py            <- handle_combat(), damage logic
      coins.py             <- coin drops, coin counter
      powers.py            <- power-up tracking + effects

    ui/
      __init__.py
      hud.py               <- health bar, hover meter, coins
      menus.py             <- title, game over, victory, transitions
      island_map.py        <- island selection screen
      shop.py              <- HP shop
```

## Part 2: Island System

5 islands, each with increasing levels. The last level of each island is a boss fight.

| Island | Name              | Levels | Boss               | Power Reward    | Theme                     |
|--------|-------------------|--------|--------------------|-----------------|---------------------------|
| 1      | The Garden Isles  | 3      | Wasp King          | Double Jump     | Green, flowers, grass     |
| 2      | The Swamp         | 4      | Swamp Beetle Lord  | Dash            | Dark green, murky, vines  |
| 3      | The Crystal Caves | 5      | Crystal Spider Queen | Wall Climb    | Blue/purple, crystals     |
| 4      | The Volcano       | 6      | Fire Moth          | Shield          | Red/orange, lava, ash     |
| 5      | The Shadow Fortress | 7    | Shadow Hornet      | Stinger Upgrade | Dark, purple lightning    |

Total: 25 levels across 5 islands.

### Difficulty Scaling

- Each island multiplies enemy HP by 1.5x
- Enemies move faster on later islands
- More enemies per level on later islands
- Bosses have more HP and attack faster

### Level Progression

- Beat all levels in order within an island (level 1 -> 2 -> ... -> boss)
- Beating the boss unlocks the next island
- Can replay earlier levels (enemies respawn, coins drop again)

## Part 3: Coins & Shop

### Coins
- Every enemy drops 2 coins on death (float toward player)
- Every boss drops 5 coins on defeat
- Coins persist across deaths
- Coin counter shown in HUD (top right)

### HP Shop (on Island Map)
- Buy +1 Max HP for 50 coins
- Maximum 8 purchases (5 HP -> 13 HP max)
- Price stays at 50 coins each time
- Shown as heart icons for visual tracking

## Part 4: Powers

Earned by defeating each island's boss. Permanent once earned.

### 1. Double Jump (Island 1)
- Press jump again mid-air for a second jump
- Same height as normal jump
- Resets on landing

### 2. Dash (Island 2)
- Press Shift/C to burst forward ~150 pixels
- Direction matches facing direction
- 1-second cooldown
- Invincible during dash

### 3. Wall Climb (Island 3)
- Press up while touching a wall to climb
- Slower than walking speed
- Can jump off walls

### 4. Shield (Island 4)
- Automatically blocks first hit of damage
- Glowing circle visual when active
- Recharges after 5 seconds of no damage

### 5. Stinger Upgrade (Island 5)
- Stinger does 2 damage instead of 1
- Bigger, glowing stinger visual

## Part 5: Island Map Screen

Side-scrolling map with island landmasses on water:
- Hornet cursor moves between unlocked islands (left/right arrows)
- Locked islands shown grayed out with lock icon
- Press Enter to open level select within an island
- Level select shows numbered nodes (1, 2, 3... boss)
- Bottom bar shows earned powers (??? for locked ones)
- Top right: Shop button (press S)
- Animated water wave effect

## Part 6: Save System

Auto-saves to `save_data.json`:
- Coins collected
- Unlocked islands
- Completed levels
- Purchased HP upgrades
- Earned powers

Saves after: level completion, boss defeat, shop purchase.
