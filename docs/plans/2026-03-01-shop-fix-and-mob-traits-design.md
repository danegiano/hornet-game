# Shop Fix & Enemy Trait System Design

**Date:** 2026-03-01
**Status:** Approved

## Overview

Two changes to the hornet game:
1. Fix the shop — pressing S on the island map does nothing (should open the shop)
2. Add 4 new enemy ability traits that stack across islands 1-4

## Part 1: Shop Bug Fix

**Problem:** Pressing S on the island map screen does nothing. The shop never opens.

**Root Cause:** Needs investigation — the `shop.py` code handles S key correctly for closing, but the connection between `island_map.py` returning `"shop"` and `game.py` switching to shop state may be broken.

**Fix:** Read the actual `game.py` and `island_map.py`, find where the S key press is getting lost, and wire the shop state transition properly.

## Part 2: Enemy Trait System

### Architecture: Trait-Based System

Instead of creating new enemy subclasses, we add a **traits list** to the base `Enemy` class. Each trait modifies the enemy's behavior. Traits can be combined — a single enemy can have poison AND shadow AND armor.

### The 4 Traits

#### Poison
- **Trigger:** When enemy damages the player (contact hit)
- **Effect:** Player turns green, loses 1 HP every 2 seconds for 6 seconds (3 ticks = 3 extra damage)
- **Visual:** Green tint on player, small green particles floating up
- **Stacking:** Does NOT stack — getting poisoned again resets the timer
- **Introduced:** Island 1 (Swamp) — fits the swamp theme

#### Shadow Form
- **Trigger:** Every 5 seconds, enemy goes shadow for 3 seconds
- **Effect:** Enemy can't be hit while shadowy, but can still damage the player
- **Visual:** Enemy becomes semi-transparent (alpha 80)
- **Counter-play:** Watch the timing, attack when solid
- **Introduced:** Island 2 (Crystal Caves) — cave shadows

#### Armor
- **Trigger:** Enemy spawns with armor
- **Effect:** +2 bonus HP that must be broken before real HP takes damage
- **Visual:** Gray outline/border around the enemy. Flash/crack effect when armor breaks
- **Introduced:** Island 3 (Volcano) — hardened lava shell

#### Ranged Attack
- **Trigger:** Player within 200px, enemy shoots every 3 seconds
- **Effect:** Small projectile flies toward player position. Deals 1 damage. Disappears after 2 seconds or hitting a platform
- **Visual:** Small colored circle matching the enemy color
- **Introduced:** Island 4 (Shadow Fortress) — hardest ability, saved for last

### Trait Distribution by Island

| Island | HP Scale | Speed Scale | New Trait | Stacking |
|--------|----------|-------------|-----------|----------|
| 0 - Garden | x1.0 | x1.0 | None | None |
| 1 - Swamp | x1.5 | x1.0 | Poison | ~30% of enemies get poison |
| 2 - Caves | x2.25 | x1.1 | Shadow | Poison + Shadow combos appear |
| 3 - Volcano | x3.375 | x1.2 | Armor | Poison + Shadow + Armor combos |
| 4 - Shadow Fortress | x5.0+ | x1.3 | Ranged | All 4 traits possible, wild combos |

Not every enemy gets traits — roughly 40-60% of enemies on each island have traits. Some stay "normal" so there's variety.

### Example Combos (Island 4)

- Shadow Ranged Fly — goes invisible then shoots
- Armored Poison Spider — tanky, lunges, poisons on hit
- Poison Shadow Ranged Wasp — ultimate annoying enemy

## Implementation Notes

### Files to Modify
- `src/entities/enemies.py` — Add trait system to base Enemy class
- `src/world/levels.py` — Add traits to enemy definitions, update `scale_enemies()`
- `src/entities/player.py` — Add poison status effect handling
- `src/systems/combat.py` — Check for shadow (invulnerable) and armor
- `src/ui/hud.py` — Show poison indicator
- `src/game.py` — Fix shop state transition
- `src/ui/island_map.py` — Verify S key handling

### Player Poison State
- New fields on player: `poisoned`, `poison_timer`, `poison_tick_timer`
- Poison tint drawn as green overlay on player rectangle
- Poison damage bypasses shield (it's already in your system)

### Enemy Trait Storage
- `self.traits = []` on base Enemy
- Helper methods: `has_trait("poison")`, `is_shadow_active()`, `armor_hp`
- Traits set during level definition: `Wasp(x, y, left, right, traits=["poison", "shadow"])`
