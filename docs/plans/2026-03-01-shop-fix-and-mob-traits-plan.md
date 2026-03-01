# Shop Fix & Enemy Trait System — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix the broken S-key shop opening, then add 4 enemy ability traits (poison, shadow, armor, ranged) that stack across islands.

**Architecture:** Add a `traits` list to the base `Enemy` class. Each trait modifies behavior in `update()`, `draw()`, and `take_damage()`. The player gets a new poison status effect. Level definitions pass traits when constructing enemies. The shop bug is a same-event double-processing issue fixed with `continue`.

**Tech Stack:** Python 3, Pygame

---

### Task 1: Fix the Shop Bug

**Files:**
- Modify: `src/game.py:139-161`

**The Bug:** When S is pressed on the island map, the event loop processes it in the `STATE_ISLAND_MAP` block (line 144) which switches state to `"shop"`. Then the SAME event continues to the `"shop"` block (line 157) where `shop.handle_input` sees S and returns `"close"`. The shop opens and immediately closes in one frame — invisible to the player.

**Step 1: Add `continue` after shop state transitions**

In `src/game.py`, add `continue` after both state transitions so the same event isn't double-processed:

```python
# Line 153-155: After opening shop, skip to next event
elif result == "shop":
    shop = Shop(save_data)
    game_state = "shop"
    continue  # Don't let this same S-key event close the shop

# Line 159-161: After closing shop, skip to next event
if result == "close":
    island_map = IslandMap(save_data)
    game_state = STATE_ISLAND_MAP
    continue  # Don't let this event trigger island map input
```

**Step 2: Test manually**

Run: `cd /home/dane/Games/hornet-game && python main.py`
- Press ENTER to get to island map
- Press S — shop should open and STAY open
- Press S or ESC — shop should close back to island map
- Press S again — should reopen

**Step 3: Commit**

```bash
git add src/game.py
git commit -m "fix: shop opens and closes instantly — add continue to prevent same-event double-processing"
```

---

### Task 2: Add Trait System to Base Enemy Class

**Files:**
- Modify: `src/entities/enemies.py:7-30` (Enemy base class)

**Step 1: Add traits support to Enemy.__init__**

Add a `traits` parameter and trait-related state to the base `Enemy` class:

```python
class Enemy:
    def __init__(self, x, y, width, height, hp, color, traits=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.hp = hp
        self.color = color
        self.alive = True
        self.death_timer = 0

        # --- Trait system ---
        self.traits = traits or []

        # Shadow trait state
        self.shadow_active = False
        self.shadow_timer = 0          # counts up, toggles at thresholds
        self.shadow_solid_time = 300   # 5 seconds solid (60fps * 5)
        self.shadow_fade_time = 180    # 3 seconds shadow (60fps * 3)

        # Armor trait state
        self.armor_hp = 2 if "armor" in self.traits else 0
        self.armor_flash_timer = 0     # visual flash when armor breaks

        # Ranged trait state
        self.ranged_cooldown = 0
        self.ranged_cooldown_max = 180  # 3 seconds between shots
        self.projectiles = []           # list of {"rect": Rect, "dx": float, "dy": float, "timer": int}
```

**Step 2: Add trait helper methods to Enemy**

```python
def has_trait(self, trait_name):
    return trait_name in self.traits

def update_traits(self, player_x=None, player_y=None):
    """Update trait timers and state. Call from subclass update()."""
    # Shadow form — toggle between solid and shadow
    if self.has_trait("shadow"):
        self.shadow_timer += 1
        if not self.shadow_active:
            if self.shadow_timer >= self.shadow_solid_time:
                self.shadow_active = True
                self.shadow_timer = 0
        else:
            if self.shadow_timer >= self.shadow_fade_time:
                self.shadow_active = False
                self.shadow_timer = 0

    # Armor flash countdown
    if self.armor_flash_timer > 0:
        self.armor_flash_timer -= 1

    # Ranged attack — shoot projectile toward player
    if self.has_trait("ranged") and player_x is not None:
        self.ranged_cooldown -= 1
        dist = abs(self.rect.centerx - player_x)
        if dist < 200 and self.ranged_cooldown <= 0:
            self.ranged_cooldown = self.ranged_cooldown_max
            # Calculate direction toward player
            dx = player_x - self.rect.centerx
            dy = (player_y if player_y else self.rect.centery) - self.rect.centery
            length = max(1, (dx**2 + dy**2) ** 0.5)
            speed = 3
            self.projectiles.append({
                "rect": pygame.Rect(self.rect.centerx - 4, self.rect.centery - 4, 8, 8),
                "dx": dx / length * speed,
                "dy": dy / length * speed,
                "timer": 120,  # 2 seconds lifetime
            })

    # Update projectile positions
    for proj in self.projectiles[:]:
        proj["rect"].x += proj["dx"]
        proj["rect"].y += proj["dy"]
        proj["timer"] -= 1
        if proj["timer"] <= 0:
            self.projectiles.remove(proj)
```

**Step 3: Override take_damage to respect armor and shadow**

```python
def take_damage(self, amount):
    # Can't be hit while in shadow form
    if self.shadow_active:
        return

    # Armor absorbs damage first
    if self.armor_hp > 0:
        self.armor_hp -= amount
        if self.armor_hp <= 0:
            self.armor_flash_timer = 20  # flash when armor breaks
            # Any overflow damage hits real HP
            overflow = abs(self.armor_hp)
            self.armor_hp = 0
            if overflow > 0:
                self.hp -= overflow
        return

    self.hp -= amount
    if self.hp <= 0:
        self.alive = False
        self.death_timer = 15
```

**Step 4: Update Enemy.draw to show trait visuals**

```python
def draw(self, screen, camera_x):
    if not self.alive:
        if self.death_timer > 0:
            draw_rect = self.rect.move(-camera_x, 0)
            pygame.draw.rect(screen, WHITE, draw_rect)
        return

    draw_rect = self.rect.move(-camera_x, 0)

    # Shadow form — draw semi-transparent
    if self.shadow_active:
        s = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        s.fill((*self.color, 80))  # alpha 80
        screen.blit(s, draw_rect)
    else:
        pygame.draw.rect(screen, self.color, draw_rect)

    # Armor outline
    if self.armor_hp > 0:
        pygame.draw.rect(screen, (180, 180, 180), draw_rect, 3)
    elif self.armor_flash_timer > 0:
        # Flash effect when armor just broke
        if self.armor_flash_timer % 4 < 2:
            pygame.draw.rect(screen, WHITE, draw_rect, 2)

    # Draw projectiles
    for proj in self.projectiles:
        proj_draw = proj["rect"].move(-camera_x, 0)
        pygame.draw.circle(screen, self.color, proj_draw.center, 4)
```

**Step 5: Test manually**

Run: `python main.py`
- Game should still load and play normally (no enemies have traits yet)

**Step 6: Commit**

```bash
git add src/entities/enemies.py
git commit -m "feat: add trait system to base Enemy class (shadow, armor, ranged, poison support)"
```

---

### Task 3: Add Traits to Wasp, Fly, and Spider Subclasses

**Files:**
- Modify: `src/entities/enemies.py:31-246` (Wasp, Fly, Spider classes)

**Step 1: Update Wasp to accept and use traits**

Change `Wasp.__init__` signature to accept traits, pass to super, and call `update_traits()` in `update()`:

```python
class Wasp(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right, traits=None):
        super().__init__(x, y, 36, 24, 2, WASP_YELLOW, traits)
        # ... rest stays the same

    def update(self, player_x=None, player_y=None):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return
        self.update_traits(player_x, player_y)
        # ... rest of existing update logic stays the same
```

Note: Wasp.update() currently takes no args. We add `player_x=None, player_y=None` so ranged trait can shoot. This means `game.py` will need to pass player position (Task 5).

**Step 2: Update Wasp.draw to use trait visuals**

The Wasp has sprite-based drawing. We need to apply shadow transparency and armor outline on top of the sprite:

```python
def draw(self, screen, camera_x):
    if not self.alive:
        if self.death_timer > 0:
            draw_rect = self.rect.move(-camera_x, 0)
            pygame.draw.rect(screen, WHITE, draw_rect)
        return

    draw_rect = self.rect.move(-camera_x, 0)
    if self.anim_f == 0:
        spr = self.spr0 if self.moving_right else self.spr0_flip
    else:
        spr = self.spr1 if self.moving_right else self.spr1_flip

    sx = draw_rect.centerx - spr.get_width() // 2
    sy = draw_rect.centery - spr.get_height() // 2

    # Shadow form — draw sprite semi-transparent
    if self.shadow_active:
        ghost = spr.copy()
        ghost.set_alpha(80)
        screen.blit(ghost, (sx, sy))
    else:
        screen.blit(spr, (sx, sy))

    # Armor outline
    if self.armor_hp > 0:
        pygame.draw.rect(screen, (180, 180, 180), draw_rect.inflate(4, 4), 3)
    elif self.armor_flash_timer > 0 and self.armor_flash_timer % 4 < 2:
        pygame.draw.rect(screen, WHITE, draw_rect.inflate(4, 4), 2)

    # Draw projectiles
    for proj in self.projectiles:
        proj_draw = proj["rect"].move(-camera_x, 0)
        pygame.draw.circle(screen, self.color, proj_draw.center, 4)
```

**Step 3: Update Fly the same way**

```python
class Fly(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right, traits=None):
        super().__init__(x, y, 24, 20, 1, GREEN, traits)
        # ... rest stays the same

    def update(self, player_x=None, player_y=None):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return
        self.update_traits(player_x, player_y)
        # ... rest of existing fly update logic (anim, patrol, wave)
```

Apply the same sprite draw pattern as Wasp (shadow alpha, armor outline, projectiles).

**Step 4: Update Spider the same way**

```python
class Spider(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right, traits=None):
        super().__init__(x, y, 28, 28, 1, PURPLE, traits)
        # ... rest stays the same

    def update(self, player_x=None, player_y=None):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return
        self.update_traits(player_x, player_y)
        # ... rest of existing spider update logic (lunge, return, etc.)
        # Note: Spider already takes player_x, just add player_y
```

Apply the same sprite draw pattern (shadow alpha, armor outline, projectiles).

**Step 5: Test manually**

Run: `python main.py`
- Game should still work normally (no traits assigned to any enemies yet)

**Step 6: Commit**

```bash
git add src/entities/enemies.py
git commit -m "feat: wire trait system into Wasp, Fly, and Spider subclasses"
```

---

### Task 4: Add Poison Status Effect to Player

**Files:**
- Modify: `src/entities/player.py:6-80` (Player.__init__ and update)
- Modify: `src/entities/player.py:269-342` (Player.draw)
- Modify: `src/ui/hud.py` (show poison indicator)

**Step 1: Add poison state to Player.__init__**

After the shield state block (line 78), add:

```python
# Poison state
self.poisoned = False
self.poison_timer = 0          # total poison duration remaining (frames)
self.poison_tick_timer = 0     # countdown to next damage tick
self.poison_duration = 360     # 6 seconds at 60fps
self.poison_tick_rate = 120    # damage every 2 seconds
```

**Step 2: Add poison update logic to Player.update**

At the start of `Player.update()`, after the invincibility timer block (line 83), add:

```python
# --- Poison damage over time ---
if self.poisoned:
    self.poison_timer -= 1
    self.poison_tick_timer -= 1
    if self.poison_tick_timer <= 0:
        self.hp -= 1  # Poison damage bypasses shield and invincibility
        self.poison_tick_timer = self.poison_tick_rate
    if self.poison_timer <= 0:
        self.poisoned = False
```

**Step 3: Add apply_poison method to Player**

```python
def apply_poison(self):
    """Apply or refresh poison. Doesn't stack — just resets timer."""
    self.poisoned = True
    self.poison_timer = self.poison_duration
    self.poison_tick_timer = self.poison_tick_rate  # first tick after 2 sec
```

**Step 4: Add poison visual to Player.draw**

After drawing the sprite (around line 302), before the shield bubble:

```python
# --- Poison tint ---
if self.poisoned:
    poison_overlay = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
    poison_overlay.fill((0, 180, 0, 60))  # green tint
    screen.blit(poison_overlay, draw_rect)
```

**Step 5: Add poison indicator to HUD**

In `src/ui/hud.py`, inside `draw_hud()`, after the hover meter (line 17), add:

```python
# Poison indicator
if player.poisoned:
    poison_text = font.render("POISONED", True, (0, 200, 0))
    screen.blit(poison_text, (12, 48))
```

Note: The `font` variable is created on line 20, so we need to move the font init above the poison indicator, or just add the poison indicator after line 22 where font already exists.

**Step 6: Test manually**

Run: `python main.py`
- Play a level — no enemies have poison yet, so nothing should change
- Confirm HUD still draws correctly

**Step 7: Commit**

```bash
git add src/entities/player.py src/ui/hud.py
git commit -m "feat: add poison status effect to player with green tint and HUD indicator"
```

---

### Task 5: Wire Traits Into Combat System

**Files:**
- Modify: `src/systems/combat.py` (check shadow/armor on hit, apply poison on contact)
- Modify: `src/game.py:203-207` (pass player position to enemy update)

**Step 1: Update enemy update calls in game.py to pass player position**

In `src/game.py`, change the enemy update loop (lines 203-207) to always pass player position:

```python
for enemy in enemies:
    enemy.update(player_x=player.rect.centerx, player_y=player.rect.centery)
```

This replaces the current code that only passes `player.rect.centerx` to Spiders. Now ALL enemies get player position (needed for ranged trait).

**Step 2: Add projectile collision to combat.py**

In `handle_combat()`, after the enemy contact damage loop (after line 41), add projectile handling:

```python
# Enemy projectiles damage player
for enemy in enemies:
    if not enemy.alive:
        continue
    for proj in enemy.projectiles[:]:
        if player.rect.colliderect(proj["rect"]):
            hit = player.take_damage(1)
            if hit:
                player.vel_y = -6
                hit_events.append("player_hurt")
                # Poison on projectile hit too
                if enemy.has_trait("poison"):
                    player.apply_poison()
            enemy.projectiles.remove(proj)
```

**Step 3: Apply poison on enemy contact damage**

Modify the existing enemy contact damage loop (lines 32-41) to apply poison:

```python
# Enemies damage player on contact
for enemy in enemies:
    if enemy.alive and player.rect.colliderect(enemy.rect):
        if player.take_damage(1):
            if player.rect.centerx < enemy.rect.centerx:
                player.rect.x -= 30
            else:
                player.rect.x += 30
            player.vel_y = -8
            hit_events.append("player_hurt")
            # Poison trait — apply poison on contact damage
            if enemy.has_trait("poison"):
                player.apply_poison()
```

**Step 4: Handle shadow form in player attack**

The shadow check is already in `Enemy.take_damage()` (from Task 2), so when the player attacks a shadowed enemy, `take_damage` will silently do nothing. No changes needed in combat.py for this — it's handled at the enemy level.

**Step 5: Test manually**

Run: `python main.py`
- Game should play normally. No enemies have traits yet, so no behavior change.

**Step 6: Commit**

```bash
git add src/systems/combat.py src/game.py
git commit -m "feat: wire trait effects into combat — poison on contact, projectile collision"
```

---

### Task 6: Assign Traits to Enemies in Level Definitions

**Files:**
- Modify: `src/world/levels.py` (add traits to enemy constructors for islands 1-4)

**Step 1: Update scale_enemies to preserve traits**

The existing `scale_enemies()` function only changes HP and speed — traits are stored on the enemy object already, so no change needed. But we should make sure it doesn't break anything.

**Step 2: Add traits to Island 1 (Swamp) enemies — Poison introduced**

In the Island 1 level definitions, add `traits=["poison"]` to roughly 30% of enemies. Pick enemies that thematically fit (spiders and some wasps in the swamp):

Example for level 0 (Murky Shallows):
```python
# Some enemies get poison trait
Wasp(300, 540 - 24, 250, 500, traits=["poison"]),  # poison wasp
Wasp(800, 540 - 24, 750, 1050),                     # normal wasp
Fly(500, 300, 400, 700, traits=["poison"]),           # poison fly
```

**Step 3: Add traits to Island 2 (Caves) enemies — Shadow introduced**

Add shadow to some enemies, poison+shadow combos on a few:

```python
Spider(450, 350 - 28, 400, 530, traits=["shadow"]),           # shadow spider
Wasp(300, 540 - 24, 250, 500, traits=["poison"]),             # poison wasp
Fly(600, 280, 550, 750, traits=["poison", "shadow"]),          # poison+shadow fly
```

**Step 4: Add traits to Island 3 (Volcano) enemies — Armor introduced**

Mix of poison, shadow, and armor:

```python
Wasp(300, 540 - 24, 250, 500, traits=["armor"]),                      # armored wasp
Spider(450, 350 - 28, 400, 530, traits=["poison", "shadow"]),          # poison+shadow spider
Fly(600, 280, 550, 750, traits=["armor", "poison"]),                    # armored poison fly
```

**Step 5: Add traits to Island 4 (Shadow Fortress) enemies — Ranged introduced**

All 4 traits in wild combos:

```python
Fly(500, 300, 400, 700, traits=["ranged", "shadow"]),                     # shadow sniper fly
Spider(450, 350 - 28, 400, 530, traits=["armor", "poison"]),              # tank spider
Wasp(800, 540 - 24, 750, 1050, traits=["poison", "shadow", "ranged"]),   # nightmare wasp
```

**Important:** Not every enemy gets traits! Keep some enemies plain so there's variety. Roughly:
- Island 1: ~30% have poison
- Island 2: ~40% have traits (mix of poison and shadow)
- Island 3: ~50% have traits (poison, shadow, armor combos)
- Island 4: ~60% have traits (all 4 possible, some with 2-3 traits stacked)

**Step 6: Test manually**

Run: `python main.py`
- Play Island 0 — enemies should be normal (no traits)
- If you have save data to access Island 1, check that poison enemies have green tint on contact
- Check that shadow enemies go transparent periodically

**Step 7: Commit**

```bash
git add src/world/levels.py
git commit -m "feat: assign trait combos to enemies across islands 1-4"
```

---

### Task 7: Final Polish and Testing

**Files:**
- Modify: `src/ui/hud.py` (show player max HP correctly with upgrades)
- Review: all modified files

**Step 1: Fix HUD health bar to use actual max HP**

In `src/ui/hud.py` line 9, the health bar uses `PLAYER_MAX_HP` (always 5) instead of the player's actual max HP. This should use `player.hp` / actual max:

```python
# Calculate max HP (base + upgrades)
max_hp = getattr(player, '_max_hp', PLAYER_MAX_HP)
hp_width = int(100 * max(0, player.hp) / max_hp)
```

Actually — check if the player tracks max_hp. If not, this is fine for now and can be a future task. Skip this if it adds complexity.

**Step 2: Full playtest**

Run: `python main.py` and test:
1. Press ENTER → island map loads
2. Press S → shop opens (FIXED)
3. Press ESC → shop closes
4. Press S → shop reopens (FIXED)
5. Press ENTER → play Island 0 (Garden) — enemies are normal
6. Play through to Island 1 → some enemies should have poison
7. Get hit by a poison enemy → player turns green, takes damage over time
8. Confirm shadow enemies go transparent and can't be hit
9. Confirm armored enemies take extra hits
10. Confirm ranged enemies shoot projectiles

**Step 3: Final commit**

```bash
git add -A
git commit -m "feat: complete shop fix and enemy trait system"
```

---

## Task Summary

| Task | What It Does | Files |
|------|-------------|-------|
| 1 | Fix shop S-key bug | `game.py` |
| 2 | Add trait system to base Enemy | `enemies.py` |
| 3 | Wire traits into Wasp, Fly, Spider | `enemies.py` |
| 4 | Add poison effect to Player | `player.py`, `hud.py` |
| 5 | Wire traits into combat | `combat.py`, `game.py` |
| 6 | Assign traits to level enemies | `levels.py` |
| 7 | Final polish and testing | all files |
