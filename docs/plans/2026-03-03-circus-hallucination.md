# Circus + Hallucination Land Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a post-game boss rush (The Circus) and a hard endgame world (Hallucination Land) that unlock after beating the final boss.

**Architecture:** Build in two phases — Phase 1 is The Circus (boss rush with one-life rules, reuses existing boss classes with difficulty multipliers), Phase 2 is Hallucination Land (5 new islands, shadow enemies, special shop with shadow powers). New game states are added to settings.py and wired into the existing state machine in game.py.

**Tech Stack:** Python, Pygame, existing island/level/boss/shop system

---

## PHASE 1 — THE CIRCUS

---

### Task 1: Add circus + hallucination fields to save_data.py

**Files:**
- Modify: `src/save_data.py`

**Step 1: Add new fields to `__init__`**

In `SaveData.__init__`, after `self.powers = []`, add:
```python
self.circus_unlocked = False
self.hallucination_unlocked = False
self.hallucination_island = 0
self.shadow_powers = []
self.hallucination_lives = 0  # stock of lives for Hallucination Land
```

**Step 2: Update `save()` to include new fields**

Add these keys to the `data` dict:
```python
"circus_unlocked": self.circus_unlocked,
"hallucination_unlocked": self.hallucination_unlocked,
"hallucination_island": self.hallucination_island,
"shadow_powers": self.shadow_powers,
"hallucination_lives": self.hallucination_lives,
```

**Step 3: Update `load()` to read new fields**

Add after the existing `load()` calls:
```python
self.circus_unlocked = data.get("circus_unlocked", False)
self.hallucination_unlocked = data.get("hallucination_unlocked", False)
self.hallucination_island = data.get("hallucination_island", 0)
self.shadow_powers = data.get("shadow_powers", [])
self.hallucination_lives = data.get("hallucination_lives", 0)
```

**Step 4: Add helper methods at bottom of class**

```python
def unlock_circus(self):
    if not self.circus_unlocked:
        self.circus_unlocked = True
        self.save()

def unlock_hallucination(self):
    if not self.hallucination_unlocked:
        self.hallucination_unlocked = True
        self.save()

def has_shadow_power(self, power_name):
    return power_name in self.shadow_powers

def unlock_shadow_power(self, power_name):
    if power_name not in self.shadow_powers:
        self.shadow_powers.append(power_name)

def buy_hallucination_lives(self, amount, cost):
    """Buy up to 10 lives for Hallucination Land."""
    if self.hallucination_lives >= 10:
        return False
    if self.coins < cost:
        return False
    to_buy = min(amount, 10 - self.hallucination_lives)
    self.coins -= cost * to_buy
    self.hallucination_lives += to_buy
    return True

def use_hallucination_life(self):
    if self.hallucination_lives <= 0:
        return False
    self.hallucination_lives -= 1
    return True
```

**Step 5: Run the game to verify no crash**

```bash
cd ~/Games/hornet-game && python main.py
```
Expected: Game boots to title screen normally.

**Step 6: Commit**

```bash
git add src/save_data.py
git commit -m "feat: add circus and hallucination save fields"
```

---

### Task 2: Add new game states and circus constants to settings.py

**Files:**
- Modify: `src/settings.py`

**Step 1: Add new game states after the existing STATE_ constants**

```python
# Circus (boss rush) states
STATE_CIRCUS        = "circus"        # The circus lobby/intro screen
STATE_CIRCUS_BOSS   = "circus_boss"   # Fighting a circus boss
STATE_CIRCUS_FAIL   = "circus_fail"   # Died — show restart screen
STATE_CIRCUS_WIN    = "circus_win"    # Beat all 5 — portal appears

# Hallucination Land states
STATE_HALLUCINATION_MAP     = "hallucination_map"
STATE_HALLUCINATION_PLAYING = "hallucination_playing"
STATE_HALLUCINATION_SHOP    = "hallucination_shop"
```

**Step 2: Add circus boss order and multipliers**

```python
# Circus — boss rush settings
# Bosses in order: island 0 → 1 → 2 → 3 → 4
CIRCUS_BOSS_ORDER = [0, 1, 2, 3, 4]   # island index for each circus fight
CIRCUS_HP_MULT    = 1.5   # bosses have 50% more HP
CIRCUS_SPEED_MULT = 1.25  # bosses move 25% faster
CIRCUS_DAMAGE_ADD = 1     # bosses deal +1 extra damage
```

**Step 3: Add Hallucination Land island data**

```python
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
```

**Step 4: Run the game to verify no crash**

```bash
python main.py
```
Expected: Game boots normally — settings.py is just constants.

**Step 5: Commit**

```bash
git add src/settings.py
git commit -m "feat: add circus and hallucination constants to settings"
```

---

### Task 3: Add shadow powers to powers.py

**Files:**
- Modify: `src/systems/powers.py`

**Step 1: Add shadow power name constants**

After `POWER_STINGER_UPGRADE = "stinger_upgrade"`, add:

```python
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
```

**Step 2: Commit**

```bash
git add src/systems/powers.py
git commit -m "feat: define shadow powers for Hallucination Land"
```

---

### Task 4: Show The Circus on the island map

**Files:**
- Modify: `src/ui/island_map.py`

**Step 1: Update `handle_input` to navigate to The Circus**

The island map currently lets you go right up to index 4 (5 islands). We need a 6th slot for The Circus. Change the right-arrow logic:

```python
if event.key == pygame.K_RIGHT:
    max_sel = 5 if self.save_data.circus_unlocked else min(self.save_data.max_island_unlocked, 4)
    if self.selected < max_sel:
        self.selected += 1
```

Change the ENTER handler:
```python
elif event.key == pygame.K_RETURN:
    if self.selected == 5:
        return "circus"   # new return value
    return ("play", self.selected)
```

**Step 2: Draw The Circus island in `draw()`**

After the `for i, island in enumerate(ISLAND_DATA):` loop, add a 6th island for The Circus:

```python
# Draw The Circus (slot 5) if unlocked
if self.save_data.circus_unlocked:
    ix = start_x + 5 * island_spacing
    iy = 340
    height = 90
    color = (220, 80, 80)  # circus red
    points = [
        (ix - 40, iy + 20),
        (ix - 30, iy - height // 2),
        (ix - 10, iy - height),
        (ix + 10, iy - height + 10),
        (ix + 30, iy - height // 2 - 5),
        (ix + 40, iy + 20),
    ]
    pygame.draw.polygon(screen, color, points)
    pygame.draw.polygon(screen, (160, 40, 40), points, 3)
    name_t = self.font_small.render("THE CIRCUS", True, WHITE)
    screen.blit(name_t, (ix - name_t.get_width() // 2, iy + 30))
    sub_t = self.font_small.render("BOSS RUSH", True, (220, 180, 180))
    screen.blit(sub_t, (ix - sub_t.get_width() // 2, iy + 50))

    if self.selected == 5:
        bounce = math.sin(self.wave_offset * 3) * 5
        arrow_y = iy - height - 40 + bounce
        pygame.draw.polygon(screen, (255, 80, 80), [
            (ix, arrow_y + 15),
            (ix - 10, arrow_y),
            (ix + 10, arrow_y),
        ])
```

**Step 3: Run the game, beat the game (or temporarily unlock circus in the REPL) and check the map shows The Circus**

Quick test: open `save_data.json`, set `"circus_unlocked": true`, run the game, go to island map. You should see The Circus on the right.

**Step 4: Commit**

```bash
git add src/ui/island_map.py
git commit -m "feat: show The Circus on island map when unlocked"
```

---

### Task 5: Create the Circus screen (lobby + boss rush flow)

**Files:**
- Create: `src/ui/circus.py`

**Step 1: Write the file**

```python
import pygame
import math
from src.settings import *


class CircusLobby:
    """The Circus intro screen — shows boss order, rules, lets player start."""

    BOSS_NAMES = [
        "Wasp King",
        "Swamp Beetle Lord",
        "Crystal Spider Queen",
        "Fire Moth",
        "Shadow Hornet",
    ]

    def __init__(self):
        self.font_big = None
        self.font_med = None
        self.font_small = None
        self.wave = 0

    def _init_fonts(self):
        if self.font_big is None:
            self.font_big   = pygame.font.Font(None, 56)
            self.font_med   = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        """Returns 'start' to begin, 'back' to go back to island map."""
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_RETURN:
            return "start"
        if event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, screen):
        self._init_fonts()
        self.wave += 0.03

        # Dark red background
        screen.fill((25, 5, 5))

        # Flashing title
        pulse = abs(math.sin(self.wave * 2))
        r = int(200 + pulse * 55)
        title = self.font_big.render("THE CIRCUS", True, (r, 60, 60))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        sub = self.font_med.render("BOSS RUSH", True, (200, 150, 150))
        screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 90))

        # Rules
        rules = [
            "Fight all 5 bosses — stronger than ever.",
            "One life. Die once and you start over.",
            "Beat them all to open the portal.",
        ]
        ry = 140
        for rule in rules:
            rt = self.font_small.render(rule, True, (200, 180, 180))
            screen.blit(rt, (SCREEN_WIDTH // 2 - rt.get_width() // 2, ry))
            ry += 26

        # Boss list
        by = 260
        list_title = self.font_med.render("BOSSES:", True, (220, 100, 100))
        screen.blit(list_title, (SCREEN_WIDTH // 2 - list_title.get_width() // 2, by))
        by += 36
        for i, name in enumerate(self.BOSS_NAMES):
            bt = self.font_small.render(f"{i+1}. {name}", True, (200, 160, 160))
            screen.blit(bt, (SCREEN_WIDTH // 2 - bt.get_width() // 2, by))
            by += 26

        # Prompt
        blink = int(self.wave * 3) % 2 == 0
        if blink:
            prompt = self.font_med.render("ENTER to begin  |  ESC to go back", True, (255, 200, 200))
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT - 50))


class CircusFail:
    """Screen shown when player dies in the circus."""

    def __init__(self, boss_reached):
        self.boss_reached = boss_reached  # 0-indexed, how far they got
        self.font_big = None
        self.font_med = None
        self.font_small = None

    def _init_fonts(self):
        if self.font_big is None:
            self.font_big   = pygame.font.Font(None, 56)
            self.font_med   = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        """Returns 'retry' or 'back'."""
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_RETURN:
            return "retry"
        if event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, screen):
        self._init_fonts()
        screen.fill((20, 0, 0))

        title = self.font_big.render("YOU FELL.", True, (200, 50, 50))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        msg = self.font_med.render(f"Reached boss {self.boss_reached + 1} of 5", True, (180, 130, 130))
        screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))

        sub = self.font_small.render("The circus starts over...", True, (150, 100, 100))
        screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 250))

        prompt = self.font_med.render("ENTER to try again  |  ESC to leave", True, (200, 160, 160))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT - 80))


class CircusWin:
    """Screen shown when player beats all 5 circus bosses."""

    def __init__(self):
        self.font_big = None
        self.font_med = None
        self.font_small = None
        self.wave = 0

    def _init_fonts(self):
        if self.font_big is None:
            self.font_big   = pygame.font.Font(None, 56)
            self.font_med   = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        """Returns 'enter_portal' or 'back'."""
        if event.type != pygame.KEYDOWN:
            return None
        if event.key == pygame.K_RETURN:
            return "enter_portal"
        if event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, screen):
        self._init_fonts()
        self.wave += 0.03
        screen.fill((5, 0, 20))

        pulse = abs(math.sin(self.wave * 2))
        r = int(100 + pulse * 100)
        b = int(200 + pulse * 55)
        title = self.font_big.render("YOU CONQUERED THE CIRCUS!", True, (r, 50, b))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        msg = self.font_med.render("The portal to Hallucination Land is open.", True, (180, 150, 220))
        screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 210))

        prompt = self.font_med.render("ENTER to enter the portal", True, (200, 180, 255))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT - 80))
```

**Step 2: Run the game — verify no import errors**

```bash
python -c "from src.ui.circus import CircusLobby, CircusFail, CircusWin; print('OK')"
```
Expected: `OK`

**Step 3: Commit**

```bash
git add src/ui/circus.py
git commit -m "feat: create Circus lobby, fail, and win screens"
```

---

### Task 6: Wire The Circus into game.py

**Files:**
- Modify: `src/game.py`

**Step 1: Import new classes at the top of game.py**

After the existing imports, add:
```python
from src.ui.circus import CircusLobby, CircusFail, CircusWin
```

**Step 2: Add circus state variables near the other state variables (around line 104)**

```python
# Circus state
circus_lobby = None
circus_fail_screen = None
circus_win_screen = None
circus_boss_index = 0   # which circus boss we're currently on (0-4)
```

**Step 3: Add a `start_circus_boss()` helper function near `start_level()`**

```python
def start_circus_boss():
    """Set up a circus boss fight. Applies difficulty multipliers."""
    nonlocal platforms, enemies, particles, player, camera, boss, bg, prev_boss_state, boss_music_started, coin_manager
    coin_manager = CoinManager()
    particles = []
    enemies = []

    island_idx = CIRCUS_BOSS_ORDER[circus_boss_index]

    # Use the boss level layout of that island
    island_info = ISLAND_DATA[island_idx]
    boss_level = island_info["levels"] - 1
    platforms, _ = create_level(island_idx, boss_level)  # get the arena platforms

    player = Player(50, 400)
    apply_powers(player, save_data)
    camera = Camera()

    # Background matches the island
    if island_idx == 0:
        bg = ParallaxBackground(boss_level)
    elif island_idx == 1:
        bg = ParallaxBackground("swamp")
    elif island_idx == 2:
        bg = ParallaxBackground("cave")
    elif island_idx == 3:
        bg = ParallaxBackground("volcano")
    else:
        bg = ParallaxBackground("shadow")

    # Spawn the right boss with multipliers applied
    if island_idx == 0:
        boss = WaspKing(1800, 540 - 90)
    elif island_idx == 1:
        boss = SwampBeetleLord(1800, 540 - 80)
    elif island_idx == 2:
        boss = CrystalSpiderQueen(1900, 350)
    elif island_idx == 3:
        boss = FireMoth(2000, 300)
    else:
        boss = ShadowHornet(2200, 350)

    # Apply circus difficulty multipliers
    boss.max_hp = int(boss.max_hp * CIRCUS_HP_MULT)
    boss.hp     = boss.max_hp
    if hasattr(boss, 'speed_multiplier'):
        boss.speed_multiplier *= CIRCUS_SPEED_MULT
    if hasattr(boss, 'charge_speed'):
        boss.charge_speed = int(boss.charge_speed * CIRCUS_SPEED_MULT)
    boss._circus_damage_add = CIRCUS_DAMAGE_ADD  # flag checked in combat

    prev_boss_state = "idle"
    boss_music_started = False
```

**Step 4: Handle island_map returning "circus"**

In the `if game_state == STATE_ISLAND_MAP` event block, after the existing `result` checks, add:

```python
elif result == "circus":
    circus_lobby = CircusLobby()
    game_state = STATE_CIRCUS
```

**Step 5: Handle STATE_CIRCUS events**

In the main event loop, add a new block:

```python
if game_state == STATE_CIRCUS and circus_lobby:
    result = circus_lobby.handle_input(event)
    if result == "start":
        circus_boss_index = 0
        start_circus_boss()
        game_state = STATE_CIRCUS_BOSS
        play_music("boss_music" if "boss_music" in sounds else "level_music")
    elif result == "back":
        island_map = IslandMap(save_data)
        game_state = STATE_ISLAND_MAP

if game_state == STATE_CIRCUS_FAIL and circus_fail_screen:
    result = circus_fail_screen.handle_input(event)
    if result == "retry":
        circus_boss_index = 0
        start_circus_boss()
        game_state = STATE_CIRCUS_BOSS
    elif result == "back":
        island_map = IslandMap(save_data)
        game_state = STATE_ISLAND_MAP

if game_state == STATE_CIRCUS_WIN and circus_win_screen:
    result = circus_win_screen.handle_input(event)
    if result == "enter_portal":
        save_data.unlock_hallucination()
        island_map = IslandMap(save_data)  # placeholder until hallucination map exists
        game_state = STATE_ISLAND_MAP      # TODO: switch to STATE_HALLUCINATION_MAP
    elif result == "back":
        island_map = IslandMap(save_data)
        game_state = STATE_ISLAND_MAP
```

**Step 6: Handle STATE_CIRCUS_BOSS in the game update loop**

The circus boss fight uses the same playing loop as a normal boss level. Find the section that checks `game_state == STATE_PLAYING` and the boss-death section. In the boss-death check, add handling for circus mode:

Find the boss death code (around where `boss.alive == False` leads to level complete). Add an extra check:

```python
# If we're in a circus boss fight, advance to next boss (or win)
if game_state == STATE_CIRCUS_BOSS and boss and not boss.alive:
    if circus_boss_index < 4:
        circus_boss_index += 1
        start_circus_boss()
        # stay in STATE_CIRCUS_BOSS
    else:
        # Beat all 5 — circus win!
        circus_win_screen = CircusWin()
        game_state = STATE_CIRCUS_WIN
        stop_music()
```

And player death while in circus:
```python
# In circus, dying goes to fail screen (not game over)
if game_state == STATE_CIRCUS_BOSS and player and player.hp <= 0:
    circus_fail_screen = CircusFail(circus_boss_index)
    game_state = STATE_CIRCUS_FAIL
    stop_music()
```

**Step 7: Draw circus states**

Add draw calls for the new states in the drawing section:

```python
elif game_state == STATE_CIRCUS and circus_lobby:
    circus_lobby.draw(screen)
elif game_state == STATE_CIRCUS_FAIL and circus_fail_screen:
    circus_fail_screen.draw(screen)
elif game_state == STATE_CIRCUS_WIN and circus_win_screen:
    circus_win_screen.draw(screen)
elif game_state == STATE_CIRCUS_BOSS:
    # Uses the same drawing code as STATE_PLAYING — handled there
    pass
```

**Note on STATE_CIRCUS_BOSS drawing:** The playing draw loop checks `game_state == STATE_PLAYING`. Change it to:

```python
if game_state in (STATE_PLAYING, STATE_CIRCUS_BOSS):
```

And similarly for the update loop.

**Step 8: Trigger circus unlock when Shadow Hornet dies**

Find where the ShadowHornet (island 4 boss) death is handled and island 4 is completed. After `save_data.unlock_power(...)` is called for island 4, add:

```python
save_data.unlock_circus()
```

**Step 9: Test the circus flow**

1. Temporarily set `save_data.circus_unlocked = True` in `SaveData.__init__` for testing
2. Run the game, go to island map, navigate right to The Circus
3. Press Enter → should see CircusLobby screen
4. Press Enter again → should fight WaspKing (with bigger HP)
5. Kill the boss → should advance to boss 2
6. Die → should see CircusFail, ENTER retries from boss 1
7. Beat all 5 → should see CircusWin
8. Undo the temp change once done testing

**Step 10: Commit**

```bash
git add src/game.py
git commit -m "feat: wire The Circus boss rush into game.py"
```

---

## PHASE 2 — HALLUCINATION LAND

---

### Task 7: Create hallucination level generation

**Files:**
- Create: `src/world/hallucination_levels.py`

**Step 1: Write the file**

Hallucination levels reuse the same platform layouts as the normal islands but make ALL enemies shadow + scaled up:

```python
from src.settings import *
from src.world.levels import create_level
from src.entities.enemies import Wasp, Fly, Spider


def create_hallucination_level(island, level):
    """Return (platforms, enemies) for a Hallucination Land level.

    Reuses the normal level platforms but:
    - All enemies are shadow form (trait = "shadow")
    - Enemies have +100% HP and +25% speed
    - Each level has one boss (handled separately in game.py)
    """
    # Re-use the matching normal island's level layout
    # Map hallucination island 0-4 → normal island 0-4
    # Map hallucination level 0-2 → normal island levels 0-2
    # Level 3 (boss level) uses normal island's boss level layout
    normal_island = island
    normal_level = min(level, ISLAND_DATA[normal_island]["levels"] - 1)

    platforms, enemies = create_level(normal_island, normal_level)

    # Override theme color for all platforms
    theme_color = HALLUCINATION_LEVEL_THEMES[island][level]["platform"]
    for p in platforms:
        p.color = theme_color

    # Make all enemies shadow + stronger
    shadow_enemies = []
    for e in enemies:
        # Add shadow trait
        if "shadow" not in e.traits:
            e.traits.append("shadow")
        # Double HP
        e.hp = max(1, e.hp * 2)
        # Speed boost
        if hasattr(e, 'speed'):
            e.speed *= 1.25
        shadow_enemies.append(e)

    return platforms, shadow_enemies
```

**Step 2: Verify import works**

```bash
python -c "from src.world.hallucination_levels import create_hallucination_level; print('OK')"
```
Expected: `OK`

**Step 3: Commit**

```bash
git add src/world/hallucination_levels.py
git commit -m "feat: hallucination level generator — shadow enemies, scaled stats"
```

---

### Task 8: Create the Hallucination island map

**Files:**
- Create: `src/ui/hallucination_map.py`

**Step 1: Write the file**

```python
import pygame
import math
from src.settings import *


class HallucinationMap:
    """Island map for Hallucination Land — dark, eerie version."""

    def __init__(self, save_data):
        self.save_data = save_data
        self.selected = 0
        self.wave_offset = 0
        self.font_big = None
        self.font_med = None
        self.font_small = None

    def _init_fonts(self):
        if self.font_big is None:
            self.font_big   = pygame.font.Font(None, 48)
            self.font_med   = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        """Returns:
           - ("play", island_index) to start playing
           - ("shop", island_index) to open the hallucination shop
           - None for no action
        """
        if event.type != pygame.KEYDOWN:
            return None

        max_sel = min(self.save_data.hallucination_island, 4)
        if event.key == pygame.K_RIGHT:
            if self.selected < max_sel:
                self.selected += 1
        elif event.key == pygame.K_LEFT:
            if self.selected > 0:
                self.selected -= 1
        elif event.key == pygame.K_RETURN:
            return ("play", self.selected)
        elif event.key == pygame.K_s:
            return ("shop", self.selected)
        return None

    def draw(self, screen):
        self._init_fonts()
        self.wave_offset += 0.03

        # Dark void background
        screen.fill((5, 0, 15))

        # Eerie mist at bottom
        for row in range(400, SCREEN_HEIGHT):
            depth = (row - 400) / (SCREEN_HEIGHT - 400)
            r = int(20 * depth)
            g = 0
            b = int(40 * depth)
            pygame.draw.line(screen, (r, g, b), (0, row), (SCREEN_WIDTH, row))

        # Draw hallucination islands
        island_spacing = 140
        start_x = 80
        for i, island in enumerate(HALLUCINATION_ISLAND_DATA):
            ix = start_x + i * island_spacing
            iy = 340

            is_unlocked = i <= self.save_data.hallucination_island
            color = island["color"] if is_unlocked else (40, 20, 60)

            height = 70 + i * 12
            points = [
                (ix - 40, iy + 20),
                (ix - 30, iy - height // 2),
                (ix - 10, iy - height),
                (ix + 10, iy - height + 10),
                (ix + 30, iy - height // 2 - 5),
                (ix + 40, iy + 20),
            ]
            pygame.draw.polygon(screen, color, points)
            darker = (max(0, color[0]-20), max(0, color[1]-10), max(0, color[2]-20))
            pygame.draw.polygon(screen, darker, points, 3)

            name_text = self.font_small.render(island["name"], True, (200, 150, 220) if is_unlocked else (60, 40, 80))
            screen.blit(name_text, (ix - name_text.get_width() // 2, iy + 30))

            if not is_unlocked:
                lock_text = self.font_med.render("LOCKED", True, (80, 30, 80))
                screen.blit(lock_text, (ix - lock_text.get_width() // 2, iy - height - 30))

            if i == self.selected:
                bounce = math.sin(self.wave_offset * 3) * 5
                arrow_y = iy - height - 40 + bounce
                pygame.draw.polygon(screen, (180, 80, 255), [
                    (ix, arrow_y + 15),
                    (ix - 10, arrow_y),
                    (ix + 10, arrow_y),
                ])

        # Title
        title = self.font_big.render("HALLUCINATION LAND", True, (160, 80, 220))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        # Coin counter
        coin_text = self.font_med.render(f"Coins: {self.save_data.coins}", True, (200, 180, 255))
        screen.blit(coin_text, (20, 20))

        # Lives counter
        lives_color = (50, 200, 50) if self.save_data.hallucination_lives > 0 else (150, 50, 50)
        lives_text = self.font_med.render(f"Lives: {self.save_data.hallucination_lives}/10", True, lives_color)
        screen.blit(lives_text, (20, 50))

        # Hint
        ctrl_text = self.font_small.render("LEFT/RIGHT to select  |  ENTER to play  |  S for shop", True, (120, 90, 150))
        screen.blit(ctrl_text, (SCREEN_WIDTH // 2 - ctrl_text.get_width() // 2, SCREEN_HEIGHT - 30))
```

**Step 2: Verify import**

```bash
python -c "from src.ui.hallucination_map import HallucinationMap; print('OK')"
```
Expected: `OK`

**Step 3: Commit**

```bash
git add src/ui/hallucination_map.py
git commit -m "feat: Hallucination Land island map screen"
```

---

### Task 9: Create the Hallucination shop

**Files:**
- Create: `src/ui/hallucination_shop.py`

**Step 1: Write the file**

```python
import pygame
from src.settings import *
from src.systems.powers import (
    ALL_SHADOW_POWERS, HALLUCINATION_ISLAND_POWER,
    SHADOW_POWER_COST, SHADOW_POWER_DESC
)

HSHOP_LIFE_COST  = 100   # cost per extra life
HSHOP_LIFE_STOCK = 10    # max lives you can hold


class HallucinationShop:
    """Special shop in Hallucination Land. Sells lives + shadow powers."""

    def __init__(self, save_data, island_index):
        self.save_data = save_data
        self.island_index = island_index
        self.font_big = None
        self.font_med = None
        self.font_small = None
        self.message = ""
        self.message_timer = 0
        self.selected = 0   # 0 = lives, 1 = shadow power

        from src.systems.powers import HALLUCINATION_ISLAND_POWER
        self.shadow_power = HALLUCINATION_ISLAND_POWER.get(island_index)

    def _init_fonts(self):
        if self.font_big is None:
            self.font_big   = pygame.font.Font(None, 48)
            self.font_med   = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return None
        if event.key in (pygame.K_ESCAPE, pygame.K_s):
            return "close"
        elif event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % 2
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % 2
        elif event.key == pygame.K_RETURN:
            if self.selected == 0:
                self._buy_life()
            else:
                self._buy_shadow_power()
        return None

    def _buy_life(self):
        if self.save_data.hallucination_lives >= HSHOP_LIFE_STOCK:
            self.message = "Already at max lives!"
        elif self.save_data.coins < HSHOP_LIFE_COST:
            self.message = "Not enough coins!"
        else:
            self.save_data.coins -= HSHOP_LIFE_COST
            self.save_data.hallucination_lives += 1
            self.save_data.save()
            self.message = "Got 1 extra life!"
        self.message_timer = 90

    def _buy_shadow_power(self):
        if self.shadow_power is None:
            return
        if self.save_data.has_shadow_power(self.shadow_power):
            self.message = "Already have this power!"
        elif self.save_data.coins < SHADOW_POWER_COST[self.shadow_power]:
            self.message = "Not enough coins!"
        else:
            self.save_data.coins -= SHADOW_POWER_COST[self.shadow_power]
            self.save_data.unlock_shadow_power(self.shadow_power)
            self.save_data.save()
            self.message = "Shadow power unlocked!"
        self.message_timer = 90

    def draw(self, screen):
        self._init_fonts()
        screen.fill((5, 0, 20))

        title = self.font_big.render("SHADOW SHOP", True, (160, 80, 220))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        coin_t = self.font_med.render(f"Coins: {self.save_data.coins}", True, (200, 180, 255))
        screen.blit(coin_t, (SCREEN_WIDTH // 2 - coin_t.get_width() // 2, 80))

        nav = self.font_small.render("UP/DOWN to select  |  ENTER to buy  |  ESC to go back", True, (120, 90, 160))
        screen.blit(nav, (SCREEN_WIDTH // 2 - nav.get_width() // 2, 112))

        # Two boxes side by side
        box_w, box_h = 280, 220
        gap = 40
        total_w = box_w * 2 + gap
        start_x = SCREEN_WIDTH // 2 - total_w // 2
        box_y = 148

        # --- Lives box ---
        lx = start_x
        lc = (180, 100, 255) if self.selected == 0 else (70, 40, 100)
        pygame.draw.rect(screen, (20, 10, 40), (lx, box_y, box_w, box_h))
        pygame.draw.rect(screen, lc, (lx, box_y, box_w, box_h), 3)

        lt = self.font_med.render("+1 Life", True, WHITE)
        screen.blit(lt, (lx + box_w//2 - lt.get_width()//2, box_y + 14))

        can_afford = self.save_data.coins >= HSHOP_LIFE_COST
        at_max = self.save_data.hallucination_lives >= HSHOP_LIFE_STOCK
        pc = (50, 200, 50) if can_afford and not at_max else (200, 50, 50)
        pt = self.font_med.render(f"Cost: {HSHOP_LIFE_COST} coins", True, pc)
        screen.blit(pt, (lx + box_w//2 - pt.get_width()//2, box_y + 50))

        owned_t = self.font_small.render(
            f"Lives: {self.save_data.hallucination_lives} / {HSHOP_LIFE_STOCK}",
            True, (200, 180, 255)
        )
        screen.blit(owned_t, (lx + box_w//2 - owned_t.get_width()//2, box_y + 90))

        desc_t = self.font_small.render("Respawn once in Hallucination Land", True, (160, 140, 200))
        screen.blit(desc_t, (lx + box_w//2 - desc_t.get_width()//2, box_y + 115))

        if at_max:
            pr_t = self.font_small.render("MAX LIVES", True, (255, 220, 50))
        else:
            pr_t = self.font_small.render("ENTER to buy", True, (180, 160, 220))
        screen.blit(pr_t, (lx + box_w//2 - pr_t.get_width()//2, box_y + 190))

        # --- Shadow power box ---
        sx = start_x + box_w + gap
        sc = (180, 100, 255) if self.selected == 1 else (70, 40, 100)
        pygame.draw.rect(screen, (20, 10, 40), (sx, box_y, box_w, box_h))
        pygame.draw.rect(screen, sc, (sx, box_y, box_w, box_h), 3)

        if self.shadow_power:
            power_name = self.shadow_power.replace("_", " ").upper()
            cost = SHADOW_POWER_COST[self.shadow_power]
            desc = SHADOW_POWER_DESC[self.shadow_power]
            already_have = self.save_data.has_shadow_power(self.shadow_power)

            spt = self.font_med.render(power_name, True, (200, 150, 255))
            screen.blit(spt, (sx + box_w//2 - spt.get_width()//2, box_y + 14))

            sp_cost_c = (50, 200, 50) if self.save_data.coins >= cost and not already_have else (200, 50, 50)
            sp_ct = self.font_med.render(f"Cost: {cost} coins", True, sp_cost_c)
            screen.blit(sp_ct, (sx + box_w//2 - sp_ct.get_width()//2, box_y + 50))

            # Word-wrap description (simple — split at spaces)
            words = desc.split()
            line, lines_out = "", []
            for w in words:
                if len(line) + len(w) < 30:
                    line += w + " "
                else:
                    lines_out.append(line)
                    line = w + " "
            lines_out.append(line)
            for k, ln in enumerate(lines_out):
                ln_t = self.font_small.render(ln, True, (160, 140, 200))
                screen.blit(ln_t, (sx + box_w//2 - ln_t.get_width()//2, box_y + 90 + k * 22))

            if already_have:
                owned_sp = self.font_small.render("OWNED", True, (255, 220, 50))
                screen.blit(owned_sp, (sx + box_w//2 - owned_sp.get_width()//2, box_y + 190))
            else:
                buy_sp = self.font_small.render("ENTER to buy", True, (180, 160, 220))
                screen.blit(buy_sp, (sx + box_w//2 - buy_sp.get_width()//2, box_y + 190))

        # Feedback message
        if self.message_timer > 0:
            self.message_timer -= 1
            ok = "Got" in self.message or "unlocked" in self.message
            mc = (50, 200, 50) if ok else (200, 50, 50)
            mt = self.font_med.render(self.message, True, mc)
            screen.blit(mt, (SCREEN_WIDTH // 2 - mt.get_width() // 2, box_y + box_h + 20))

        close_t = self.font_small.render("ESC or S to go back", True, (100, 80, 130))
        screen.blit(close_t, (SCREEN_WIDTH // 2 - close_t.get_width() // 2, SCREEN_HEIGHT - 30))
```

**Step 2: Verify import**

```bash
python -c "from src.ui.hallucination_shop import HallucinationShop; print('OK')"
```
Expected: `OK`

**Step 3: Commit**

```bash
git add src/ui/hallucination_shop.py
git commit -m "feat: Hallucination Land shop — lives + shadow powers"
```

---

### Task 10: Apply shadow powers to the player in game.py

**Files:**
- Modify: `src/game.py`

**Step 1: Extend `apply_powers()` to also apply shadow powers**

Find the `apply_powers(player, save_data)` function and add at the bottom:

```python
# Shadow powers
from src.systems.powers import SHADOW_VEIL, SHADOW_WINGS, SHADOW_FORM, SHADOW_STINGER, SHADOW_DASH
if save_data.has_shadow_power(SHADOW_WINGS):
    player.hover_max = 99999    # effectively infinite
if save_data.has_shadow_power(SHADOW_FORM):
    player.shadow_form = True   # player takes half damage (handled in player.take_damage)
if save_data.has_shadow_power(SHADOW_STINGER):
    player.shadow_stinger = True  # flag checked in combat
if save_data.has_shadow_power(SHADOW_VEIL):
    player.has_shadow_veil = True  # adds a new active ability (cooldown handled in player.py)
if save_data.has_shadow_power(SHADOW_DASH):
    player.shadow_dash = True   # dash is damage-immune (handled in player.py)
```

**Step 2: Add shadow_form half-damage to Player.take_damage in `src/entities/player.py`**

Find `take_damage` in player.py. At the very top of the method:

```python
def take_damage(self, amount):
    if getattr(self, 'shadow_form', False):
        amount = max(1, amount // 2)
    # ... rest of existing code ...
```

**Step 3: Add shadow_veil ability (V key) to Player in `src/entities/player.py`**

In `Player.__init__`, add:
```python
self.has_shadow_veil = False
self.shadow_veil_active = False
self.shadow_veil_timer = 0     # countdown while active (180 frames = 3 sec)
self.shadow_veil_cooldown = 0  # countdown before can use again (1800 = 30 sec)
```

In `Player.update()`, add:
```python
if self.shadow_veil_active:
    self.shadow_veil_timer -= 1
    if self.shadow_veil_timer <= 0:
        self.shadow_veil_active = False
        self.shadow_veil_cooldown = 1800
elif self.shadow_veil_cooldown > 0:
    self.shadow_veil_cooldown -= 1
```

In `take_damage`, add at the very top (before shadow_form check):
```python
if getattr(self, 'shadow_veil_active', False):
    return  # invincible while veil is active
```

In game.py event handling (K_v key):
```python
if event.key == pygame.K_v and game_state in (STATE_PLAYING, STATE_HALLUCINATION_PLAYING):
    if player and getattr(player, 'has_shadow_veil', False):
        if not player.shadow_veil_active and player.shadow_veil_cooldown == 0:
            player.shadow_veil_active = True
            player.shadow_veil_timer = 180
```

**Step 4: Commit**

```bash
git add src/game.py src/entities/player.py
git commit -m "feat: apply shadow powers to player (shadow form, veil, wings)"
```

---

### Task 11: Wire Hallucination Land into game.py

**Files:**
- Modify: `src/game.py`

**Step 1: Import new classes**

```python
from src.ui.hallucination_map import HallucinationMap
from src.ui.hallucination_shop import HallucinationShop
from src.world.hallucination_levels import create_hallucination_level
```

**Step 2: Add hallucination state variables near the circus ones**

```python
hallucination_map_ui = None
hallucination_shop_ui = None
current_hallucination_island = 0
current_hallucination_level  = 0
```

**Step 3: Update CircusWin portal handler**

Change the `enter_portal` handler (from Task 6 Step 5) to go to hallucination map:
```python
if result == "enter_portal":
    save_data.unlock_hallucination()
    hallucination_map_ui = HallucinationMap(save_data)
    game_state = STATE_HALLUCINATION_MAP
```

**Step 4: Add a `start_hallucination_level()` helper near `start_level()`**

```python
def start_hallucination_level():
    nonlocal platforms, enemies, particles, player, camera, boss, bg, prev_boss_state, boss_music_started, coin_manager
    coin_manager = CoinManager()
    particles = []

    platforms, enemies = create_hallucination_level(current_hallucination_island, current_hallucination_level)
    player = Player(50, 400)
    apply_powers(player, save_data)
    camera = Camera()
    bg = ParallaxBackground("shadow")  # dark bg for all hallucination levels

    # Every level in hallucination has a boss
    island_idx = current_hallucination_island
    if island_idx == 0:
        boss = WaspKing(1800, 540 - 90)
    elif island_idx == 1:
        boss = SwampBeetleLord(1800, 540 - 80)
    elif island_idx == 2:
        boss = CrystalSpiderQueen(1900, 350)
    elif island_idx == 3:
        boss = FireMoth(2000, 300)
    else:
        boss = ShadowHornet(2200, 350)

    # Hallucination bosses are stronger than circus bosses
    boss.max_hp = int(boss.max_hp * 2.0)
    boss.hp     = boss.max_hp

    prev_boss_state = "idle"
    boss_music_started = False
```

**Step 5: Handle hallucination map events**

```python
if game_state == STATE_HALLUCINATION_MAP and hallucination_map_ui:
    result = hallucination_map_ui.handle_input(event)
    if result is not None:
        if isinstance(result, tuple) and result[0] == "play":
            current_hallucination_island = result[1]
            current_hallucination_level  = 0
            start_hallucination_level()
            game_state = STATE_HALLUCINATION_PLAYING
            play_music("level_music")
        elif isinstance(result, tuple) and result[0] == "shop":
            hallucination_shop_ui = HallucinationShop(save_data, result[1])
            game_state = STATE_HALLUCINATION_SHOP

if game_state == STATE_HALLUCINATION_SHOP and hallucination_shop_ui:
    result = hallucination_shop_ui.handle_input(event)
    if result == "close":
        hallucination_map_ui = HallucinationMap(save_data)
        game_state = STATE_HALLUCINATION_MAP
```

**Step 6: Make the play loop also run for STATE_HALLUCINATION_PLAYING**

Find all `game_state == STATE_PLAYING` checks in the update and draw loops. Change to:

```python
if game_state in (STATE_PLAYING, STATE_CIRCUS_BOSS, STATE_HALLUCINATION_PLAYING):
```

**Step 7: Handle level completion in hallucination land**

In the boss death / level complete section, add:

```python
if game_state == STATE_HALLUCINATION_PLAYING and boss and not boss.alive:
    # Advance to next hallucination level
    if current_hallucination_level < 3:
        current_hallucination_level += 1
        start_hallucination_level()
    else:
        # Finished this hallucination island
        if current_hallucination_island < 4:
            save_data.hallucination_island = max(
                save_data.hallucination_island,
                current_hallucination_island + 1
            )
            save_data.save()
        hallucination_map_ui = HallucinationMap(save_data)
        game_state = STATE_HALLUCINATION_MAP
        stop_music()
```

**Step 8: Handle player death in hallucination land (use a life, or go back to map)**

In the player HP <= 0 section:

```python
if game_state == STATE_HALLUCINATION_PLAYING and player and player.hp <= 0:
    if save_data.use_hallucination_life():
        save_data.save()
        # Respawn at start of current level
        start_hallucination_level()
    else:
        # Out of lives — back to hallucination map
        hallucination_map_ui = HallucinationMap(save_data)
        game_state = STATE_HALLUCINATION_MAP
        stop_music()
```

**Step 9: Draw hallucination states**

```python
elif game_state == STATE_HALLUCINATION_MAP and hallucination_map_ui:
    hallucination_map_ui.draw(screen)
elif game_state == STATE_HALLUCINATION_SHOP and hallucination_shop_ui:
    hallucination_shop_ui.draw(screen)
```

**Step 10: Test hallucination land**

1. Temporarily set `save_data.hallucination_unlocked = True` and `save_data.hallucination_island = 0` in `__init__`
2. In game.py title → island map, manually trigger `STATE_HALLUCINATION_MAP` with a key press for testing
3. Navigate the hallucination map, enter a level, verify shadow enemies appear
4. Buy lives in the shadow shop, verify they persist in save file
5. Remove temp changes once confirmed working

**Step 11: Commit**

```bash
git add src/game.py src/ui/hallucination_map.py src/ui/hallucination_shop.py src/world/hallucination_levels.py
git commit -m "feat: wire Hallucination Land into game — map, shop, levels, lives"
```

---

### Task 12: Final polish and achievement popup

**Files:**
- Modify: `src/game.py`

**Step 1: Add an achievement popup for beating Shadow Hornet**

In game.py, add a simple popup state after beating island 4:

```python
# Near the top where state vars are defined:
achievement_popup_timer = 0
achievement_popup_text  = ""
```

Where Shadow Hornet's death is handled (island 4 boss dies), add:
```python
save_data.unlock_circus()
achievement_popup_text  = "ACHIEVEMENT UNLOCKED: THE CIRCUS IS OPEN!"
achievement_popup_timer = 240  # 4 seconds
```

In the draw section, draw the popup over everything when active:
```python
if achievement_popup_timer > 0:
    achievement_popup_timer -= 1
    alpha = min(255, achievement_popup_timer * 6)
    popup_font = pygame.font.Font(None, 28)
    popup_surf = popup_font.render(achievement_popup_text, True, (255, 220, 50))
    popup_bg = pygame.Surface((popup_surf.get_width() + 20, 40), pygame.SRCALPHA)
    popup_bg.fill((0, 0, 0, 180))
    screen.blit(popup_bg, (SCREEN_WIDTH//2 - popup_bg.get_width()//2, SCREEN_HEIGHT - 70))
    screen.blit(popup_surf, (SCREEN_WIDTH//2 - popup_surf.get_width()//2, SCREEN_HEIGHT - 60))
```

**Step 2: Final full playthrough test**

1. Start fresh (delete save_data.json)
2. Play through to island 4, beat Shadow Hornet
3. Verify achievement popup appears
4. Verify The Circus appears on island map
5. Enter Circus, fight all 5 bosses (or skip with F1 bot)
6. Verify CircusWin screen + portal → Hallucination Land
7. Play a hallucination level, verify shadow enemies, buy lives, buy a shadow power
8. Verify save file has all new fields

**Step 3: Commit**

```bash
git add src/game.py
git commit -m "feat: achievement popup on final boss kill — circus unlock"
```

---

## Done!

The full feature is:
- Beat Shadow Hornet → achievement popup + The Circus on island map
- The Circus: 5 harder bosses back-to-back, one life, portal on win
- Hallucination Land: 5 islands × 4 levels, shadow enemies, lives + shadow powers in special shop
