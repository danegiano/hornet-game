import pygame
import os
from src.settings import *
from src.entities.enemies import Fly, Wasp


class WaspKing:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 120, 90)  # 3x player size
        self.hp = 10
        self.max_hp = 10
        self.color = ORANGE
        self.alive = True
        self.vel_y = 0

        self.spr0 = pygame.image.load(os.path.join("sprites", "king_0.png")).convert_alpha()
        self.spr1 = pygame.image.load(os.path.join("sprites", "king_1.png")).convert_alpha()
        self.anim_t = 0
        self.anim_f = 0
        self.facing_right = False

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

        # Animation
        self.anim_t += 1
        flap_speed = 3 if self.state in ["charge", "slam"] else 8
        if self.anim_t >= flap_speed:
            self.anim_t = 0
            self.anim_f = 1 - self.anim_f

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
                self.facing_right = True
            else:
                self.rect.x -= speed
                self.facing_right = False
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

        # Sprite
        spr = self.spr0 if self.anim_f == 0 else self.spr1
        if self.facing_right:
            spr = pygame.transform.flip(spr, True, False)

        screen.blit(spr, draw_rect.topleft)

        # Shockwave
        if self.shockwave and self.shockwave_timer > 0:
            sw = self.shockwave.move(-camera_x, 0)
            wave_surface = pygame.Surface((sw.width, sw.height), pygame.SRCALPHA)
            wave_surface.fill((255, 100, 50, 150))
            screen.blit(wave_surface, sw)


class SwampBeetleLord:
    """Boss of Island 1: The Swamp.

    A big beetle that walks on the ground. Attacks:
      1. Roll — curls into a ball and rolls across the arena, bouncing off walls once.
      2. Stomp — jumps high, slams down, sends shockwaves left AND right.
      3. Summon — spawns 2-3 small wasps to help.
    """

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 80)
        self.hp = 15
        self.max_hp = 15
        self.color = (40, 80, 30)       # Dark green
        self.alive = True
        self.vel_y = 0
        self.vel_x = 0

        # Attack pattern state
        self.state = "idle"
        self.state_timer = 0
        self.pattern_index = 0
        self.patterns = ["roll", "stomp", "summon"]
        self.idle_time = 60
        self.speed_multiplier = 1.0

        # Roll attack
        self.roll_speed = 10
        self.roll_bounces = 0

        # Stomp
        self.stomp_start_y = 0
        self.shockwave = None          # kept for combat.py compatibility
        self.shockwave_left = None
        self.shockwave_right = None
        self.shockwave_timer = 0

        # Summon (same interface name as WaspKing so game.py can use it)
        self.summoned_flies = []

        # Animation (simple rectangle for now — no sprite)
        self.anim_t = 0
        self.anim_f = 0
        self.facing_right = False

        # Arena bounds — set during first update
        self.arena_left = None
        self.arena_right = None

    def take_damage(self, amount):
        self.hp -= amount
        # Gets faster as HP drops
        self.speed_multiplier = 1.0 + (1.0 - self.hp / self.max_hp) * 0.8
        if self.hp <= 0:
            self.alive = False

    def update(self, player, arena_platforms):
        if not self.alive:
            return

        # Figure out arena bounds from platforms (once)
        if self.arena_left is None:
            lefts = [p.rect.left for p in arena_platforms]
            rights = [p.rect.right for p in arena_platforms]
            if lefts:
                self.arena_left = min(lefts)
                self.arena_right = max(rights)
            else:
                self.arena_left = 0
                self.arena_right = 2700

        # Animation tick
        self.anim_t += 1
        anim_speed = 4 if self.state == "roll" else 10
        if self.anim_t >= anim_speed:
            self.anim_t = 0
            self.anim_f = 1 - self.anim_f

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        on_ground = False
        for p in arena_platforms:
            if self.rect.colliderect(p.rect) and self.vel_y > 0:
                self.rect.bottom = p.rect.top
                self.vel_y = 0
                on_ground = True

        # Horizontal movement (for roll attack)
        if self.vel_x != 0:
            self.rect.x += self.vel_x

        # Shockwave timers
        if self.shockwave_timer > 0:
            self.shockwave_timer -= 1
            if self.shockwave_left:
                self.shockwave_left.x -= 8
                self.shockwave_left.width += 8
            if self.shockwave_right:
                self.shockwave_right.width += 8
        else:
            self.shockwave_left = None
            self.shockwave_right = None
            self.shockwave = None

        # ---- State machine ----
        if self.state == "idle":
            self.vel_x = 0
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = self.patterns[self.pattern_index]
                self.pattern_index = (self.pattern_index + 1) % len(self.patterns)
                self._start_attack(player)

        elif self.state == "roll":
            # Roll across the arena
            speed = self.roll_speed * self.speed_multiplier
            self.vel_x = speed if self.facing_right else -speed

            # Bounce off arena edges
            if self.rect.left <= self.arena_left:
                self.rect.left = self.arena_left
                self.facing_right = True
                self.vel_x = speed
                self.roll_bounces += 1
            elif self.rect.right >= self.arena_right:
                self.rect.right = self.arena_right
                self.facing_right = False
                self.vel_x = -speed
                self.roll_bounces += 1

            # After 1 bounce, stop rolling
            if self.roll_bounces >= 2:
                self.vel_x = 0
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)
                self.roll_bounces = 0

        elif self.state == "stomp":
            if self.state_timer > 30:
                # Rising up
                self.rect.y -= 6
                self.state_timer -= 1
            elif self.state_timer > 0:
                # Slamming down fast
                self.vel_y = 18
                self.state_timer -= 1
                # Landed — create TWO shockwaves (left and right)
                if on_ground and self.vel_y == 0:
                    ground_y = self.rect.bottom - 10
                    self.shockwave_left = pygame.Rect(
                        self.rect.left - 20, ground_y, 40, 15
                    )
                    self.shockwave_right = pygame.Rect(
                        self.rect.right - 20, ground_y, 40, 15
                    )
                    # Also set self.shockwave for combat.py compatibility
                    # (combat.py checks boss.shockwave)
                    self.shockwave = self.shockwave_left
                    self.shockwave_timer = 25
                    self.state = "idle"
                    self.state_timer = int(self.idle_time / self.speed_multiplier)

        elif self.state == "summon":
            self.state_timer -= 1
            if self.state_timer <= 0:
                # Spawn 2-3 wasps (using summoned_flies for game.py compat)
                self.summoned_flies = [
                    Wasp(self.rect.x - 60, self.rect.y - 10,
                         self.rect.x - 200, self.rect.x + 200),
                    Wasp(self.rect.right + 60, self.rect.y - 10,
                         self.rect.x - 200, self.rect.x + 200),
                ]
                # Spawn a 3rd wasp when below half HP
                if self.hp <= self.max_hp // 2:
                    self.summoned_flies.append(
                        Wasp(self.rect.centerx, self.rect.y - 50,
                             self.rect.x - 250, self.rect.x + 250)
                    )
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)

    def _start_attack(self, player):
        """Initialize whichever attack we're about to do."""
        if self.state == "roll":
            # Roll toward the player
            self.facing_right = player.rect.centerx > self.rect.centerx
            self.roll_bounces = 0
            self.state_timer = 120  # safety timeout

        elif self.state == "stomp":
            self.stomp_start_y = self.rect.bottom
            self.state_timer = 50

        elif self.state == "summon":
            self.state_timer = 30

    def draw(self, screen, camera_x):
        if not self.alive:
            return
        draw_rect = self.rect.move(-camera_x, 0)

        # Body — a chunky dark green rectangle
        body_color = self.color
        # Flash lighter when rolling
        if self.state == "roll":
            body_color = (60, 120, 40)

        pygame.draw.rect(screen, body_color, draw_rect)
        # Dark border
        pygame.draw.rect(screen, (20, 40, 15), draw_rect, 3)

        # Shell pattern — two lines across the back
        mid_y = draw_rect.y + draw_rect.height // 3
        pygame.draw.line(screen, (30, 60, 20),
                         (draw_rect.x + 5, mid_y),
                         (draw_rect.right - 5, mid_y), 2)
        mid_y2 = draw_rect.y + 2 * draw_rect.height // 3
        pygame.draw.line(screen, (30, 60, 20),
                         (draw_rect.x + 5, mid_y2),
                         (draw_rect.right - 5, mid_y2), 2)

        # Eyes
        eye_y = draw_rect.y + 15
        if self.facing_right:
            pygame.draw.circle(screen, (255, 50, 50),
                               (draw_rect.right - 20, eye_y), 6)
            pygame.draw.circle(screen, WHITE,
                               (draw_rect.right - 18, eye_y - 2), 2)
        else:
            pygame.draw.circle(screen, (255, 50, 50),
                               (draw_rect.x + 20, eye_y), 6)
            pygame.draw.circle(screen, WHITE,
                               (draw_rect.x + 22, eye_y - 2), 2)

        # Legs (little lines on the bottom)
        leg_y = draw_rect.bottom
        for lx_off in [15, 35, 55, 75]:
            # Alternate leg positions for animation
            offset = 3 if (self.anim_f == 0) == (lx_off % 30 < 15) else -3
            pygame.draw.line(screen, (30, 60, 20),
                             (draw_rect.x + lx_off, leg_y),
                             (draw_rect.x + lx_off + offset, leg_y + 10), 3)

        # Shockwaves
        if self.shockwave_timer > 0:
            if self.shockwave_left:
                sw = self.shockwave_left.move(-camera_x, 0)
                wave_surf = pygame.Surface((sw.width, sw.height), pygame.SRCALPHA)
                wave_surf.fill((100, 200, 50, 150))
                screen.blit(wave_surf, sw)
            if self.shockwave_right:
                sw = self.shockwave_right.move(-camera_x, 0)
                wave_surf = pygame.Surface((sw.width, sw.height), pygame.SRCALPHA)
                wave_surf.fill((100, 200, 50, 150))
                screen.blit(wave_surf, sw)
