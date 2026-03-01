# Island Progression System Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Refactor Hornet from a single-file 3-level game into a folder-based 5-island adventure with coins, boss powers, an HP shop, and save system.

**Architecture:** The existing 1190-line `main.py` gets split into a `src/` package with subfolders for entities, world, systems, and UI. New features (coins, powers, island map, shop, save) are added as new modules. The current 3 levels become Island 1; 4 new islands with unique bosses and levels are built on top.

**Tech Stack:** Python 3, Pygame, JSON for save data

---

## Phase 1: Refactor (Tasks 1-9)

The goal is to split `main.py` into the `src/` folder structure WITHOUT changing any game behavior. After each task, run the game and verify it still plays exactly the same.

**Verification command for every task in Phase 1:**
```bash
cd /home/dane/Games/hornet-game && python main.py
```
Play through: title screen -> level 1 -> kill enemies -> move right -> level transition -> all the way to boss. If anything breaks, fix it before moving on.

---

### Task 1: Create folder structure and settings module

**Files:**
- Create: `src/__init__.py`
- Create: `src/entities/__init__.py`
- Create: `src/world/__init__.py`
- Create: `src/systems/__init__.py`
- Create: `src/ui/__init__.py`
- Create: `src/settings.py`
- Modify: `main.py:1-49` (remove constants, import from settings)

**Step 1: Create all directories and empty `__init__.py` files**

```bash
mkdir -p src/entities src/world src/systems src/ui
touch src/__init__.py src/entities/__init__.py src/world/__init__.py src/systems/__init__.py src/ui/__init__.py
```

**Step 2: Create `src/settings.py`**

Extract ALL constants from `main.py` lines 1-49 into `src/settings.py`. This includes:
- `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `FPS`, `TITLE`
- All color constants (`BLACK`, `WHITE`, `YELLOW`, `DARK_YELLOW`, `ORANGE`, `RED`, `GREEN`, `PURPLE`, `WASP_YELLOW`, `WASP_YELLOW_DARK`)
- `LEVEL_THEMES` list
- All player constants (`PLAYER_WIDTH`, `PLAYER_HEIGHT`, `PLAYER_SPEED`, `GRAVITY`, `JUMP_POWER`, `HOVER_MAX`, `HOVER_GRAVITY`, `ATTACK_RANGE`, `ATTACK_WIDTH`, `ATTACK_DURATION`, `ATTACK_COOLDOWN`, `PLAYER_MAX_HP`, `INVINCIBILITY_FRAMES`)
- Game state constants (`STATE_TITLE`, `STATE_PLAYING`, `STATE_LEVEL_TRANSITION`, `STATE_GAME_OVER`, `STATE_VICTORY`)

Note: The color constants `RED`, `GREEN`, `PURPLE`, `WASP_YELLOW`, `WASP_YELLOW_DARK` are defined at lines 396-401 of main.py, between the Platform class and Enemy class. Move them ALL into settings.py.

**Step 3: Update `main.py` to import from settings**

Replace the constants at the top of `main.py` with:
```python
from src.settings import *
```

Remove all the constant definitions from main.py (lines 6-49 and lines 396-401).

**Step 4: Verify game runs**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 5: Commit**

```bash
git add src/ main.py
git commit -m "refactor: extract constants into src/settings.py"
```

---

### Task 2: Extract Platform class

**Files:**
- Create: `src/world/platforms.py`
- Modify: `main.py` (remove Platform class, add import)

**Step 1: Create `src/world/platforms.py`**

Move the `Platform` class from `main.py` lines 336-393 into `src/world/platforms.py`.

At the top of the new file, add:
```python
import pygame
import math
from src.settings import *
```

**Step 2: Update `main.py`**

Remove the Platform class. Add at the top:
```python
from src.world.platforms import Platform
```

**Step 3: Verify game runs**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 4: Commit**

```bash
git add src/world/platforms.py main.py
git commit -m "refactor: extract Platform class to src/world/platforms.py"
```

---

### Task 3: Extract Camera and ParallaxBackground

**Files:**
- Create: `src/world/camera.py`
- Modify: `main.py` (remove Camera + ParallaxBackground classes, add import)

**Step 1: Create `src/world/camera.py`**

Move `ParallaxBackground` (lines 283-322) and `Camera` (lines 324-333) into `src/world/camera.py`.

At the top:
```python
import pygame
import os
from src.settings import *
```

**Step 2: Update `main.py`**

Remove both classes. Add:
```python
from src.world.camera import Camera, ParallaxBackground
```

**Step 3: Verify game runs**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 4: Commit**

```bash
git add src/world/camera.py main.py
git commit -m "refactor: extract Camera and ParallaxBackground to src/world/camera.py"
```

---

### Task 4: Extract Enemy classes

**Files:**
- Create: `src/entities/enemies.py`
- Modify: `main.py` (remove enemy classes, add import)

**Step 1: Create `src/entities/enemies.py`**

Move these classes from `main.py` into `src/entities/enemies.py`:
- `Enemy` (lines 404-426)
- `Wasp(Enemy)` (lines 428-490)
- `Fly(Enemy)` (lines 494-552)
- `Spider(Enemy)` (lines 555-642)

At the top:
```python
import pygame
import os
import math
from src.settings import *
```

**Step 2: Update `main.py`**

Remove all four classes. Add:
```python
from src.entities.enemies import Enemy, Wasp, Fly, Spider
```

**Step 3: Verify game runs**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 4: Commit**

```bash
git add src/entities/enemies.py main.py
git commit -m "refactor: extract Enemy classes to src/entities/enemies.py"
```

---

### Task 5: Extract WaspKing boss

**Files:**
- Create: `src/entities/bosses.py`
- Modify: `main.py` (remove WaspKing class, add import)

**Step 1: Create `src/entities/bosses.py`**

Move `WaspKing` (lines 645-789) into `src/entities/bosses.py`.

At the top:
```python
import pygame
import os
from src.settings import *
from src.entities.enemies import Fly
```

Note: WaspKing's `summon` attack creates Fly instances (line 753-758), so it needs to import Fly.

**Step 2: Update `main.py`**

Remove WaspKing class. Add:
```python
from src.entities.bosses import WaspKing
```

**Step 3: Verify game runs (especially boss fight on level 3)**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 4: Commit**

```bash
git add src/entities/bosses.py main.py
git commit -m "refactor: extract WaspKing to src/entities/bosses.py"
```

---

### Task 6: Extract Player class

**Files:**
- Create: `src/entities/player.py`
- Modify: `main.py` (remove Player class, add import)

**Step 1: Create `src/entities/player.py`**

Move the `Player` class from `main.py` lines 52-281 into `src/entities/player.py`.

At the top:
```python
import pygame
import os
from src.settings import *
```

**Step 2: Update `main.py`**

Remove Player class. Add:
```python
from src.entities.player import Player
```

**Step 3: Verify game runs**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 4: Commit**

```bash
git add src/entities/player.py main.py
git commit -m "refactor: extract Player class to src/entities/player.py"
```

---

### Task 7: Extract level data and combat

**Files:**
- Create: `src/world/levels.py`
- Create: `src/systems/combat.py`
- Modify: `main.py`

**Step 1: Create `src/world/levels.py`**

Move `create_level()` (lines 791-863) and `check_level_complete()` (lines 866-871) into `src/world/levels.py`.

At the top:
```python
from src.settings import *
from src.world.platforms import Platform
from src.entities.enemies import Wasp, Fly, Spider
```

**Step 2: Create `src/systems/combat.py`**

Move `handle_combat()` (lines 931-980) into `src/systems/combat.py`.

At the top:
```python
import pygame
from src.settings import *
```

**Step 3: Update `main.py`**

Remove both functions. Add:
```python
from src.world.levels import create_level, check_level_complete
from src.systems.combat import handle_combat
```

**Step 4: Verify game runs**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 5: Commit**

```bash
git add src/world/levels.py src/systems/combat.py main.py
git commit -m "refactor: extract levels and combat to src/"
```

---

### Task 8: Extract UI functions

**Files:**
- Create: `src/ui/hud.py`
- Create: `src/ui/menus.py`
- Modify: `main.py`

**Step 1: Create `src/ui/hud.py`**

Move these functions into `src/ui/hud.py`:
- `draw_hud()` (lines 874-891)
- `draw_boss_hp()` (lines 983-991)

At the top:
```python
import pygame
from src.settings import *
```

**Step 2: Create `src/ui/menus.py`**

Move these functions into `src/ui/menus.py`:
- `draw_title_screen()` (lines 894-901)
- `draw_game_over()` (lines 903-910)
- `draw_transition()` (lines 912-919)
- `draw_victory()` (lines 921-928)

At the top:
```python
import pygame
from src.settings import *
```

**Step 3: Update `main.py`**

Remove all those functions. Add:
```python
from src.ui.hud import draw_hud, draw_boss_hp
from src.ui.menus import draw_title_screen, draw_game_over, draw_transition, draw_victory
```

**Step 4: Verify game runs**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 5: Commit**

```bash
git add src/ui/hud.py src/ui/menus.py main.py
git commit -m "refactor: extract HUD and menu drawing to src/ui/"
```

---

### Task 9: Extract game loop into game.py

**Files:**
- Create: `src/game.py`
- Modify: `main.py` (becomes tiny entry point)

**Step 1: Create `src/game.py`**

Move the entire `main()` function (lines 994-1190) into `src/game.py` as a `run()` function (or keep as `main()`). This file needs all the imports:

```python
import pygame
import os
import sys
from src.settings import *
from src.entities.player import Player
from src.entities.enemies import Wasp, Fly, Spider
from src.entities.bosses import WaspKing
from src.world.levels import create_level, check_level_complete
from src.world.camera import Camera, ParallaxBackground
from src.systems.combat import handle_combat
from src.ui.hud import draw_hud, draw_boss_hp
from src.ui.menus import draw_title_screen, draw_game_over, draw_transition, draw_victory
```

**Step 2: Make `main.py` a tiny entry point**

Replace all of `main.py` with:
```python
from src.game import main

if __name__ == "__main__":
    main()
```

**Step 3: Verify game runs end-to-end**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

Play through at least the first level fully to verify everything works.

**Step 4: Commit**

```bash
git add src/game.py main.py
git commit -m "refactor: extract game loop to src/game.py, main.py is now entry point"
```

**At this point, `main.py` should be ~4 lines. The entire game code lives in `src/`. Refactor complete!**

---

## Phase 2: Save System (Task 10)

Build the save system first because coins, powers, and island progress all depend on it.

---

### Task 10: Add save/load system

**Files:**
- Create: `src/save_data.py`
- Create: `tests/test_save_data.py`

**Step 1: Write tests for save_data**

Create `tests/test_save_data.py`:

```python
import os
import json
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.save_data import SaveData

def test_default_save():
    """New save has correct defaults."""
    save = SaveData(path="/tmp/test_hornet_save.json")
    assert save.coins == 0
    assert save.hp_upgrades == 0
    assert save.max_island_unlocked == 0
    assert save.powers == []
    assert save.completed_levels == {}

def test_save_and_load():
    """Can save and load data."""
    path = "/tmp/test_hornet_save2.json"
    save = SaveData(path=path)
    save.coins = 42
    save.hp_upgrades = 3
    save.powers = ["double_jump", "dash"]
    save.max_island_unlocked = 2
    save.completed_levels = {"0": [0, 1, 2], "1": [0]}
    save.save()

    loaded = SaveData(path=path)
    loaded.load()
    assert loaded.coins == 42
    assert loaded.hp_upgrades == 3
    assert loaded.powers == ["double_jump", "dash"]
    assert loaded.max_island_unlocked == 2
    assert loaded.completed_levels == {"0": [0, 1, 2], "1": [0]}

    os.remove(path)

def test_add_coins():
    save = SaveData(path="/tmp/test_hornet_save3.json")
    save.add_coins(10)
    assert save.coins == 10
    save.add_coins(5)
    assert save.coins == 15

def test_buy_hp():
    save = SaveData(path="/tmp/test_hornet_save4.json")
    save.coins = 100
    assert save.buy_hp() == True   # costs 50
    assert save.coins == 50
    assert save.hp_upgrades == 1
    assert save.buy_hp() == True   # costs 50
    assert save.coins == 0
    assert save.hp_upgrades == 2
    assert save.buy_hp() == False  # not enough coins
    assert save.hp_upgrades == 2

def test_buy_hp_max_limit():
    save = SaveData(path="/tmp/test_hornet_save5.json")
    save.coins = 1000
    save.hp_upgrades = 8
    assert save.buy_hp() == False  # already at max
    assert save.coins == 1000

if __name__ == "__main__":
    test_default_save()
    test_save_and_load()
    test_add_coins()
    test_buy_hp()
    test_buy_hp_max_limit()
    print("All save_data tests passed!")
```

**Step 2: Run tests to verify they fail**

```bash
cd /home/dane/Games/hornet-game && python tests/test_save_data.py
```
Expected: ImportError (save_data doesn't exist yet)

**Step 3: Implement `src/save_data.py`**

```python
import json
import os

HP_COST = 50
MAX_HP_UPGRADES = 8

class SaveData:
    def __init__(self, path="save_data.json"):
        self.path = path
        self.coins = 0
        self.hp_upgrades = 0
        self.max_island_unlocked = 0
        self.powers = []
        self.completed_levels = {}  # {"0": [0, 1, 2], "1": [0, 1]}
        # Try to load existing save
        if os.path.exists(self.path):
            self.load()

    def save(self):
        data = {
            "coins": self.coins,
            "hp_upgrades": self.hp_upgrades,
            "max_island_unlocked": self.max_island_unlocked,
            "powers": self.powers,
            "completed_levels": self.completed_levels,
        }
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        with open(self.path, "r") as f:
            data = json.load(f)
        self.coins = data.get("coins", 0)
        self.hp_upgrades = data.get("hp_upgrades", 0)
        self.max_island_unlocked = data.get("max_island_unlocked", 0)
        self.powers = data.get("powers", [])
        self.completed_levels = data.get("completed_levels", {})

    def add_coins(self, amount):
        self.coins += amount

    def buy_hp(self):
        if self.hp_upgrades >= MAX_HP_UPGRADES:
            return False
        if self.coins < HP_COST:
            return False
        self.coins -= HP_COST
        self.hp_upgrades += 1
        return True

    def get_max_hp(self):
        from src.settings import PLAYER_MAX_HP
        return PLAYER_MAX_HP + self.hp_upgrades

    def complete_level(self, island_index, level_index):
        key = str(island_index)
        if key not in self.completed_levels:
            self.completed_levels[key] = []
        if level_index not in self.completed_levels[key]:
            self.completed_levels[key].append(level_index)

    def unlock_power(self, power_name):
        if power_name not in self.powers:
            self.powers.append(power_name)

    def has_power(self, power_name):
        return power_name in self.powers
```

**Step 4: Run tests**

```bash
cd /home/dane/Games/hornet-game && python tests/test_save_data.py
```
Expected: "All save_data tests passed!"

**Step 5: Commit**

```bash
mkdir -p tests
git add src/save_data.py tests/test_save_data.py
git commit -m "feat: add save/load system with coins and HP shop logic"
```

---

## Phase 3: Coin System (Task 11)

---

### Task 11: Add coin drops and HUD counter

**Files:**
- Create: `src/systems/coins.py`
- Modify: `src/systems/combat.py` (drop coins on enemy kill)
- Modify: `src/ui/hud.py` (show coin counter)
- Modify: `src/game.py` (wire up save_data + coins)

**Step 1: Create `src/systems/coins.py`**

This handles the visual coin drop effect (little circles floating toward the player):

```python
import pygame
import math

class CoinDrop:
    """A coin that floats up then flies toward the player."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.target_x = x
        self.target_y = y
        self.collected = False
        self.float_timer = 20  # float up for 20 frames first
        self.speed = 6

    def update(self, player_rect):
        if self.collected:
            return
        if self.float_timer > 0:
            self.y -= 2  # float upward
            self.float_timer -= 1
        else:
            # Fly toward player
            dx = player_rect.centerx - self.x
            dy = player_rect.centery - self.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < 15:
                self.collected = True
                return
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self, screen, camera_x):
        if self.collected:
            return
        sx = int(self.x - camera_x)
        sy = int(self.y)
        pygame.draw.circle(screen, (255, 220, 50), (sx, sy), 6)
        pygame.draw.circle(screen, (200, 170, 0), (sx, sy), 6, 2)


class CoinManager:
    """Manages all active coin drops."""
    def __init__(self):
        self.coins = []

    def spawn(self, x, y, count):
        for i in range(count):
            self.coins.append(CoinDrop(x + i * 10 - count * 5, y))

    def update(self, player_rect):
        collected = 0
        for coin in self.coins:
            coin.update(player_rect)
            if coin.collected:
                collected += 1
        self.coins = [c for c in self.coins if not c.collected]
        return collected

    def draw(self, screen, camera_x):
        for coin in self.coins:
            coin.draw(screen, camera_x)
```

**Step 2: Modify `src/systems/combat.py`**

Update `handle_combat()` to return which enemies died (so game.py knows where to spawn coins). Change the return from just `hit_events` to also include dead enemy positions. The simplest way: add `"enemy_die_at"` events that include position data.

Add to the combat event returns: when an enemy dies, include its rect center position in a separate list.

**Step 3: Modify `src/ui/hud.py`**

Add coin counter to `draw_hud()`. Add a `coins` parameter:

```python
def draw_hud(screen, player, level_name, coins=0):
    # ... existing HP bar and hover bar code ...

    # Coin counter (top-right area)
    font = pygame.font.Font(None, 28)
    coin_text = font.render(f"Coins: {coins}", True, (255, 220, 50))
    screen.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 36))
```

**Step 4: Modify `src/game.py`**

Wire up SaveData, CoinManager, and coin collection:
- Import `SaveData` and `CoinManager`
- Create `save_data = SaveData()` at game start
- Create `coin_manager = CoinManager()` per level
- When combat returns `enemy_die`, call `coin_manager.spawn(enemy.rect.centerx, enemy.rect.y, 2)`
- When combat returns `boss_die`, call `coin_manager.spawn(boss.rect.centerx, boss.rect.y, 5)`
- Each frame: `collected = coin_manager.update(player.rect)` then `save_data.add_coins(collected)`
- Draw coins: `coin_manager.draw(screen, camera.x)`
- Pass `save_data.coins` to `draw_hud()`

**Step 5: Verify game runs — kill enemies, see coins drop and counter increase**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 6: Commit**

```bash
git add src/systems/coins.py src/systems/combat.py src/ui/hud.py src/game.py
git commit -m "feat: add coin drops from enemies with HUD counter"
```

---

## Phase 4: Powers System (Task 12)

---

### Task 12: Add powers tracking and double jump

**Files:**
- Create: `src/systems/powers.py`
- Modify: `src/entities/player.py` (add double jump, dash, wall climb, shield, stinger upgrade logic)
- Modify: `src/game.py` (apply powers from save_data to player)

**Step 1: Create `src/systems/powers.py`**

Simple module that defines power names and applies them to the player:

```python
POWER_DOUBLE_JUMP = "double_jump"
POWER_DASH = "dash"
POWER_WALL_CLIMB = "wall_climb"
POWER_SHIELD = "shield"
POWER_STINGER_UPGRADE = "stinger_upgrade"

ALL_POWERS = [POWER_DOUBLE_JUMP, POWER_DASH, POWER_WALL_CLIMB, POWER_SHIELD, POWER_STINGER_UPGRADE]

# Which island boss gives which power (0-indexed)
ISLAND_POWER = {
    0: POWER_DOUBLE_JUMP,
    1: POWER_DASH,
    2: POWER_WALL_CLIMB,
    3: POWER_SHIELD,
    4: POWER_STINGER_UPGRADE,
}
```

**Step 2: Modify `src/entities/player.py`**

Add power-related attributes to `Player.__init__()`:

```python
# Powers (set by game.py based on save data)
self.has_double_jump = False
self.has_dash = False
self.has_wall_climb = False
self.has_shield = False
self.stinger_damage = 1  # becomes 2 with upgrade

# Double jump state
self.jumps_remaining = 1  # 1 = normal, 2 = double jump
self.used_double_jump = False

# Dash state
self.dashing = False
self.dash_timer = 0
self.dash_cooldown = 0
self.dash_direction = 1

# Shield state
self.shield_active = False
self.shield_recharge_timer = 0
```

Modify the jump logic in `update()`: if `has_double_jump` and `jumps_remaining > 0` and in air, allow a second jump.

Modify `take_damage()`: if `has_shield` and `shield_active`, block the hit and start recharge timer instead.

Add dash input handling: if `has_dash` and dash key pressed and `dash_cooldown <= 0`, start dash.

**Step 3: Modify `src/game.py`**

After creating the player, apply powers from save_data:

```python
def apply_powers(player, save_data):
    player.has_double_jump = save_data.has_power("double_jump")
    player.has_dash = save_data.has_power("dash")
    player.has_wall_climb = save_data.has_power("wall_climb")
    player.has_shield = save_data.has_power("shield")
    if save_data.has_power("stinger_upgrade"):
        player.stinger_damage = 2
    player.hp = save_data.get_max_hp()
```

When a boss is defeated, unlock the power:
```python
power = ISLAND_POWER[current_island]
save_data.unlock_power(power)
save_data.save()
```

**Step 4: Verify — start game, check double jump doesn't work yet (no power). Later when island map exists, we'll test earning powers.**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 5: Commit**

```bash
git add src/systems/powers.py src/entities/player.py src/game.py
git commit -m "feat: add powers system with double jump, dash, wall climb, shield, stinger upgrade"
```

---

## Phase 5: Island Map & Game Flow (Tasks 13-14)

---

### Task 13: Add island map screen

**Files:**
- Create: `src/ui/island_map.py`
- Modify: `src/settings.py` (add new game states)
- Modify: `src/game.py` (add island map state + island/level tracking)

**Step 1: Add new game states to `src/settings.py`**

```python
STATE_ISLAND_MAP = "island_map"
STATE_LEVEL_SELECT = "level_select"

ISLAND_DATA = [
    {"name": "The Garden Isles",   "levels": 3, "color": (100, 180, 100)},
    {"name": "The Swamp",          "levels": 4, "color": (80, 120, 60)},
    {"name": "The Crystal Caves",  "levels": 5, "color": (100, 80, 200)},
    {"name": "The Volcano",        "levels": 6, "color": (200, 80, 40)},
    {"name": "The Shadow Fortress","levels": 7, "color": (80, 40, 120)},
]
```

**Step 2: Create `src/ui/island_map.py`**

This draws the island map with:
- 5 island landmasses sitting in animated water
- Hornet cursor on current selection
- Lock icons on locked islands
- Left/right to move, Enter to select
- "S" key opens shop
- Bottom bar showing powers
- Top showing coin count

Key class:
```python
class IslandMap:
    def __init__(self, save_data):
        self.save_data = save_data
        self.selected = 0  # which island is highlighted
        self.island_positions = []  # calculated x,y for each island
        self.wave_offset = 0

    def handle_input(self, event):
        """Returns action: None, ("play", island_index), or "shop" """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if self.selected < self.save_data.max_island_unlocked:
                    self.selected = min(self.selected + 1, 4)
            elif event.key == pygame.K_LEFT:
                self.selected = max(self.selected - 1, 0)
            elif event.key == pygame.K_RETURN:
                return ("play", self.selected)
            elif event.key == pygame.K_s:
                return "shop"
        return None

    def draw(self, screen):
        # Draw sky, water, islands, cursor, UI
        ...
```

**Step 3: Modify `src/game.py`**

Change the game flow:
- After title screen: go to `STATE_ISLAND_MAP` (not directly to playing)
- On island map: player selects island -> go to level select or start first incomplete level
- After beating a level: return to island map
- After beating a boss: unlock next island, grant power, return to island map
- After game over: return to island map (keep coins)

The current 3 levels (Garden, Hive, Throne Room) become island 0, levels 0-2. The current `create_level()` handles these already.

Add `current_island` and `current_level_in_island` variables alongside the existing `current_level`.

**Step 4: Verify — title screen -> island map shows 5 islands, only island 1 unlocked, can enter and play levels**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 5: Commit**

```bash
git add src/ui/island_map.py src/settings.py src/game.py
git commit -m "feat: add island map screen with 5 islands and level progression"
```

---

### Task 14: Add HP shop

**Files:**
- Create: `src/ui/shop.py`
- Modify: `src/game.py` (add shop state)

**Step 1: Create `src/ui/shop.py`**

A simple overlay or screen showing:
- Current coins
- "Buy +1 HP (50 coins)" button
- Hearts showing current HP upgrades (filled) and remaining (empty)
- "X purchased / 8 max"
- Press Enter to buy, Escape to close

```python
class Shop:
    def __init__(self, save_data):
        self.save_data = save_data

    def handle_input(self, event):
        """Returns "close" or None."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.save_data.buy_hp()
                self.save_data.save()
            elif event.key == pygame.K_ESCAPE:
                return "close"
        return None

    def draw(self, screen):
        # Semi-transparent overlay
        # Shop title, coin count, buy button, heart display
        ...
```

**Step 2: Modify `src/game.py`**

Add `STATE_SHOP = "shop"`. When island map returns `"shop"`, switch to shop state. When shop returns `"close"`, go back to island map.

**Step 3: Verify — go to island map, press S, see shop, buy HP if you have coins**

```bash
cd /home/dane/Games/hornet-game && python main.py
```

**Step 4: Commit**

```bash
git add src/ui/shop.py src/game.py
git commit -m "feat: add HP shop accessible from island map"
```

---

## Phase 6: New Islands Content (Tasks 15-18)

For each new island, create levels and a boss. The level data goes in `src/world/levels.py` and new bosses go in `src/entities/bosses.py`.

---

### Task 15: Add Island 2 — The Swamp (4 levels + Swamp Beetle Lord boss)

**Files:**
- Modify: `src/world/levels.py` (add 4 swamp levels)
- Modify: `src/entities/bosses.py` (add SwampBeetleLord)
- Create: sprite generation scripts as needed

**Step 1: Add swamp theme to LEVEL_THEMES in settings.py**

Add swamp colors and platform style.

**Step 2: Add 4 level layouts to `create_level()` in levels.py**

Levels for island 1 (the current ones) are indices 0-2.
Island 2 levels use a mapping: `(island_index, level_in_island)` -> level data.

Refactor `create_level()` to take `(island_index, level_index)` instead of just `level_num`. The current 3 levels map to `(0, 0)`, `(0, 1)`, `(0, 2)`.

Add 3 regular swamp levels + 1 boss level. Enemies are 1.5x HP, slightly faster. More enemies per level.

**Step 3: Create SwampBeetleLord boss**

A giant beetle that:
- Rolls into a ball and charges across the arena
- Stomps the ground to shake platforms
- Summons smaller beetles
- Has 15 HP (1.5x Wasp King's 10)
- Gives "dash" power on defeat

**Step 4: Generate swamp sprites**

Create a `make_swamp.py` script to generate swamp background layers and beetle sprites, similar to existing `make_bg.py`.

**Step 5: Verify — unlock island 2 (temporarily set max_island_unlocked=1 in save), play through all 4 levels, defeat boss**

**Step 6: Commit**

```bash
git add src/world/levels.py src/entities/bosses.py src/settings.py sprites/
git commit -m "feat: add Island 2 (The Swamp) with 4 levels and Swamp Beetle Lord boss"
```

---

### Task 16: Add Island 3 — The Crystal Caves (5 levels + Crystal Spider Queen)

**Step 1:** Add crystal cave theme, 4 regular levels + 1 boss level.

**Step 2:** Create Crystal Spider Queen boss:
- Drops from ceiling to attack
- Shoots crystal projectiles
- Creates web traps on platforms
- 22 HP (1.5x previous)
- Gives "wall_climb" power

**Step 3:** Generate crystal cave sprites.

**Step 4:** Verify and commit.

```bash
git commit -m "feat: add Island 3 (Crystal Caves) with 5 levels and Crystal Spider Queen boss"
```

---

### Task 17: Add Island 4 — The Volcano (6 levels + Fire Moth boss)

**Step 1:** Add volcano theme, 5 regular levels + 1 boss level.

**Step 2:** Create Fire Moth boss:
- Flies in erratic patterns
- Drops fire balls that leave burning patches
- Creates walls of flame
- 33 HP
- Gives "shield" power

**Step 3:** Generate volcano sprites.

**Step 4:** Verify and commit.

```bash
git commit -m "feat: add Island 4 (Volcano) with 6 levels and Fire Moth boss"
```

---

### Task 18: Add Island 5 — The Shadow Fortress (7 levels + Shadow Hornet boss)

**Step 1:** Add shadow fortress theme, 6 regular levels + 1 boss level.

**Step 2:** Create Shadow Hornet boss (final boss!):
- Mirror of the player — has all the same moves but darker
- Charges, jumps, attacks with a shadow stinger
- Teleports behind the player
- Gets faster as HP drops
- 50 HP
- Gives "stinger_upgrade" power

**Step 3:** Generate shadow fortress sprites.

**Step 4:** Verify full game: play all 5 islands, defeat all bosses, earn all powers.

**Step 5:** Commit.

```bash
git commit -m "feat: add Island 5 (Shadow Fortress) with 7 levels and Shadow Hornet final boss"
```

---

## Phase 7: Polish (Task 19)

### Task 19: Final integration and cleanup

**Files:**
- Modify: `src/game.py`
- Clean up: root directory patch/make scripts

**Step 1:** Add a "Game Complete!" screen after defeating Island 5's boss showing all powers earned, total coins, etc.

**Step 2:** Move all the `make_*.py`, `patch_*.py`, `fix.py` scripts to an `archive/` or `tools/` folder to clean up the root directory.

**Step 3:** Update `README.md` with the new game description.

**Step 4:** Full playtest and commit.

```bash
git add -A
git commit -m "feat: polish game complete screen, clean up root directory"
```

**Step 5:** Push to GitHub.

```bash
git push
```
