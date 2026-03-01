# Hornet Platformer Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Pygame platformer where a hornet fights through 3 levels and defeats the Wasp King boss.

**Architecture:** Single-file `main.py` with all game logic. Classes for Player, enemies, platforms, and camera. Game state machine handles title/playing/transitions/game-over/victory screens. Levels defined as data (lists of platform positions and enemy placements).

**Tech Stack:** Python 3, Pygame

---

### Task 1: Project Setup + Game Window

**Files:**
- Create: `main.py`
- Create: `README.md`

**Step 1: Create main.py with a basic Pygame window**

```python
import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "HORNET"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
```

**Step 2: Create README.md**

```markdown
# Hornet

A platformer where you play as a hornet fighting through 3 levels to defeat the Wasp King.

Built with Python and Pygame.

## How to Run

```
python main.py
```

## Controls

- Arrow keys or A/D: Move left/right
- Spacebar: Jump (hold to hover)
- Z or X: Attack
```

**Step 3: Run the game to verify**

Run: `python main.py`
Expected: A black 800x600 window titled "HORNET" appears. Closing it exits cleanly.

**Step 4: Commit**

```bash
git add main.py README.md
git commit -m "feat: basic Pygame window and game loop"
```

---

### Task 2: Player Movement (Left/Right + Gravity)

**Files:**
- Modify: `main.py`

**Step 1: Add a Player class with horizontal movement and gravity**

Add above `main()`:

```python
# Player constants
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 30
PLAYER_SPEED = 5
GRAVITY = 0.8
JUMP_POWER = -15
GROUND_Y = SCREEN_HEIGHT - 60  # Temporary ground line

# Colors
YELLOW = (255, 220, 50)
DARK_YELLOW = (200, 170, 0)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True

    def update(self, keys):
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
            self.facing_right = True

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Temporary ground collision
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Jump
        if (keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False

    def draw(self, screen):
        # Body (yellow rectangle)
        pygame.draw.rect(screen, YELLOW, self.rect)
        # Stinger (triangle on the front)
        if self.facing_right:
            tip_x = self.rect.right + 8
            base_top = (self.rect.right, self.rect.centery - 4)
            base_bot = (self.rect.right, self.rect.centery + 4)
        else:
            tip_x = self.rect.left - 8
            base_top = (self.rect.left, self.rect.centery - 4)
            base_bot = (self.rect.left, self.rect.centery + 4)
        tip = (tip_x, self.rect.centery)
        pygame.draw.polygon(screen, DARK_YELLOW, [tip, base_top, base_bot])
```

**Step 2: Update main() to use the Player**

In main(), after creating the clock, add:
```python
    player = Player(100, GROUND_Y - PLAYER_HEIGHT)
```

In the game loop, after event handling:
```python
        keys = pygame.key.get_pressed()
        player.update(keys)
```

Replace `screen.fill(BLACK)` section with:
```python
        screen.fill((135, 200, 235))  # Light blue sky
        # Temporary ground
        pygame.draw.rect(screen, (100, 180, 100), (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
        player.draw(screen)
```

**Step 3: Run and verify**

Run: `python main.py`
Expected: Yellow rectangle with a stinger on a green ground. Arrow keys move left/right. Spacebar jumps. Gravity pulls the hornet back down.

**Step 4: Commit**

```bash
git add main.py
git commit -m "feat: add player with movement, jump, and gravity"
```

---

### Task 3: Hover Mechanic

**Files:**
- Modify: `main.py`

**Step 1: Add hover constants and hover state to Player**

Add constants:
```python
HOVER_MAX = 60        # Frames of hover time (~1 second at 60fps)
HOVER_GRAVITY = 0.15  # Much slower fall while hovering
```

Add to Player `__init__`:
```python
        self.hover_fuel = HOVER_MAX
        self.is_hovering = False
```

**Step 2: Update Player.update() with hover logic**

Replace the gravity and jump section with:
```python
        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False

        # Hover (hold space while in the air)
        if keys[pygame.K_SPACE] and not self.on_ground and self.hover_fuel > 0 and self.vel_y > 0:
            self.is_hovering = True
            self.hover_fuel -= 1
            self.vel_y += HOVER_GRAVITY  # Slow fall
        else:
            self.is_hovering = False
            self.vel_y += GRAVITY  # Normal gravity

        self.rect.y += self.vel_y

        # Temporary ground collision
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.on_ground = True
            self.hover_fuel = HOVER_MAX  # Refill hover
        else:
            self.on_ground = False
```

**Step 3: Run and verify**

Run: `python main.py`
Expected: Jump and hold spacebar — the hornet falls much slower while hovering. After ~1 second of hovering, it falls normally again. Landing refills hover.

**Step 4: Commit**

```bash
git add main.py
git commit -m "feat: add hover mechanic with fuel meter"
```

---

### Task 4: Platforms + Collision

**Files:**
- Modify: `main.py`

**Step 1: Add a Platform class**

```python
class Platform:
    def __init__(self, x, y, width, height, color=(100, 180, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, camera_x):
        draw_rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(screen, self.color, draw_rect)
```

**Step 2: Replace temporary ground with platform list**

Remove the `GROUND_Y` constant. In `main()`, create a list of platforms:
```python
    platforms = [
        Platform(0, SCREEN_HEIGHT - 60, 2000, 60),      # Long ground
        Platform(300, 420, 150, 20),                      # Floating platform
        Platform(550, 340, 150, 20),                      # Higher platform
        Platform(800, 400, 200, 20),                      # Another platform
    ]
```

**Step 3: Update Player to collide with platforms instead of the ground**

Replace the temporary ground collision in `Player.update()`. Add a `platforms` parameter:
```python
    def update(self, keys, platforms):
```

Replace the ground collision section with:
```python
        # Platform collision (vertical)
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.hover_fuel = HOVER_MAX
                elif self.vel_y < 0:  # Jumping up into platform
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
```

**Step 4: Update draw calls in main loop**

```python
        screen.fill((135, 200, 235))
        for p in platforms:
            p.draw(screen, 0)  # camera_x=0 for now
        player.draw(screen)
```

Update the player.update call:
```python
        player.update(keys, platforms)
```

**Step 5: Run and verify**

Run: `python main.py`
Expected: Ground platform plus floating platforms. Hornet lands on platforms, can jump between them.

**Step 6: Commit**

```bash
git add main.py
git commit -m "feat: add platforms with collision detection"
```

---

### Task 5: Camera

**Files:**
- Modify: `main.py`

**Step 1: Add Camera class**

```python
class Camera:
    def __init__(self):
        self.x = 0

    def update(self, player):
        # Camera follows player, keeping them in the left third of the screen
        target_x = player.rect.centerx - SCREEN_WIDTH // 3
        self.x += (target_x - self.x) * 0.1  # Smooth follow
        if self.x < 0:
            self.x = 0
```

**Step 2: Update Player.draw() to use camera offset**

```python
    def draw(self, screen, camera_x):
        # Body
        draw_rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(screen, YELLOW, draw_rect)
        # Stinger
        if self.facing_right:
            tip_x = draw_rect.right + 8
            base_top = (draw_rect.right, draw_rect.centery - 4)
            base_bot = (draw_rect.right, draw_rect.centery + 4)
        else:
            tip_x = draw_rect.left - 8
            base_top = (draw_rect.left, draw_rect.centery - 4)
            base_bot = (draw_rect.left, draw_rect.centery + 4)
        tip = (tip_x, draw_rect.centery)
        pygame.draw.polygon(screen, DARK_YELLOW, [tip, base_top, base_bot])
```

**Step 3: Use camera in main loop**

Create camera after player:
```python
    camera = Camera()
```

In game loop:
```python
        camera.update(player)

        screen.fill((135, 200, 235))
        for p in platforms:
            p.draw(screen, camera.x)
        player.draw(screen, camera.x)
```

**Step 4: Run and verify**

Run: `python main.py`
Expected: Camera smoothly follows the hornet as it moves right. Level scrolls.

**Step 5: Commit**

```bash
git add main.py
git commit -m "feat: add smooth horizontal camera follow"
```

---

### Task 6: Stinger Attack

**Files:**
- Modify: `main.py`

**Step 1: Add attack constants and state to Player**

Add constants:
```python
ATTACK_RANGE = 50
ATTACK_WIDTH = 10
ATTACK_DURATION = 10   # Frames the attack hitbox is active
ATTACK_COOLDOWN = 20   # Frames before you can attack again
```

Add to Player `__init__`:
```python
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.attack_rect = None
```

**Step 2: Add attack logic to Player.update()**

At the end of update(), add:
```python
        # Attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Attack
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
                self.attack_rect = None

    def start_attack(self):
        if self.attack_cooldown <= 0 and not self.attacking:
            self.attacking = True
            self.attack_timer = ATTACK_DURATION
            self.attack_cooldown = ATTACK_COOLDOWN
            # Create hitbox in front of player
            if self.facing_right:
                self.attack_rect = pygame.Rect(
                    self.rect.right, self.rect.top - 5,
                    ATTACK_RANGE, self.rect.height + 10
                )
            else:
                self.attack_rect = pygame.Rect(
                    self.rect.left - ATTACK_RANGE, self.rect.top - 5,
                    ATTACK_RANGE, self.rect.height + 10
                )
```

**Step 3: Update Player.draw() to show attack**

Add after drawing the stinger:
```python
        # Attack visual
        if self.attacking and self.attack_rect:
            atk_draw = self.attack_rect.move(-camera_x, 0)
            attack_surface = pygame.Surface((atk_draw.width, atk_draw.height), pygame.SRCALPHA)
            attack_surface.fill((255, 255, 200, 120))  # Semi-transparent yellow
            screen.blit(attack_surface, atk_draw)
```

**Step 4: Handle attack input in main loop**

In the event loop, add:
```python
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_z, pygame.K_x):
                    player.start_attack()
```

**Step 5: Run and verify**

Run: `python main.py`
Expected: Press Z or X — a yellow flash appears in front of the hornet briefly. Can't spam it (cooldown works).

**Step 6: Commit**

```bash
git add main.py
git commit -m "feat: add stinger melee attack with cooldown"
```

---

### Task 7: HUD (Health Bar + Hover Meter)

**Files:**
- Modify: `main.py`

**Step 1: Add health to Player**

Add constants:
```python
PLAYER_MAX_HP = 5
INVINCIBILITY_FRAMES = 60  # 1 second of invincibility after hit
```

Add to Player `__init__`:
```python
        self.hp = PLAYER_MAX_HP
        self.invincible_timer = 0
```

Add to Player `update()`:
```python
        # Invincibility timer
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
```

**Step 2: Add take_damage method to Player**

```python
    def take_damage(self, amount):
        if self.invincible_timer <= 0:
            self.hp -= amount
            self.invincible_timer = INVINCIBILITY_FRAMES
            return True
        return False
```

**Step 3: Add flashing effect when invincible**

In Player.draw(), wrap the drawing code so it flashes:
```python
    def draw(self, screen, camera_x):
        # Flash when invincible (skip drawing every other frame)
        if self.invincible_timer > 0 and self.invincible_timer % 4 < 2:
            return
        # ... rest of draw code
```

**Step 4: Add HUD drawing function**

```python
def draw_hud(screen, player, level_name):
    # Health bar background
    pygame.draw.rect(screen, (80, 80, 80), (10, 10, 104, 16))
    # Health bar fill
    hp_width = int(100 * player.hp / PLAYER_MAX_HP)
    color = (50, 200, 50) if player.hp > 2 else (200, 50, 50)
    pygame.draw.rect(screen, color, (12, 12, hp_width, 12))

    # Hover meter background
    pygame.draw.rect(screen, (80, 80, 80), (10, 32, 104, 10))
    # Hover meter fill
    hover_width = int(100 * player.hover_fuel / HOVER_MAX)
    pygame.draw.rect(screen, (100, 180, 255), (12, 34, hover_width, 6))

    # Level name
    font = pygame.font.Font(None, 28)
    text = font.render(level_name, True, WHITE)
    screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, 10))
```

**Step 5: Call draw_hud in main loop**

After drawing player:
```python
        draw_hud(screen, player, "Level 1: The Garden")
```

**Step 6: Run and verify**

Run: `python main.py`
Expected: Green health bar top-left, blue hover meter below it, level name top-right. Hover meter drains while hovering and refills on landing.

**Step 7: Commit**

```bash
git add main.py
git commit -m "feat: add HUD with health bar, hover meter, level name"
```

---

### Task 8: Beetle Enemy

**Files:**
- Modify: `main.py`

**Step 1: Add Enemy base class and Beetle**

```python
RED = (200, 50, 50)

class Enemy:
    def __init__(self, x, y, width, height, hp, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.hp = hp
        self.color = color
        self.alive = True
        self.death_timer = 0  # Flash timer when killed

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            self.death_timer = 15  # Brief flash before disappearing

    def draw(self, screen, camera_x):
        if not self.alive:
            if self.death_timer > 0:
                # Flash white when dying
                draw_rect = self.rect.move(-camera_x, 0)
                pygame.draw.rect(screen, WHITE, draw_rect)
            return
        draw_rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(screen, self.color, draw_rect)

class Beetle(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__(x, y, 36, 24, 2, RED)
        self.speed = 1.5
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.moving_right = True

    def update(self):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        if self.moving_right:
            self.rect.x += self.speed
            if self.rect.right >= self.patrol_right:
                self.moving_right = False
        else:
            self.rect.x -= self.speed
            if self.rect.left <= self.patrol_left:
                self.moving_right = True
```

**Step 2: Add beetles to the test level in main()**

```python
    enemies = [
        Beetle(400, SCREEN_HEIGHT - 60 - 24, 350, 550),
        Beetle(700, SCREEN_HEIGHT - 60 - 24, 650, 900),
    ]
```

**Step 3: Update and draw enemies in game loop**

```python
        for enemy in enemies:
            enemy.update()
            enemy.draw(screen, camera.x)
```

**Step 4: Run and verify**

Run: `python main.py`
Expected: Red rectangles patrol back and forth on the ground. They don't interact with the player yet (that's next task).

**Step 5: Commit**

```bash
git add main.py
git commit -m "feat: add beetle enemy with patrol behavior"
```

---

### Task 9: Combat System (Damage + Knockback)

**Files:**
- Modify: `main.py`

**Step 1: Add combat collision checking function**

```python
def handle_combat(player, enemies):
    # Player attack hits enemies
    if player.attacking and player.attack_rect:
        for enemy in enemies:
            if enemy.alive and player.attack_rect.colliderect(enemy.rect):
                enemy.take_damage(1)

    # Enemies damage player on contact
    for enemy in enemies:
        if enemy.alive and player.rect.colliderect(enemy.rect):
            if player.take_damage(1):
                # Knockback: push player away from enemy
                if player.rect.centerx < enemy.rect.centerx:
                    player.rect.x -= 30
                else:
                    player.rect.x += 30
                player.vel_y = -8  # Small bounce up
```

**Step 2: Call handle_combat in game loop**

After updating player and enemies:
```python
        handle_combat(player, enemies)
```

**Step 3: Run and verify**

Run: `python main.py`
Expected: Walking into a beetle damages the hornet (health bar drops, hornet flashes and gets knocked back). Pressing Z/X near a beetle damages it. Beetles take 2 hits to die and flash white when killed.

**Step 4: Commit**

```bash
git add main.py
git commit -m "feat: add combat system with damage and knockback"
```

---

### Task 10: Game States (Title, Game Over, Victory)

**Files:**
- Modify: `main.py`

**Step 1: Add game state constants and state machine**

```python
# Game states
STATE_TITLE = "title"
STATE_PLAYING = "playing"
STATE_LEVEL_TRANSITION = "transition"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"
```

**Step 2: Add screen drawing functions**

```python
def draw_title_screen(screen):
    screen.fill(BLACK)
    font_big = pygame.font.Font(None, 80)
    font_small = pygame.font.Font(None, 36)
    title = font_big.render("HORNET", True, YELLOW)
    prompt = font_small.render("Press ENTER to start", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 350))

def draw_game_over(screen):
    screen.fill(BLACK)
    font_big = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 36)
    title = font_big.render("GAME OVER", True, RED)
    prompt = font_small.render("Press ENTER to retry", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 220))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 330))

def draw_transition(screen, level_name):
    screen.fill(BLACK)
    font_big = pygame.font.Font(None, 56)
    font_small = pygame.font.Font(None, 36)
    title = font_big.render(level_name, True, WHITE)
    prompt = font_small.render("Press ENTER to continue", True, (180, 180, 180))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 240))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 330))

def draw_victory(screen):
    screen.fill(BLACK)
    font_big = pygame.font.Font(None, 56)
    font_small = pygame.font.Font(None, 36)
    title = font_big.render("You defeated the Wasp King!", True, YELLOW)
    prompt = font_small.render("Press ENTER to play again", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 240))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 330))
```

**Step 3: Restructure main() with game states**

Restructure the main loop to use a `game_state` variable. Handle state transitions: ENTER on title starts playing, hp <= 0 goes to game over, ENTER on game over restarts, etc.

The game loop becomes:
```python
    game_state = STATE_TITLE
    current_level = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_state == STATE_TITLE:
                        game_state = STATE_PLAYING
                        # Reset player and load level
                    elif game_state == STATE_GAME_OVER:
                        game_state = STATE_PLAYING
                        # Reset player, reload current level
                    elif game_state == STATE_LEVEL_TRANSITION:
                        game_state = STATE_PLAYING
                        # Load next level
                    elif game_state == STATE_VICTORY:
                        game_state = STATE_TITLE
                if event.key in (pygame.K_z, pygame.K_x) and game_state == STATE_PLAYING:
                    player.start_attack()

        if game_state == STATE_PLAYING:
            keys = pygame.key.get_pressed()
            player.update(keys, platforms)
            for enemy in enemies:
                enemy.update()
            handle_combat(player, enemies)
            camera.update(player)

            if player.hp <= 0:
                game_state = STATE_GAME_OVER

        # Draw based on state
        if game_state == STATE_TITLE:
            draw_title_screen(screen)
        elif game_state == STATE_PLAYING:
            screen.fill((135, 200, 235))
            for p in platforms:
                p.draw(screen, camera.x)
            for enemy in enemies:
                enemy.draw(screen, camera.x)
            player.draw(screen, camera.x)
            draw_hud(screen, player, level_names[current_level])
        elif game_state == STATE_GAME_OVER:
            draw_game_over(screen)
        elif game_state == STATE_LEVEL_TRANSITION:
            draw_transition(screen, level_names[current_level])
        elif game_state == STATE_VICTORY:
            draw_victory(screen)

        pygame.display.flip()
        clock.tick(FPS)
```

**Step 4: Run and verify**

Run: `python main.py`
Expected: Title screen appears. Press ENTER to start playing. Die = game over screen. ENTER restarts.

**Step 5: Commit**

```bash
git add main.py
git commit -m "feat: add game states (title, playing, game over, victory)"
```

---

### Task 11: Level Data System

**Files:**
- Modify: `main.py`

**Step 1: Create level data definitions**

```python
# Level color themes
LEVEL_THEMES = [
    {"bg": (135, 200, 235), "platform": (100, 180, 100), "name": "Level 1: The Garden"},
    {"bg": (180, 160, 80),  "platform": (160, 120, 60),  "name": "Level 2: The Hive"},
    {"bg": (100, 40, 40),   "platform": (80, 80, 80),    "name": "Level 3: The Throne Room"},
]

def create_level(level_num):
    """Return (platforms, enemies) for the given level number (0-indexed)."""
    theme = LEVEL_THEMES[level_num]
    color = theme["platform"]

    if level_num == 0:  # The Garden
        platforms = [
            Platform(0, 540, 600, 60, color),
            Platform(250, 440, 150, 20, color),
            Platform(500, 380, 200, 20, color),
            Platform(750, 540, 400, 60, color),
            Platform(900, 440, 150, 20, color),
            Platform(1200, 540, 600, 60, color),
            Platform(1400, 420, 150, 20, color),
            Platform(1700, 540, 400, 60, color),
            # End platform
            Platform(2000, 540, 200, 60, color),
        ]
        enemies = [
            Beetle(300, 540 - 24, 250, 500),
            Beetle(800, 540 - 24, 750, 1050),
            Beetle(1300, 540 - 24, 1200, 1500),
            Beetle(1750, 540 - 24, 1700, 1950),
        ]
    elif level_num == 1:  # The Hive
        platforms = [
            Platform(0, 540, 300, 60, color),
            Platform(200, 420, 120, 20, color),
            Platform(400, 340, 120, 20, color),
            Platform(550, 450, 150, 20, color),
            Platform(750, 540, 200, 60, color),
            Platform(850, 380, 120, 20, color),
            Platform(1050, 300, 150, 20, color),
            Platform(1250, 420, 120, 20, color),
            Platform(1400, 540, 300, 60, color),
            Platform(1600, 380, 150, 20, color),
            Platform(1850, 540, 400, 60, color),
        ]
        enemies = [
            Beetle(100, 540 - 24, 50, 250),
            Beetle(800, 540 - 24, 750, 900),
            Fly(450, 280, 400, 600),
            Fly(900, 320, 850, 1100),
            Fly(1650, 320, 1600, 1850),
            Beetle(1500, 540 - 24, 1400, 1650),
        ]
    elif level_num == 2:  # The Throne Room
        platforms = [
            Platform(0, 540, 300, 60, color),
            Platform(200, 420, 100, 20, color),
            Platform(400, 350, 80, 20, color),
            Platform(550, 440, 100, 20, color),
            Platform(700, 540, 150, 60, color),
            Platform(900, 380, 100, 20, color),
            Platform(1050, 300, 100, 20, color),
            Platform(1200, 420, 80, 20, color),
            Platform(1350, 540, 200, 60, color),
            Platform(1500, 400, 100, 20, color),
            # Boss arena — flat wide platform
            Platform(1700, 540, 800, 60, color),
        ]
        enemies = [
            Beetle(100, 540 - 24, 50, 250),
            Spider(450, 350 - 28, 400, 530),
            Fly(600, 380, 550, 750),
            Beetle(750, 540 - 24, 700, 830),
            Spider(950, 380 - 28, 900, 1050),
            Fly(1100, 250, 1050, 1250),
            Beetle(1400, 540 - 24, 1350, 1530),
        ]

    return platforms, enemies
```

**Step 2: Add a `load_level` helper in main() and use it**

```python
def load_level(level_num):
    platforms, enemies = create_level(level_num)
    player = Player(50, 400)
    player.hp = PLAYER_MAX_HP
    camera = Camera()
    return platforms, enemies, player, camera
```

Update state transitions to use `load_level()`. When all enemies are dead and the player reaches the end platform, transition to next level (or boss fight for level 3).

**Step 3: Add level completion detection**

```python
def check_level_complete(player, enemies, level_num):
    """Check if all enemies are dead and player reached end of level."""
    all_dead = all(not e.alive and e.death_timer <= 0 for e in enemies)
    # Player past end threshold
    if level_num == 0:
        past_end = player.rect.x > 2000
    elif level_num == 1:
        past_end = player.rect.x > 1900
    elif level_num == 2:
        past_end = player.rect.x > 1700  # Reached boss arena
    else:
        past_end = False
    return all_dead and past_end
```

**Step 4: Run and verify**

Run: `python main.py`
Expected: Level 1 loads with garden theme. Killing all beetles and reaching the end triggers transition to Level 2 with different colors and enemies.

**Step 5: Commit**

```bash
git add main.py
git commit -m "feat: add level data system with 3 levels and transitions"
```

---

### Task 12: Fly Enemy

**Files:**
- Modify: `main.py`

**Step 1: Add Fly class**

```python
import math

GREEN = (50, 200, 50)

class Fly(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__(x, y, 24, 20, 1, GREEN)
        self.base_y = y
        self.speed = 2.5
        self.wave_offset = 0
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.moving_right = True

    def update(self):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        # Horizontal patrol
        if self.moving_right:
            self.rect.x += self.speed
            if self.rect.right >= self.patrol_right:
                self.moving_right = False
        else:
            self.rect.x -= self.speed
            if self.rect.left <= self.patrol_left:
                self.moving_right = True

        # Sine wave vertical movement
        self.wave_offset += 0.05
        self.rect.y = self.base_y + int(math.sin(self.wave_offset) * 30)
```

**Step 2: Run and verify**

Run: `python main.py`
Expected: Green rectangles float in a wavy pattern through the air. They die in 1 hit.

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: add fly enemy with sine-wave movement"
```

---

### Task 13: Spider Enemy

**Files:**
- Modify: `main.py`

**Step 1: Add Spider class**

```python
PURPLE = (150, 50, 200)

class Spider(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__(x, y, 28, 28, 1, PURPLE)
        self.home_x = x
        self.speed = 6
        self.lunge_range = 150  # How close player must be to trigger lunge
        self.lunging = False
        self.lunge_target_x = 0
        self.returning = False
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right

    def update(self, player_x=None):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        if self.lunging:
            # Move toward lunge target
            if self.rect.centerx < self.lunge_target_x:
                self.rect.x += self.speed
                if self.rect.centerx >= self.lunge_target_x:
                    self.lunging = False
                    self.returning = True
            else:
                self.rect.x -= self.speed
                if self.rect.centerx <= self.lunge_target_x:
                    self.lunging = False
                    self.returning = True
        elif self.returning:
            # Return to home position
            if abs(self.rect.x - self.home_x) < 3:
                self.rect.x = self.home_x
                self.returning = False
            elif self.rect.x < self.home_x:
                self.rect.x += self.speed * 0.5
            else:
                self.rect.x -= self.speed * 0.5
        elif player_x is not None:
            # Check if player is close enough to lunge
            dist = abs(self.rect.centerx - player_x)
            if dist < self.lunge_range:
                self.lunging = True
                self.lunge_target_x = player_x
```

**Step 2: Update enemy update calls to pass player position for spiders**

In the game loop, change:
```python
        for enemy in enemies:
            if isinstance(enemy, Spider):
                enemy.update(player.rect.centerx)
            else:
                enemy.update()
```

**Step 3: Run and verify**

Run: `python main.py`
Expected: Purple rectangles sit still, then lunge quickly when the hornet gets close, then return home. Die in 1 hit.

**Step 4: Commit**

```bash
git add main.py
git commit -m "feat: add spider enemy with lunge attack"
```

---

### Task 14: Boss — The Wasp King

**Files:**
- Modify: `main.py`

**Step 1: Add Boss class**

```python
ORANGE = (230, 150, 30)

class WaspKing:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 120, 90)  # 3x player size
        self.hp = 10
        self.max_hp = 10
        self.color = ORANGE
        self.alive = True
        self.vel_y = 0

        # Attack pattern state
        self.state = "idle"  # idle, charging, slamming, summoning
        self.state_timer = 0
        self.pattern_index = 0
        self.patterns = ["charge", "slam", "summon"]
        self.idle_time = 60  # Frames between attacks
        self.speed_multiplier = 1.0

        # Charge
        self.charge_speed = 8
        self.charge_target_x = 0

        # Slam
        self.slam_start_y = 0
        self.shockwave = None
        self.shockwave_timer = 0

        # Summon
        self.summoned_flies = []

    def take_damage(self, amount):
        self.hp -= amount
        # Get faster as health drops
        self.speed_multiplier = 1.0 + (1.0 - self.hp / self.max_hp) * 0.8
        if self.hp <= 0:
            self.alive = False

    def update(self, player, arena_platforms):
        if not self.alive:
            return

        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        for p in arena_platforms:
            if self.rect.colliderect(p.rect) and self.vel_y > 0:
                self.rect.bottom = p.rect.top
                self.vel_y = 0

        # Shockwave timer
        if self.shockwave and self.shockwave_timer > 0:
            self.shockwave_timer -= 1
            self.shockwave.width += 10  # Expand shockwave
        else:
            self.shockwave = None

        if self.state == "idle":
            self.state_timer -= 1
            if self.state_timer <= 0:
                # Pick next attack
                self.state = self.patterns[self.pattern_index]
                self.pattern_index = (self.pattern_index + 1) % len(self.patterns)
                self._start_attack(player)

        elif self.state == "charge":
            # Rush at the player
            speed = self.charge_speed * self.speed_multiplier
            if self.rect.centerx < self.charge_target_x:
                self.rect.x += speed
            else:
                self.rect.x -= speed
            self.state_timer -= 1
            if self.state_timer <= 0 or abs(self.rect.centerx - self.charge_target_x) < 10:
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)

        elif self.state == "slam":
            if self.state_timer > 30:
                # Rising up
                self.rect.y -= 5
                self.state_timer -= 1
            elif self.state_timer > 0:
                # Slamming down
                self.vel_y = 15
                self.state_timer -= 1
                # Check if landed
                if self.vel_y == 0 and self.rect.bottom >= self.slam_start_y:
                    # Create shockwave
                    self.shockwave = pygame.Rect(
                        self.rect.x - 50, self.rect.bottom - 10,
                        self.rect.width + 100, 15
                    )
                    self.shockwave_timer = 20
                    self.state = "idle"
                    self.state_timer = int(self.idle_time / self.speed_multiplier)

        elif self.state == "summon":
            self.state_timer -= 1
            if self.state_timer <= 0:
                # Spawn 2 flies
                self.summoned_flies = [
                    Fly(self.rect.x - 50, self.rect.y - 30,
                        self.rect.x - 200, self.rect.x + 200),
                    Fly(self.rect.right + 50, self.rect.y - 30,
                        self.rect.x - 200, self.rect.x + 200),
                ]
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)

    def _start_attack(self, player):
        if self.state == "charge":
            self.charge_target_x = player.rect.centerx
            self.state_timer = 60
        elif self.state == "slam":
            self.slam_start_y = self.rect.bottom
            self.state_timer = 50
        elif self.state == "summon":
            self.state_timer = 30

    def draw(self, screen, camera_x):
        if not self.alive:
            return
        draw_rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(screen, self.color, draw_rect)
        # Eyes
        eye_y = draw_rect.top + 20
        pygame.draw.circle(screen, RED, (draw_rect.left + 30, eye_y), 8)
        pygame.draw.circle(screen, RED, (draw_rect.right - 30, eye_y), 8)
        # Shockwave
        if self.shockwave and self.shockwave_timer > 0:
            sw = self.shockwave.move(-camera_x, 0)
            wave_surface = pygame.Surface((sw.width, sw.height), pygame.SRCALPHA)
            wave_surface.fill((255, 100, 50, 150))
            screen.blit(wave_surface, sw)

def draw_boss_hp(screen, boss):
    """Draw boss health bar at top center of screen."""
    bar_width = 300
    bar_x = SCREEN_WIDTH // 2 - bar_width // 2
    pygame.draw.rect(screen, (80, 80, 80), (bar_x - 2, 10, bar_width + 4, 22))
    hp_width = int(bar_width * boss.hp / boss.max_hp)
    pygame.draw.rect(screen, ORANGE, (bar_x, 12, hp_width, 18))
    font = pygame.font.Font(None, 24)
    label = font.render("WASP KING", True, WHITE)
    screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 36))
```

**Step 2: Integrate boss into Level 3**

In `create_level` for level 2 (index 2), the boss spawns in the arena area (x=1800). Modify the game state to handle the boss fight:
- When player reaches the boss arena in Level 3, spawn the boss
- Boss fight is still `STATE_PLAYING` but with boss active
- Boss defeat triggers `STATE_VICTORY`

Add boss combat to `handle_combat`:
```python
def handle_combat(player, enemies, boss=None):
    # ... existing enemy combat ...

    # Boss combat
    if boss and boss.alive:
        # Player attack hits boss
        if player.attacking and player.attack_rect:
            if player.attack_rect.colliderect(boss.rect):
                boss.take_damage(1)

        # Boss body damages player
        if player.rect.colliderect(boss.rect):
            if player.take_damage(1):
                if player.rect.centerx < boss.rect.centerx:
                    player.rect.x -= 40
                else:
                    player.rect.x += 40
                player.vel_y = -10

        # Boss shockwave damages player
        if boss.shockwave and boss.shockwave_timer > 0:
            if player.rect.colliderect(boss.shockwave):
                if player.take_damage(1):
                    player.vel_y = -12
```

**Step 3: Run and verify**

Run: `python main.py`
Expected: Reach Level 3 boss arena, Wasp King appears. He cycles through charge/slam/summon attacks, gets faster as he takes damage. Defeat him = victory screen.

**Step 4: Commit**

```bash
git add main.py
git commit -m "feat: add Wasp King boss with charge, slam, summon attacks"
```

---

### Task 15: Final Polish + Player Fall Death

**Files:**
- Modify: `main.py`

**Step 1: Add fall death**

In Player.update(), after platform collision:
```python
        # Fall off screen = lose a life
        if self.rect.top > SCREEN_HEIGHT + 50:
            self.hp = 0
```

**Step 2: Prevent player from moving left off screen**

In Player.update():
```python
        # Don't go left off screen start
        if self.rect.left < 0:
            self.rect.left = 0
```

**Step 3: Run full playthrough**

Run: `python main.py`
Expected: Complete game works — title screen, 3 levels with increasing difficulty, boss fight, victory. Falling off screen kills you. Full game loop is playable.

**Step 4: Commit**

```bash
git add main.py
git commit -m "feat: add fall death and screen boundary, game complete"
```

---

## Summary

| Task | What it adds | Depends on |
|------|-------------|------------|
| 1 | Window + game loop | — |
| 2 | Player movement + jump | 1 |
| 3 | Hover mechanic | 2 |
| 4 | Platforms + collision | 2 |
| 5 | Camera | 4 |
| 6 | Stinger attack | 2 |
| 7 | HUD | 3, 6 |
| 8 | Beetle enemy | 4, 5 |
| 9 | Combat system | 6, 7, 8 |
| 10 | Game states | 9 |
| 11 | Level data system | 10 |
| 12 | Fly enemy | 8 |
| 13 | Spider enemy | 8 |
| 14 | Boss | 11, 12, 13 |
| 15 | Polish + fall death | 14 |

Each task builds on the last. After every task you can run the game and see your progress!
