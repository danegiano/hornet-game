import pygame
import os
import sys
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "HORNET"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game states
STATE_TITLE = "title"
STATE_PLAYING = "playing"
STATE_LEVEL_TRANSITION = "transition"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"

LEVEL_THEMES = [
    {"bg": (135, 200, 235), "platform": (100, 180, 100), "name": "Level 1: The Garden"},
    {"bg": (180, 160, 80),  "platform": (160, 120, 60),  "name": "Level 2: The Hive"},
    {"bg": (100, 40, 40),   "platform": (80, 80, 80),    "name": "Level 3: The Throne Room"},
]

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

YELLOW = (255, 220, 50)
DARK_YELLOW = (200, 170, 0)
ORANGE = (230, 150, 30)


class Player:
    def __init__(self, x, y):
        # Load player sprites once
        self.sprite_scale = 2  # draw sprite bigger on screen
        self.spr_idle0 = pygame.image.load(os.path.join("sprites", "hornet_idle_0.png")).convert_alpha()
        self.spr_idle1 = pygame.image.load(os.path.join("sprites", "hornet_idle_1.png")).convert_alpha()
        self.spr_attack0 = pygame.image.load(os.path.join("sprites", "hornet_attack_0.png")).convert_alpha()
        self.spr_run0 = pygame.image.load(os.path.join("sprites", "hornet_run_0.png")).convert_alpha()
        self.spr_run1 = pygame.image.load(os.path.join("sprites", "hornet_run_1.png")).convert_alpha()
        self.spr_idle0_flip = pygame.transform.flip(self.spr_idle0, True, False)
        self.spr_idle1_flip = pygame.transform.flip(self.spr_idle1, True, False)
        self.spr_attack0_flip = pygame.transform.flip(self.spr_attack0, True, False)
        self.spr_run0_flip = pygame.transform.flip(self.spr_run0, True, False)
        self.spr_run1_flip = pygame.transform.flip(self.spr_run1, True, False)
        self.spr_idle0 = pygame.transform.scale(self.spr_idle0, (self.spr_idle0.get_width()*self.sprite_scale, self.spr_idle0.get_height()*self.sprite_scale))
        self.spr_idle1 = pygame.transform.scale(self.spr_idle1, (self.spr_idle1.get_width()*self.sprite_scale, self.spr_idle1.get_height()*self.sprite_scale))
        self.spr_attack0 = pygame.transform.scale(self.spr_attack0, (self.spr_attack0.get_width()*self.sprite_scale, self.spr_attack0.get_height()*self.sprite_scale))
        self.spr_run0 = pygame.transform.scale(self.spr_run0, (self.spr_run0.get_width()*self.sprite_scale, self.spr_run0.get_height()*self.sprite_scale))
        self.spr_run1 = pygame.transform.scale(self.spr_run1, (self.spr_run1.get_width()*self.sprite_scale, self.spr_run1.get_height()*self.sprite_scale))
        self.spr_idle0_flip = pygame.transform.scale(self.spr_idle0_flip, (self.spr_idle0_flip.get_width()*self.sprite_scale, self.spr_idle0_flip.get_height()*self.sprite_scale))
        self.spr_idle1_flip = pygame.transform.scale(self.spr_idle1_flip, (self.spr_idle1_flip.get_width()*self.sprite_scale, self.spr_idle1_flip.get_height()*self.sprite_scale))
        self.spr_attack0_flip = pygame.transform.scale(self.spr_attack0_flip, (self.spr_attack0_flip.get_width()*self.sprite_scale, self.spr_attack0_flip.get_height()*self.sprite_scale))
        self.spr_run0_flip = pygame.transform.scale(self.spr_run0_flip, (self.spr_run0_flip.get_width()*self.sprite_scale, self.spr_run0_flip.get_height()*self.sprite_scale))
        self.spr_run1_flip = pygame.transform.scale(self.spr_run1_flip, (self.spr_run1_flip.get_width()*self.sprite_scale, self.spr_run1_flip.get_height()*self.sprite_scale))
        self.anim_timer = 0
        self.anim_frame = 0
        self.anim_mode = "idle"

        # rect is the rectangle that represents the player's body
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        # vel_y is vertical velocity — positive = falling, negative = rising
        self.vel_y = 0
        # on_ground tracks whether the player is standing on the ground
        self.on_ground = False
        # facing_right tracks which way the player is looking
        self.facing_right = True
        # hover_fuel is how many frames of hover the player has left
        self.hover_fuel = HOVER_MAX
        # is_hovering is True while the player is actively slowing their fall
        self.is_hovering = False
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.attack_rect = None
        self.hp = PLAYER_MAX_HP
        self.invincible_timer = 0
        self.just_jumped = False

    def update(self, keys, platforms):
        # Invincibility timer
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        # --- Horizontal movement ---
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
            self.facing_right = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
            self.facing_right = False

        # Advance run animation when moving on ground
        moving = (keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_a])

        # Set animation mode
        if self.attacking:
            self.anim_mode = "attack"
        elif moving and self.on_ground:
            self.anim_mode = "run"
        else:
            self.anim_mode = "idle"

        if self.anim_mode == "run":
            self.anim_timer += 1
            if self.anim_timer >= 8:
                self.anim_timer = 0
                self.anim_frame = 1 - self.anim_frame
        elif self.anim_mode == "idle":
            self.anim_timer += 1
            if self.anim_timer >= 20:
                self.anim_timer = 0
                self.anim_frame = 1 - self.anim_frame
        else:
            self.anim_timer = 0
            self.anim_frame = 0

        # Don't go left off screen start
        if self.rect.left < 0:
            self.rect.left = 0

        # --- Jump ---
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_POWER  # A negative value shoots the player upward
            self.on_ground = False
            self.just_jumped = True
        else:
            self.just_jumped = False

        # --- Hover (hold space while in the air) ---
        # All four conditions must be true to hover:
        #   1. Holding space
        #   2. Not on the ground (in the air)
        #   3. Have hover fuel left
        #   4. Falling (vel_y > 0) — hover doesn't activate on the way up
        if keys[pygame.K_SPACE] and not self.on_ground and self.hover_fuel > 0 and self.vel_y > 0:
            self.is_hovering = True
            self.hover_fuel -= 1         # Drain 1 frame of fuel
            self.vel_y += HOVER_GRAVITY  # Slow fall instead of normal gravity
        else:
            self.is_hovering = False
            self.vel_y += GRAVITY        # Normal gravity applies

        self.rect.y += self.vel_y

        # --- Platform collision (vertical) ---
        # Reset on_ground each frame — we'll set it back to True if we land
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down onto the platform
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.hover_fuel = HOVER_MAX  # Refill hover fuel on landing
                elif self.vel_y < 0:  # Jumping up into the bottom of a platform
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Fall off screen = die
        if self.rect.top > SCREEN_HEIGHT + 50:
            self.hp = 0

        # Attack cooldown — counts down every frame until you can attack again
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Attack timer — counts down while the hitbox is active
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
                self.attack_rect = None

        # Keep the attack hitbox glued to the player while attacking
        if self.attacking and self.attack_rect:
            if self.facing_right:
                self.attack_rect.x = self.rect.right
                self.attack_rect.y = self.rect.top - 5
            else:
                self.attack_rect.x = self.rect.left - ATTACK_RANGE
                self.attack_rect.y = self.rect.top - 5

    def take_damage(self, amount):
        if self.invincible_timer <= 0:
            self.hp -= amount
            self.invincible_timer = INVINCIBILITY_FRAMES
            return True
        return False

    def start_attack(self):
        # Only start a new attack if we're not already attacking and cooldown is done
        if self.attack_cooldown <= 0 and not self.attacking:
            self.attacking = True
            self.attack_timer = ATTACK_DURATION
            self.attack_cooldown = ATTACK_COOLDOWN
            # Create a hitbox rectangle in front of the player
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

    def draw(self, screen, camera_x):
        # Flash when invincible (skip drawing every other frame)
        if self.invincible_timer > 0 and self.invincible_timer % 4 < 2:
            return

        # Shift the player's draw position left by camera_x so it moves with the world
        draw_rect = self.rect.move(-camera_x, 0)
        # Draw animated sprite
        if self.anim_mode == "attack":
            spr = self.spr_attack0 if self.facing_right else self.spr_attack0_flip
        elif self.anim_mode == "run":
            if self.anim_frame == 0:
                spr = self.spr_run0 if self.facing_right else self.spr_run0_flip
            else:
                spr = self.spr_run1 if self.facing_right else self.spr_run1_flip
        else:
            if self.anim_frame == 0:
                spr = self.spr_idle0 if self.facing_right else self.spr_idle0_flip
            else:
                spr = self.spr_idle1 if self.facing_right else self.spr_idle1_flip
        spr_x = draw_rect.centerx - spr.get_width() // 2
        spr_y = draw_rect.centery - spr.get_height() // 2
        screen.blit(spr, (spr_x, spr_y))


        # --- Stinger triangle ---
        # The stinger pokes out from the front of the hornet
        # It's a small triangle made of 3 points (a polygon)
        # We use draw_rect positions (not self.rect) so the stinger scrolls too

        if self.facing_right:
            # Stinger points to the right
            tip_x = draw_rect.right + 8
            base_top = (draw_rect.right, draw_rect.centery - 4)
            base_bot = (draw_rect.right, draw_rect.centery + 4)
        else:
            # Stinger points to the left
            tip_x = draw_rect.left - 8
            base_top = (draw_rect.left, draw_rect.centery - 4)
            base_bot = (draw_rect.left, draw_rect.centery + 4)

        tip = (tip_x, draw_rect.centery)
        pygame.draw.polygon(screen, DARK_YELLOW, [tip, base_top, base_bot])

        # --- Attack visual ---
        # When attacking, show a semi-transparent yellow flash where the hitbox is
        if self.attacking and self.attack_rect:
            atk_draw = self.attack_rect.move(-camera_x, 0)
            # SRCALPHA means the surface supports transparency
            attack_surface = pygame.Surface((atk_draw.width, atk_draw.height), pygame.SRCALPHA)
            attack_surface.fill((255, 255, 200, 120))  # Semi-transparent yellow
            screen.blit(attack_surface, atk_draw)


class Camera:
    def __init__(self):
        self.x = 0

    def update(self, player):
        # Camera follows player, keeping them in the left third of the screen
        target_x = player.rect.centerx - SCREEN_WIDTH // 3
        self.x += (target_x - self.x) * 0.1  # Smooth follow (lerp)
        if self.x < 0:
            self.x = 0  # Don't scroll left past the start of the world


class Platform:
    def __init__(self, x, y, width, height, color=(100, 180, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, camera_x):
        # Shift the platform left by camera_x so it scrolls with the world
        draw_rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(screen, self.color, draw_rect)


RED = (200, 50, 50)
GREEN = (50, 200, 50)
PURPLE = (150, 50, 200)

# Wasp (yellow) sprite colors
WASP_YELLOW = (255, 220, 50)
WASP_YELLOW_DARK = (200, 170, 0)

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

class Wasp(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__(x, y, 36, 24, 2, WASP_YELLOW)
        self.speed = 2.2
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.moving_right = True

        # Load wasp sprites
        self.scale = 2
        self.spr0 = pygame.image.load(os.path.join("sprites", "wasp_yellow_0.png")).convert_alpha()
        self.spr1 = pygame.image.load(os.path.join("sprites", "wasp_yellow_1.png")).convert_alpha()
        self.spr0 = pygame.transform.scale(self.spr0, (self.spr0.get_width()*self.scale, self.spr0.get_height()*self.scale))
        self.spr1 = pygame.transform.scale(self.spr1, (self.spr1.get_width()*self.scale, self.spr1.get_height()*self.scale))
        self.spr0_flip = pygame.transform.flip(self.spr0, True, False)
        self.spr1_flip = pygame.transform.flip(self.spr1, True, False)

        self.anim_t = 0
        self.anim_f = 0

    def update(self):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        # Flap animation
        self.anim_t += 1
        if self.anim_t >= 10:
            self.anim_t = 0
            self.anim_f = 1 - self.anim_f

        # Patrol
        if self.moving_right:
            self.rect.x += self.speed
            if self.rect.right >= self.patrol_right:
                self.moving_right = False
        else:
            self.rect.x -= self.speed
            if self.rect.left <= self.patrol_left:
                self.moving_right = True

    def draw(self, screen, camera_x):
        if not self.alive:
            if self.death_timer > 0:
                draw_rect = self.rect.move(-camera_x, 0)
                pygame.draw.rect(screen, WHITE, draw_rect)
            return

        draw_rect = self.rect.move(-camera_x, 0)
        if self.anim_f == 0:
            spr = self.spr0
            spr_flip = self.spr0_flip
        else:
            spr = self.spr1
            spr_flip = self.spr1_flip

        # Face direction based on movement
        spr = spr if self.moving_right else spr_flip

        sx = draw_rect.centerx - spr.get_width() // 2
        sy = draw_rect.centery - spr.get_height() // 2
        screen.blit(spr, (sx, sy))


class Wasp(Enemy):
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


class Spider(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__(x, y, 28, 28, 1, PURPLE)
        self.home_x = x
        self.speed = 6
        self.lunge_range = 150
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
            if abs(self.rect.x - self.home_x) < 3:
                self.rect.x = self.home_x
                self.returning = False
            elif self.rect.x < self.home_x:
                self.rect.x += self.speed * 0.5
            else:
                self.rect.x -= self.speed * 0.5
        elif player_x is not None:
            dist = abs(self.rect.centerx - player_x)
            if dist < self.lunge_range:
                self.lunging = True
                self.lunge_target_x = player_x


class WaspKing:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 120, 90)  # 3x player size
        self.hp = 10
        self.max_hp = 10
        self.color = ORANGE
        self.alive = True
        self.vel_y = 0

        # Attack pattern state
        self.state = "idle"
        self.state_timer = 0
        self.pattern_index = 0
        self.patterns = ["charge", "slam", "summon"]
        self.idle_time = 60
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
            self.shockwave.width += 10
        else:
            self.shockwave = None

        if self.state == "idle":
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = self.patterns[self.pattern_index]
                self.pattern_index = (self.pattern_index + 1) % len(self.patterns)
                self._start_attack(player)

        elif self.state == "charge":
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
                if self.vel_y == 0 and self.rect.bottom >= self.slam_start_y:
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
            Platform(2000, 540, 200, 60, color),
        ]
        enemies = [
            Wasp(300, 540 - 24, 250, 500),
            Wasp(800, 540 - 24, 750, 1050),
            Wasp(1300, 540 - 24, 1200, 1500),
            Wasp(1750, 540 - 24, 1700, 1950),
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
            Wasp(100, 540 - 24, 50, 250),
            Wasp(800, 540 - 24, 750, 900),
            Fly(450, 280, 400, 600),
            Fly(900, 320, 850, 1100),
            Fly(1650, 320, 1600, 1850),
            Wasp(1500, 540 - 24, 1400, 1650),
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
            Platform(1700, 540, 800, 60, color),  # Boss arena
        ]
        enemies = [
            Wasp(100, 540 - 24, 50, 250),
            Spider(450, 350 - 28, 400, 530),
            Fly(600, 380, 550, 750),
            Wasp(750, 540 - 24, 700, 830),
            Spider(950, 380 - 28, 900, 1050),
            Fly(1100, 250, 1050, 1250),
            Wasp(1400, 540 - 24, 1350, 1530),
        ]
    else:
        platforms = []
        enemies = []

    return platforms, enemies


def check_level_complete(player, enemies):
    """Check if all enemies are dead and player reached end of level."""
    all_dead = all(not e.alive and e.death_timer <= 0 for e in enemies)
    # Player past the rightmost reasonable point
    past_end = player.rect.x > 1900
    return all_dead and past_end


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


def handle_combat(player, enemies, boss=None):
    hit_events = []

    # Player attack hits enemies
    if player.attacking and player.attack_rect:
        for enemy in enemies:
            if enemy.alive and player.attack_rect.colliderect(enemy.rect):
                enemy.take_damage(1)
                if not enemy.alive:
                    hit_events.append("enemy_die")
                else:
                    hit_events.append("hit_enemy")
        # Player attack hits boss
        if boss and boss.alive and player.attack_rect.colliderect(boss.rect):
            boss.take_damage(1)
            if not boss.alive:
                hit_events.append("boss_die")
            else:
                hit_events.append("hit_enemy")

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
                hit_events.append("player_hurt")

    # Boss damages player
    if boss and boss.alive:
        if player.rect.colliderect(boss.rect):
            if player.take_damage(1):
                if player.rect.centerx < boss.rect.centerx:
                    player.rect.x -= 40
                else:
                    player.rect.x += 40
                player.vel_y = -10
                hit_events.append("player_hurt")
        # Shockwave damages player
        if boss.shockwave and boss.shockwave_timer > 0:
            if player.rect.colliderect(boss.shockwave):
                if player.take_damage(1):
                    player.vel_y = -12
                    hit_events.append("player_hurt")

    return hit_events


def draw_boss_hp(screen, boss):
    bar_width = 300
    bar_x = SCREEN_WIDTH // 2 - bar_width // 2
    pygame.draw.rect(screen, (80, 80, 80), (bar_x - 2, 10, bar_width + 4, 22))
    hp_width = int(bar_width * boss.hp / boss.max_hp)
    pygame.draw.rect(screen, ORANGE, (bar_x, 12, hp_width, 18))
    font = pygame.font.Font(None, 24)
    label = font.render("WASP KING", True, WHITE)
    screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 36))


def main():
    pygame.init()
    pygame.mixer.init()

    # Load sound effects
    sound_dir = os.path.join("assets", "sounds")
    sounds = {}
    sound_names = [
        "jump", "hover", "attack", "hit_enemy", "player_hurt",
        "enemy_die", "boss_charge", "boss_slam", "boss_die", "level_complete"
    ]
    for name in sound_names:
        path = os.path.join(sound_dir, f"{name}.wav")
        if os.path.exists(path):
            sounds[name] = pygame.mixer.Sound(path)
            sounds[name].set_volume(0.5)
    # Hover sound needs to loop, set it quieter
    if "hover" in sounds:
        sounds["hover"].set_volume(0.3)

    def play_music(track_name):
        """Load and play background music on loop."""
        path = os.path.join(sound_dir, f"{track_name}.wav")
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # -1 = loop forever

    def stop_music():
        pygame.mixer.music.stop()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    game_state = STATE_TITLE
    current_level = 0

    # Initialize game objects (will be reset when starting/restarting)
    platforms = []
    enemies = []
    player = None
    camera = None
    boss = None

    def start_level():
        nonlocal platforms, enemies, player, camera, boss
        platforms, enemies = create_level(current_level)
        player = Player(50, 400)
        player.hp = PLAYER_MAX_HP
        camera = Camera()
        # Spawn boss on level 3 (index 2)
        if current_level == 2:
            boss = WaspKing(2000, 540 - 90)  # In the boss arena
        else:
            boss = None

    hover_channel = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_state == STATE_TITLE:
                        current_level = 0
                        start_level()
                        game_state = STATE_PLAYING
                    elif game_state == STATE_GAME_OVER:
                        start_level()
                        game_state = STATE_PLAYING
                    elif game_state == STATE_LEVEL_TRANSITION:
                        start_level()
                        game_state = STATE_PLAYING
                    elif game_state == STATE_VICTORY:
                        current_level = 0
                        game_state = STATE_TITLE
                if event.key in (pygame.K_z, pygame.K_x) and game_state == STATE_PLAYING:
                    player.start_attack()
                    if "attack" in sounds:
                        sounds["attack"].play()

        if game_state == STATE_PLAYING:
            keys = pygame.key.get_pressed()
            player.update(keys, platforms)

            # Jump sound — fires the frame the player leaves the ground
            if player.just_jumped and "jump" in sounds:
                sounds["jump"].play()

            # Hover sound — loop while hovering, stop when done
            if player.is_hovering and "hover" in sounds:
                if hover_channel is None or not hover_channel.get_busy():
                    hover_channel = sounds["hover"].play(-1)
            else:
                if hover_channel and hover_channel.get_busy():
                    hover_channel.stop()
                    hover_channel = None

            for enemy in enemies:
                if isinstance(enemy, Spider):
                    enemy.update(player.rect.centerx)
                else:
                    enemy.update()
            if boss and boss.alive:
                boss.update(player, platforms)
                # Add summoned flies to enemy list
                if boss.summoned_flies:
                    enemies.extend(boss.summoned_flies)
                    boss.summoned_flies = []
            combat_events = handle_combat(player, enemies, boss)
            for evt in combat_events:
                if evt in sounds:
                    sounds[evt].play()
            camera.update(player)

            # Check for death
            if player.hp <= 0:
                game_state = STATE_GAME_OVER

            # Check for level complete or boss defeat
            if current_level == 2 and boss and not boss.alive:
                game_state = STATE_VICTORY
            elif current_level < 2 and check_level_complete(player, enemies):
                current_level += 1
                game_state = STATE_LEVEL_TRANSITION

        # Drawing
        if game_state == STATE_TITLE:
            draw_title_screen(screen)
        elif game_state == STATE_PLAYING:
            screen.fill(LEVEL_THEMES[current_level]["bg"])
            for p in platforms:
                p.draw(screen, camera.x)
            for enemy in enemies:
                enemy.draw(screen, camera.x)
            if boss and boss.alive:
                boss.draw(screen, camera.x)
            player.draw(screen, camera.x)
            draw_hud(screen, player, LEVEL_THEMES[current_level]["name"])
            if boss and boss.alive:
                draw_boss_hp(screen, boss)
        elif game_state == STATE_GAME_OVER:
            draw_game_over(screen)
        elif game_state == STATE_LEVEL_TRANSITION:
            draw_transition(screen, LEVEL_THEMES[current_level]["name"])
        elif game_state == STATE_VICTORY:
            draw_victory(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
