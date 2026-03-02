import pygame
import os
import math
import random
from src.settings import *
from src.entities.enemies import Fly, Wasp, Spider


class WaspKing:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 120, 90)  # 3x player size
        self.name = "Wasp King"
        self.hp = 10
        self.max_hp = 10
        self.color = ORANGE
        self.alive = True
        self.vel_y = 0
        self.hurt_flash_timer = 0

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
        self.hurt_flash_timer = 12
        self.speed_multiplier = 1.0 + (1.0 - self.hp / self.max_hp) * 0.8
        if self.hp <= 0:
            self.alive = False

    def update(self, player, arena_platforms):
        if not self.alive:
            return

        if self.hurt_flash_timer > 0:
            self.hurt_flash_timer -= 1

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

        # Hurt flash — white overlay blinks when taking damage
        if self.hurt_flash_timer > 0 and self.hurt_flash_timer % 4 < 2:
            flash = pygame.Surface(spr.get_size(), pygame.SRCALPHA)
            flash.fill((255, 255, 255, 180))
            screen.blit(flash, draw_rect.topleft, special_flags=pygame.BLEND_RGBA_ADD)

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
        self.name = "Sludge Baron"
        self.hp = 15
        self.max_hp = 15
        self.color = (40, 80, 30)       # Dark green
        self.alive = True
        self.vel_y = 0
        self.vel_x = 0
        self.hurt_flash_timer = 0

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

        # Sprites
        try:
            self.spr0 = pygame.image.load(os.path.join("sprites", "sludge_baron_0.png")).convert_alpha()
            self.spr1 = pygame.image.load(os.path.join("sprites", "sludge_baron_1.png")).convert_alpha()
            self.has_sprites = True
        except Exception:
            self.has_sprites = False

        # Animation
        self.anim_t = 0
        self.anim_f = 0
        self.facing_right = False

        # Arena bounds — set during first update
        self.arena_left = None
        self.arena_right = None

    def take_damage(self, amount):
        self.hp -= amount
        self.hurt_flash_timer = 12
        # Gets faster as HP drops
        self.speed_multiplier = 1.0 + (1.0 - self.hp / self.max_hp) * 0.8
        if self.hp <= 0:
            self.alive = False

    def update(self, player, arena_platforms):
        if not self.alive:
            return

        if self.hurt_flash_timer > 0:
            self.hurt_flash_timer -= 1

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

        if self.has_sprites:
            spr = self.spr1 if self.state == "roll" else self.spr0
            if self.facing_right:
                spr = pygame.transform.flip(spr, True, False)
            screen.blit(spr, draw_rect.topleft)
        else:
            # Fallback: colored rectangle
            body_color = (60, 120, 40) if self.state == "roll" else self.color
            pygame.draw.rect(screen, body_color, draw_rect)
            pygame.draw.rect(screen, (20, 40, 15), draw_rect, 3)

        # Hurt flash — white overlay blinks when taking damage
        if self.hurt_flash_timer > 0 and self.hurt_flash_timer % 4 < 2:
            flash = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            flash.fill((255, 255, 255, 180))
            screen.blit(flash, draw_rect.topleft, special_flags=pygame.BLEND_RGBA_ADD)

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


class CrystalSpiderQueen:
    """Boss of Island 2: The Crystal Caves.

    A giant purple crystal spider that hangs from the ceiling.
    Attacks cycle through:
      1. Web Trap — drops sticky web patches on platforms below.
      2. Crystal Barrage — shoots 3-5 crystal projectiles in a spread.
      3. Ceiling Drop — teleports up, pauses, then slams down on player.
      4. Summon — spawns 2 spiders to help.
    """

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 90)
        self.name = "Crystal Widow"
        self.hp = 22
        self.max_hp = 22
        self.color = (120, 50, 180)  # Purple crystal spider
        self.alive = True
        self.vel_y = 0
        self.vel_x = 0
        self.hurt_flash_timer = 0

        # Attack pattern state
        self.state = "idle"
        self.state_timer = 0
        self.pattern_index = 0
        self.patterns = ["web_trap", "crystal_barrage", "ceiling_drop", "summon"]
        self.idle_time = 60
        self.speed_multiplier = 1.0

        # Floating movement (side to side)
        self.float_y = y         # The y we hover at
        self.float_dir = 1       # 1 = moving right, -1 = moving left
        self.float_speed = 1.5

        # Web traps (sticky patches on platforms)
        self.web_traps = []      # list of pygame.Rect for web patches

        # Crystal projectiles
        self.projectiles = []    # list of dicts: {rect, vel_x, vel_y}

        # Ceiling drop
        self.drop_target_x = 0
        self.pre_drop_y = 0
        self.shockwave = None
        self.shockwave_timer = 0

        # Summon (same interface as other bosses)
        self.summoned_flies = []

        # For combat.py compatibility (shockwave checks)
        self.shockwave_left = None
        self.shockwave_right = None

        # Animation
        self.anim_t = 0
        self.anim_f = 0
        self.facing_right = False

        # Arena bounds
        self.arena_left = None
        self.arena_right = None

        # Leg animation offset
        self.leg_phase = 0

    def take_damage(self, amount):
        self.hp -= amount
        self.hurt_flash_timer = 12
        # Gets faster as HP drops
        self.speed_multiplier = 1.0 + (1.0 - self.hp / self.max_hp) * 0.8
        if self.hp <= 0:
            self.alive = False

    def update(self, player, arena_platforms):
        if not self.alive:
            return

        if self.hurt_flash_timer > 0:
            self.hurt_flash_timer -= 1

        # Figure out arena bounds from platforms (once)
        if self.arena_left is None:
            lefts = [p.rect.left for p in arena_platforms]
            rights = [p.rect.right for p in arena_platforms]
            if lefts:
                self.arena_left = min(lefts)
                self.arena_right = max(rights)
            else:
                self.arena_left = 0
                self.arena_right = 2800

        # Animation tick
        self.anim_t += 1
        if self.anim_t >= 8:
            self.anim_t = 0
            self.anim_f = 1 - self.anim_f
        self.leg_phase += 0.05

        # Update projectiles (crystal shards fall with gravity)
        for proj in self.projectiles[:]:
            proj["rect"].x += proj["vel_x"]
            proj["rect"].y += proj["vel_y"]
            proj["vel_y"] += 0.3  # gravity on crystals
            # Remove if off screen
            if proj["rect"].y > 700 or proj["rect"].x < -50 or proj["rect"].x > 5000:
                self.projectiles.remove(proj)
                continue
            # Remove if hitting a platform
            for p in arena_platforms:
                if proj["rect"].colliderect(p.rect):
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    break

        # Update web traps — they last 5 seconds (300 frames)
        for trap in self.web_traps[:]:
            trap["timer"] -= 1
            if trap["timer"] <= 0:
                self.web_traps.remove(trap)

        # Shockwave timer
        if self.shockwave and self.shockwave_timer > 0:
            self.shockwave_timer -= 1
            self.shockwave.width += 12
            self.shockwave.x -= 6
        else:
            self.shockwave = None

        # ---- State machine ----
        if self.state == "idle":
            # Float side to side
            self.rect.x += self.float_dir * self.float_speed * self.speed_multiplier
            if self.arena_left is not None:
                if self.rect.left <= self.arena_left + 50:
                    self.float_dir = 1
                    self.facing_right = True
                elif self.rect.right >= self.arena_right - 50:
                    self.float_dir = -1
                    self.facing_right = False
            # Keep at floating height (no gravity in idle)
            self.rect.y = self.float_y

            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = self.patterns[self.pattern_index]
                self.pattern_index = (self.pattern_index + 1) % len(self.patterns)
                self._start_attack(player, arena_platforms)

        elif self.state == "web_trap":
            self.state_timer -= 1
            if self.state_timer <= 0:
                # Drop web traps on platforms near the player
                for p in arena_platforms:
                    dist = abs(p.rect.centerx - player.rect.centerx)
                    if dist < 300 and p.rect.width >= 60:
                        # Place a web on this platform
                        web_x = p.rect.x + random.randint(0, max(0, p.rect.width - 40))
                        web_rect = pygame.Rect(web_x, p.rect.top - 5, 40, 10)
                        self.web_traps.append({"rect": web_rect, "timer": 300})
                        if len(self.web_traps) >= 3:
                            break
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)

        elif self.state == "crystal_barrage":
            self.state_timer -= 1
            if self.state_timer == 20:
                # Fire crystal projectiles in a spread
                num_crystals = 3 + (1 if self.hp < self.max_hp // 2 else 0) + \
                               (1 if self.hp < self.max_hp // 4 else 0)
                spread_start = -2
                spread_step = 4 / max(1, num_crystals - 1) if num_crystals > 1 else 0
                for i in range(num_crystals):
                    vel_x = spread_start + spread_step * i
                    vel_y = 2
                    proj_rect = pygame.Rect(
                        self.rect.centerx - 5, self.rect.bottom, 10, 10
                    )
                    self.projectiles.append({
                        "rect": proj_rect, "vel_x": vel_x, "vel_y": vel_y
                    })
            if self.state_timer <= 0:
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)

        elif self.state == "ceiling_drop":
            if self.state_timer > 40:
                # Phase 1: Rise to ceiling fast
                self.rect.y -= 10
                if self.rect.y < 30:
                    self.rect.y = 30
                self.state_timer -= 1
            elif self.state_timer > 20:
                # Phase 2: Track player x, telegraph with position
                self.rect.x += (self.drop_target_x - self.rect.centerx) * 0.15
                self.drop_target_x = player.rect.centerx
                self.state_timer -= 1
            elif self.state_timer > 0:
                # Phase 3: Drop fast!
                self.rect.y += 20
                self.state_timer -= 1
                # Check if landed on a platform
                for p in arena_platforms:
                    if self.rect.colliderect(p.rect) and self.rect.bottom > p.rect.top:
                        self.rect.bottom = p.rect.top
                        # Create shockwave on landing
                        self.shockwave = pygame.Rect(
                            self.rect.centerx - 30, self.rect.bottom - 10,
                            60, 15
                        )
                        self.shockwave_timer = 20
                        self.state = "idle"
                        self.state_timer = int(self.idle_time / self.speed_multiplier)
                        # Return to floating height over time
                        self.float_y = self.rect.y
                        break
            if self.state_timer <= 0 and self.state == "ceiling_drop":
                # Safety: if we didn't hit a platform, go back to idle
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)

        elif self.state == "summon":
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.summoned_flies = [
                    Spider(self.rect.x - 60, self.rect.bottom - 28,
                           self.rect.x - 200, self.rect.x + 200),
                    Spider(self.rect.right + 60, self.rect.bottom - 28,
                           self.rect.x - 200, self.rect.x + 200),
                ]
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)

        # Gradually float back up to a good height after ceiling drop
        if self.state == "idle" and self.float_y > 380:
            self.float_y -= 2
        elif self.state == "idle" and self.float_y < 350:
            self.float_y = 350

    def _start_attack(self, player, arena_platforms):
        """Initialize whichever attack we're about to do."""
        if self.state == "web_trap":
            self.state_timer = 30
        elif self.state == "crystal_barrage":
            self.state_timer = 40
        elif self.state == "ceiling_drop":
            self.drop_target_x = player.rect.centerx
            self.pre_drop_y = self.rect.y
            self.state_timer = 60
        elif self.state == "summon":
            self.state_timer = 30

    def draw(self, screen, camera_x):
        if not self.alive:
            return
        draw_rect = self.rect.move(-camera_x, 0)

        # Body — a purple oval (the spider's abdomen)
        body_color = self.color
        if self.state == "ceiling_drop" and self.state_timer <= 20:
            body_color = (180, 80, 255)  # Flash bright when dropping

        # Main body (oval)
        pygame.draw.ellipse(screen, body_color, draw_rect)
        # Darker border
        pygame.draw.ellipse(screen, (60, 20, 100), draw_rect, 3)

        # Crystal pattern on body — diamond shapes
        cx, cy = draw_rect.centerx, draw_rect.centery
        for dx, dy in [(-15, -10), (15, -10), (0, 10), (-20, 5), (20, 5)]:
            crystal_pts = [
                (cx + dx, cy + dy - 6),
                (cx + dx + 5, cy + dy),
                (cx + dx, cy + dy + 6),
                (cx + dx - 5, cy + dy),
            ]
            pygame.draw.polygon(screen, (180, 130, 255), crystal_pts)
            pygame.draw.polygon(screen, (220, 180, 255), crystal_pts, 1)

        # Eyes — 4 glowing red eyes
        eye_y = draw_rect.y + 20
        eye_x = draw_rect.centerx
        for ex_off in [-12, -5, 5, 12]:
            pygame.draw.circle(screen, (255, 30, 30), (eye_x + ex_off, eye_y), 4)
            pygame.draw.circle(screen, (255, 150, 150), (eye_x + ex_off, eye_y - 1), 2)

        # 8 legs — 4 on each side, animated
        for i in range(4):
            phase = self.leg_phase + i * 0.8
            sway = int(math.sin(phase) * 5)

            # Left legs
            leg_start_y = draw_rect.y + 20 + i * 15
            lx = draw_rect.x
            pygame.draw.line(screen, (80, 30, 120),
                             (lx, leg_start_y),
                             (lx - 20 - i * 3 + sway, leg_start_y + 15 + i * 3), 3)
            # Claw at end
            pygame.draw.line(screen, (80, 30, 120),
                             (lx - 20 - i * 3 + sway, leg_start_y + 15 + i * 3),
                             (lx - 25 - i * 3 + sway, leg_start_y + 20 + i * 3), 2)

            # Right legs
            rx = draw_rect.right
            pygame.draw.line(screen, (80, 30, 120),
                             (rx, leg_start_y),
                             (rx + 20 + i * 3 - sway, leg_start_y + 15 + i * 3), 3)
            pygame.draw.line(screen, (80, 30, 120),
                             (rx + 20 + i * 3 - sway, leg_start_y + 15 + i * 3),
                             (rx + 25 + i * 3 - sway, leg_start_y + 20 + i * 3), 2)

        # Draw crystal projectiles
        for proj in self.projectiles:
            prect = proj["rect"].move(-camera_x, 0)
            # Draw as a small diamond/crystal shape
            pcx, pcy = prect.centerx, prect.centery
            pts = [
                (pcx, pcy - 6),
                (pcx + 5, pcy),
                (pcx, pcy + 6),
                (pcx - 5, pcy),
            ]
            pygame.draw.polygon(screen, (200, 150, 255), pts)
            pygame.draw.polygon(screen, (255, 220, 255), pts, 1)

        # Draw web traps
        for trap in self.web_traps:
            trect = trap["rect"].move(-camera_x, 0)
            # Semi-transparent white web patch
            web_surf = pygame.Surface((trect.width, trect.height), pygame.SRCALPHA)
            alpha = min(180, trap["timer"])
            web_surf.fill((255, 255, 255, alpha))
            screen.blit(web_surf, trect)
            # Draw web strands
            for wx in range(0, trect.width, 8):
                pygame.draw.line(screen, (200, 200, 200, alpha),
                                 (trect.x + wx, trect.y),
                                 (trect.x + trect.width // 2, trect.bottom), 1)

        # Hurt flash — white overlay blinks when taking damage
        if self.hurt_flash_timer > 0 and self.hurt_flash_timer % 4 < 2:
            flash = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            flash.fill((255, 255, 255, 180))
            screen.blit(flash, draw_rect.topleft, special_flags=pygame.BLEND_RGBA_ADD)

        # Shockwave
        if self.shockwave and self.shockwave_timer > 0:
            sw = self.shockwave.move(-camera_x, 0)
            wave_surf = pygame.Surface((sw.width, sw.height), pygame.SRCALPHA)
            wave_surf.fill((180, 100, 255, 150))
            screen.blit(wave_surf, sw)


class FireMoth:
    """Boss of Island 3: The Volcano.

    A fiery moth that flies around the arena. Attacks cycle through:
      1. Fireball Rain — flies to top center, drops 5-8 fireballs that leave burning patches.
      2. Flame Dash — dashes horizontally across the screen, leaving a fire trail.
      3. Flame Wall — sends a tall fire wall across the arena with a gap to dodge through.
      4. Summon — spawns 2 flies to help.
    """

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 70)
        self.name = "Inferno Empress"
        self.hp = 33
        self.max_hp = 33
        self.color = (255, 120, 30)  # Fiery orange
        self.alive = True
        self.vel_y = 0
        self.vel_x = 0
        self.hurt_flash_timer = 0

        # Attack pattern state
        self.state = "idle"
        self.state_timer = 0
        self.pattern_index = 0
        self.patterns = ["fireball_rain", "flame_dash", "flame_wall", "summon"]
        self.idle_time = 60
        self.speed_multiplier = 1.0

        # Floating movement (erratic circular pattern)
        self.float_y = y
        self.float_angle = 0       # For circular floating movement
        self.float_dir = 1         # 1 = moving right, -1 = moving left
        self.float_speed = 2.0

        # Fireball Rain
        self.projectiles = []       # list of dicts: {rect, vel_y} — falling fireballs
        self.burning_patches = []   # list of dicts: {rect, timer} — ground fire

        # Flame Dash
        self.dash_dir = 1           # 1 = right, -1 = left
        self.fire_trail = []        # list of dicts: {rect, timer} — trail of fire

        # Flame Wall
        self.flame_wall = None      # dict: {rect, vel_x, gap_y, gap_height} or None

        # Summon (same interface as other bosses)
        self.summoned_flies = []

        # For combat.py compatibility (shockwave checks)
        self.shockwave = None
        self.shockwave_left = None
        self.shockwave_right = None
        self.shockwave_timer = 0

        # Animation
        self.anim_t = 0
        self.anim_f = 0
        self.facing_right = False
        self.wing_phase = 0

        # Arena bounds
        self.arena_left = None
        self.arena_right = None

    def take_damage(self, amount):
        self.hp -= amount
        self.hurt_flash_timer = 12
        # Gets faster and meaner as HP drops
        self.speed_multiplier = 1.0 + (1.0 - self.hp / self.max_hp) * 0.8
        if self.hp <= 0:
            self.alive = False

    def update(self, player, arena_platforms):
        if not self.alive:
            return

        if self.hurt_flash_timer > 0:
            self.hurt_flash_timer -= 1

        # Figure out arena bounds from platforms (once)
        if self.arena_left is None:
            lefts = [p.rect.left for p in arena_platforms]
            rights = [p.rect.right for p in arena_platforms]
            if lefts:
                self.arena_left = min(lefts)
                self.arena_right = max(rights)
            else:
                self.arena_left = 0
                self.arena_right = 3250

        # Animation tick
        self.anim_t += 1
        if self.anim_t >= 4:
            self.anim_t = 0
            self.anim_f = 1 - self.anim_f
        self.wing_phase += 0.15

        # Update fireballs (they fall with gravity)
        for proj in self.projectiles[:]:
            proj["rect"].y += proj["vel_y"]
            proj["vel_y"] += 0.5  # Gravity on fireballs
            # Check if fireball hit a platform — leave a burning patch
            landed = False
            for p in arena_platforms:
                if proj["rect"].colliderect(p.rect) and proj["vel_y"] > 0:
                    # Create a burning patch where it landed
                    patch_rect = pygame.Rect(
                        proj["rect"].x - 10, p.rect.top - 6, 28, 8
                    )
                    self.burning_patches.append({"rect": patch_rect, "timer": 180})  # 3 seconds
                    landed = True
                    break
            if landed:
                self.projectiles.remove(proj)
                continue
            # Remove if off screen
            if proj["rect"].y > 700:
                self.projectiles.remove(proj)

        # Update burning patches (they count down and disappear)
        for patch in self.burning_patches[:]:
            patch["timer"] -= 1
            if patch["timer"] <= 0:
                self.burning_patches.remove(patch)

        # Update fire trail (from flame dash)
        for trail in self.fire_trail[:]:
            trail["timer"] -= 1
            if trail["timer"] <= 0:
                self.fire_trail.remove(trail)

        # Update flame wall
        if self.flame_wall:
            self.flame_wall["rect"].x += self.flame_wall["vel_x"]
            # Remove if off screen
            if (self.flame_wall["rect"].x > self.arena_right + 100 or
                    self.flame_wall["rect"].right < self.arena_left - 100):
                self.flame_wall = None

        # ---- State machine ----
        if self.state == "idle":
            # Float around in an erratic pattern (no gravity — it's a moth!)
            self.float_angle += 0.03 * self.speed_multiplier
            self.rect.x += self.float_dir * self.float_speed * self.speed_multiplier
            self.rect.y = self.float_y + int(math.sin(self.float_angle) * 30)

            # Bounce off arena edges
            if self.arena_left is not None:
                if self.rect.left <= self.arena_left + 30:
                    self.float_dir = 1
                    self.facing_right = True
                elif self.rect.right >= self.arena_right - 30:
                    self.float_dir = -1
                    self.facing_right = False

            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = self.patterns[self.pattern_index]
                self.pattern_index = (self.pattern_index + 1) % len(self.patterns)
                self._start_attack(player)

        elif self.state == "fireball_rain":
            # Phase 1: Fly to top center of arena
            if self.state_timer > 30:
                target_x = (self.arena_left + self.arena_right) // 2
                target_y = 80
                self.rect.x += (target_x - self.rect.centerx) * 0.1
                self.rect.y += (target_y - self.rect.centery) * 0.1
                self.state_timer -= 1
            elif self.state_timer > 0:
                # Phase 2: Drop fireballs at random x positions
                if self.state_timer % 5 == 0:
                    num_fireballs = 5 + (3 if self.hp < self.max_hp // 2 else 0)
                    # Drop one fireball per tick (spread over the timer)
                    fx = random.randint(self.arena_left + 40, self.arena_right - 40)
                    fireball_rect = pygame.Rect(fx, self.rect.bottom, 8, 8)
                    self.projectiles.append({"rect": fireball_rect, "vel_y": 2})
                self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)
                self.float_y = 300  # Return to floating height

        elif self.state == "flame_dash":
            # Dash horizontally very fast, leaving fire trail
            speed = 12 * self.speed_multiplier
            self.rect.x += self.dash_dir * speed

            # Leave fire trail behind
            trail_rect = pygame.Rect(
                self.rect.centerx - 4, self.rect.centery - 4, 8, 8
            )
            self.fire_trail.append({"rect": trail_rect, "timer": 60})  # 1 second

            # Check if we've crossed the arena
            if (self.dash_dir > 0 and self.rect.right >= self.arena_right) or \
               (self.dash_dir < 0 and self.rect.left <= self.arena_left):
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)
                self.float_y = 300

        elif self.state == "flame_wall":
            self.state_timer -= 1
            if self.state_timer == 30:
                # Create the flame wall — a tall rect with a gap
                wall_height = 400
                gap_height = 80  # Player can fit through this gap
                gap_y = random.randint(200, 440)  # Random gap position
                if self.facing_right:
                    wall_x = self.arena_left - 20
                    wall_vel = 4 * self.speed_multiplier
                else:
                    wall_x = self.arena_right + 20
                    wall_vel = -4 * self.speed_multiplier
                self.flame_wall = {
                    "rect": pygame.Rect(wall_x, 140, 30, wall_height),
                    "vel_x": wall_vel,
                    "gap_y": gap_y,
                    "gap_height": gap_height,
                }
            if self.state_timer <= 0:
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)

        elif self.state == "summon":
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.summoned_flies = [
                    Fly(self.rect.x - 60, self.rect.y,
                        self.rect.x - 200, self.rect.x + 200),
                    Fly(self.rect.right + 60, self.rect.y,
                        self.rect.x - 200, self.rect.x + 200),
                ]
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)

        # Keep the moth from drifting too far vertically in idle
        if self.state == "idle" and self.float_y > 350:
            self.float_y -= 1
        elif self.state == "idle" and self.float_y < 250:
            self.float_y += 1

    def _start_attack(self, player):
        """Initialize whichever attack we're about to do."""
        if self.state == "fireball_rain":
            self.state_timer = 60  # 30 frames to fly up, 30 to rain fire
        elif self.state == "flame_dash":
            # Dash toward the player
            self.dash_dir = 1 if player.rect.centerx > self.rect.centerx else -1
            self.facing_right = self.dash_dir > 0
            # Position at the correct height for the dash
            self.rect.y = player.rect.y - 20
        elif self.state == "flame_wall":
            self.state_timer = 50
        elif self.state == "summon":
            self.state_timer = 30

    def get_all_damage_rects(self):
        """Return a list of all rects that damage the player.
        Used by game.py to check fire damage."""
        rects = []
        for patch in self.burning_patches:
            rects.append(patch["rect"])
        for trail in self.fire_trail:
            rects.append(trail["rect"])
        # Flame wall — everything EXCEPT the gap damages
        if self.flame_wall:
            wall = self.flame_wall
            wr = wall["rect"]
            gap_y = wall["gap_y"]
            gap_h = wall["gap_height"]
            # Top section (above the gap)
            if gap_y > wr.y:
                rects.append(pygame.Rect(wr.x, wr.y, wr.width, gap_y - wr.y))
            # Bottom section (below the gap)
            gap_bottom = gap_y + gap_h
            if gap_bottom < wr.bottom:
                rects.append(pygame.Rect(wr.x, gap_bottom, wr.width, wr.bottom - gap_bottom))
        return rects

    def draw(self, screen, camera_x):
        if not self.alive:
            return
        draw_rect = self.rect.move(-camera_x, 0)

        # --- Draw the moth body ---
        body_color = self.color
        if self.state == "flame_dash":
            body_color = (255, 200, 50)  # Flash bright yellow when dashing

        # Body — oval shape
        pygame.draw.ellipse(screen, body_color, draw_rect)
        # Darker border
        pygame.draw.ellipse(screen, (180, 80, 10), draw_rect, 2)

        # Wings — two big wings on each side, animated with flapping
        wing_offset = int(math.sin(self.wing_phase) * 8)
        cx, cy = draw_rect.centerx, draw_rect.centery

        # Left wing (upper)
        lw_pts = [
            (cx - 5, cy - 5),
            (cx - 40 - wing_offset, cy - 30 - wing_offset),
            (cx - 35 - wing_offset, cy + 5),
        ]
        pygame.draw.polygon(screen, (255, 160, 50), lw_pts)
        pygame.draw.polygon(screen, (255, 200, 100), lw_pts, 2)

        # Left wing (lower)
        lw2_pts = [
            (cx - 5, cy + 5),
            (cx - 30 - wing_offset // 2, cy + 25 + wing_offset // 2),
            (cx - 20 - wing_offset // 2, cy - 5),
        ]
        pygame.draw.polygon(screen, (255, 140, 30), lw2_pts)

        # Right wing (upper)
        rw_pts = [
            (cx + 5, cy - 5),
            (cx + 40 + wing_offset, cy - 30 - wing_offset),
            (cx + 35 + wing_offset, cy + 5),
        ]
        pygame.draw.polygon(screen, (255, 160, 50), rw_pts)
        pygame.draw.polygon(screen, (255, 200, 100), rw_pts, 2)

        # Right wing (lower)
        rw2_pts = [
            (cx + 5, cy + 5),
            (cx + 30 + wing_offset // 2, cy + 25 + wing_offset // 2),
            (cx + 20 + wing_offset // 2, cy - 5),
        ]
        pygame.draw.polygon(screen, (255, 140, 30), rw2_pts)

        # Glowing center — a bright yellow-white center on the body
        pygame.draw.ellipse(screen, (255, 220, 100),
                            (cx - 12, cy - 10, 24, 20))
        # Hot core glow
        glow_pulse = int(math.sin(self.wing_phase * 2) * 3)
        pygame.draw.ellipse(screen, (255, 255, 180),
                            (cx - 6 - glow_pulse, cy - 5 - glow_pulse,
                             12 + glow_pulse * 2, 10 + glow_pulse * 2))

        # Eyes — two glowing red-orange eyes
        eye_y = draw_rect.y + 18
        pygame.draw.circle(screen, (255, 50, 0), (cx - 10, eye_y), 5)
        pygame.draw.circle(screen, (255, 200, 100), (cx - 9, eye_y - 2), 2)
        pygame.draw.circle(screen, (255, 50, 0), (cx + 10, eye_y), 5)
        pygame.draw.circle(screen, (255, 200, 100), (cx + 11, eye_y - 2), 2)

        # Antennae
        pygame.draw.line(screen, (200, 100, 20),
                         (cx - 8, draw_rect.y + 5),
                         (cx - 20, draw_rect.y - 15), 2)
        pygame.draw.line(screen, (200, 100, 20),
                         (cx + 8, draw_rect.y + 5),
                         (cx + 20, draw_rect.y - 15), 2)
        # Antenna tips (glowing dots)
        pygame.draw.circle(screen, (255, 200, 50), (cx - 20, draw_rect.y - 15), 3)
        pygame.draw.circle(screen, (255, 200, 50), (cx + 20, draw_rect.y - 15), 3)

        # --- Draw fireballs (falling projectiles) ---
        for proj in self.projectiles:
            prect = proj["rect"].move(-camera_x, 0)
            pygame.draw.rect(screen, (255, 100, 0), prect)
            # Bright center
            pygame.draw.rect(screen, (255, 220, 50),
                             (prect.x + 2, prect.y + 2, 4, 4))

        # --- Draw burning patches on the ground ---
        for patch in self.burning_patches:
            prect = patch["rect"].move(-camera_x, 0)
            alpha = min(200, patch["timer"] + 50)
            fire_surf = pygame.Surface((prect.width, prect.height), pygame.SRCALPHA)
            fire_surf.fill((255, 80, 0, alpha))
            screen.blit(fire_surf, prect)
            # Flickering flame on top
            if patch["timer"] % 6 < 3:
                flame_x = prect.x + prect.width // 2
                pygame.draw.circle(screen, (255, 200, 50),
                                   (flame_x, prect.y - 3), 3)

        # --- Draw fire trail (from flame dash) ---
        for trail in self.fire_trail:
            trect = trail["rect"].move(-camera_x, 0)
            alpha = min(200, trail["timer"] * 4)
            trail_surf = pygame.Surface((trect.width, trect.height), pygame.SRCALPHA)
            trail_surf.fill((255, 120, 0, alpha))
            screen.blit(trail_surf, trect)

        # --- Draw flame wall ---
        if self.flame_wall:
            wall = self.flame_wall
            wr = wall["rect"].move(-camera_x, 0)
            gap_y = wall["gap_y"]
            gap_h = wall["gap_height"]

            # Top section (above gap)
            if gap_y > wall["rect"].y:
                top_h = gap_y - wall["rect"].y
                top_surf = pygame.Surface((wr.width, top_h), pygame.SRCALPHA)
                top_surf.fill((255, 60, 0, 180))
                screen.blit(top_surf, (wr.x, wr.y))

            # Bottom section (below gap)
            gap_bottom = gap_y + gap_h
            if gap_bottom < wall["rect"].bottom:
                bot_h = wall["rect"].bottom - gap_bottom
                bot_y = wr.y + (gap_bottom - wall["rect"].y)
                bot_surf = pygame.Surface((wr.width, bot_h), pygame.SRCALPHA)
                bot_surf.fill((255, 60, 0, 180))
                screen.blit(bot_surf, (wr.x, bot_y))

            # Draw gap marker (bright yellow edges so player can see it)
            gap_screen_y = wr.y + (gap_y - wall["rect"].y)
            pygame.draw.line(screen, (255, 255, 100),
                             (wr.x, gap_screen_y),
                             (wr.right, gap_screen_y), 2)
            pygame.draw.line(screen, (255, 255, 100),
                             (wr.x, gap_screen_y + gap_h),
                             (wr.right, gap_screen_y + gap_h), 2)

        # Hurt flash — white overlay blinks when taking damage
        if self.hurt_flash_timer > 0 and self.hurt_flash_timer % 4 < 2:
            flash = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            flash.fill((255, 255, 255, 180))
            screen.blit(flash, draw_rect.topleft, special_flags=pygame.BLEND_RGBA_ADD)


class ShadowHornet:
    """FINAL BOSS of Island 4: The Shadow Fortress.

    A dark mirror of the player — the Shadow Hornet.  Attacks cycle through:
      1. Shadow Charge — flies at the player at high speed, leaving afterimages.
      2. Shadow Stinger — dashes forward and attacks with a stinger hitbox.
      3. Teleport Strike — disappears, reappears behind player, immediate attack.
      4. Shadow Clones — creates clones that mirror movement; only real one takes damage.

    Gets more aggressive as HP drops (enrage at 75%, 50%, 25%).
    """

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 64, 64)
        self.name = "Shadow Phantom"
        self.hp = 50
        self.max_hp = 50
        self.color = (40, 0, 60)        # Deep shadow purple
        self.alive = True
        self.vel_y = 0
        self.vel_x = 0
        self.hurt_flash_timer = 0

        # Attack pattern state
        self.state = "idle"
        self.state_timer = 0
        self.pattern_index = 0
        self.patterns = ["shadow_charge", "shadow_stinger", "teleport_strike", "shadow_clones"]
        self.idle_time = 60
        self.speed_multiplier = 1.0

        # Floating movement
        self.float_y = y
        self.float_angle = 0
        self.float_dir = 1
        self.float_speed = 2.0

        # Shadow Charge
        self.charge_speed = 12
        self.charge_target_x = 0
        self.charge_target_y = 0
        self.shadow_trail = []   # list of dicts: {x, y, timer, alpha}

        # Shadow Stinger
        self.stinger_hitbox = None   # pygame.Rect or None
        self.stinger_timer = 0

        # Teleport Strike
        self.teleport_visible = True   # False during teleport phase
        self.teleport_timer = 0
        self.teleport_target_x = 0
        self.teleport_target_y = 0
        self.teleport_fade = 255       # For fade in/out effect

        # Shadow Clones
        self.clones = []  # list of dicts: {rect, hp, timer, vel_x, vel_y}

        # For combat.py compatibility
        self.shockwave = None
        self.shockwave_left = None
        self.shockwave_right = None
        self.shockwave_timer = 0
        self.summoned_flies = []

        # Animation
        self.anim_t = 0
        self.anim_f = 0
        self.facing_right = False
        self.wing_phase = 0

        # Arena bounds
        self.arena_left = None
        self.arena_right = None

        # Shadow particles (cosmetic)
        self.shadow_particles = []

    def take_damage(self, amount):
        self.hp -= amount
        self.hurt_flash_timer = 12
        # Enrage: gets faster as HP drops
        hp_ratio = self.hp / self.max_hp
        if hp_ratio <= 0.25:
            self.speed_multiplier = 2.0
        elif hp_ratio <= 0.50:
            self.speed_multiplier = 1.6
        elif hp_ratio <= 0.75:
            self.speed_multiplier = 1.3
        else:
            self.speed_multiplier = 1.0
        if self.hp <= 0:
            self.alive = False

    def update(self, player, arena_platforms):
        if not self.alive:
            return

        if self.hurt_flash_timer > 0:
            self.hurt_flash_timer -= 1

        # Figure out arena bounds from platforms (once)
        if self.arena_left is None:
            lefts = [p.rect.left for p in arena_platforms]
            rights = [p.rect.right for p in arena_platforms]
            if lefts:
                self.arena_left = min(lefts)
                self.arena_right = max(rights)
            else:
                self.arena_left = 0
                self.arena_right = 3500

        # Animation tick
        self.anim_t += 1
        if self.anim_t >= 5:
            self.anim_t = 0
            self.anim_f = 1 - self.anim_f
        self.wing_phase += 0.12

        # Update shadow trail (afterimages fade out)
        for trail in self.shadow_trail[:]:
            trail["timer"] -= 1
            trail["alpha"] = max(0, trail["alpha"] - 15)
            if trail["timer"] <= 0:
                self.shadow_trail.remove(trail)

        # Update shadow particles (cosmetic dripping effect)
        if random.random() < 0.3 and self.teleport_visible:
            self.shadow_particles.append({
                "x": self.rect.centerx + random.randint(-20, 20),
                "y": self.rect.bottom + random.randint(-5, 5),
                "timer": 30,
                "vy": random.uniform(0.5, 1.5),
            })
        for p in self.shadow_particles[:]:
            p["y"] += p["vy"]
            p["timer"] -= 1
            if p["timer"] <= 0:
                self.shadow_particles.remove(p)

        # Update stinger hitbox
        if self.stinger_hitbox and self.stinger_timer > 0:
            self.stinger_timer -= 1
        else:
            self.stinger_hitbox = None

        # Update clones
        for clone in self.clones[:]:
            clone["timer"] -= 1
            # Clones mirror the boss's floating movement
            clone["rect"].x += self.float_dir * self.float_speed * self.speed_multiplier
            clone["rect"].y = self.float_y + int(math.sin(self.float_angle + clone.get("phase", 0)) * 30)
            # Keep clones in arena
            if clone["rect"].left < self.arena_left:
                clone["rect"].left = self.arena_left
            if clone["rect"].right > self.arena_right:
                clone["rect"].right = self.arena_right
            if clone["timer"] <= 0:
                self.clones.remove(clone)

        # ---- State machine ----
        if self.state == "idle":
            # Float around
            self.float_angle += 0.03 * self.speed_multiplier
            self.rect.x += self.float_dir * self.float_speed * self.speed_multiplier
            self.rect.y = self.float_y + int(math.sin(self.float_angle) * 25)

            # Bounce off arena edges
            if self.arena_left is not None:
                if self.rect.left <= self.arena_left + 30:
                    self.float_dir = 1
                    self.facing_right = True
                elif self.rect.right >= self.arena_right - 30:
                    self.float_dir = -1
                    self.facing_right = False

            self.state_timer -= 1
            # Shorter idle between attacks when enraged
            if self.state_timer <= 0:
                self.state = self.patterns[self.pattern_index]
                self.pattern_index = (self.pattern_index + 1) % len(self.patterns)
                self._start_attack(player)

        elif self.state == "shadow_charge":
            # Fly at the player at high speed, leaving shadow trail
            speed = self.charge_speed * self.speed_multiplier
            dx = self.charge_target_x - self.rect.centerx
            dy = self.charge_target_y - self.rect.centery
            dist = max(1, math.sqrt(dx * dx + dy * dy))
            self.rect.x += (dx / dist) * speed
            self.rect.y += (dy / dist) * speed
            self.facing_right = dx > 0

            # Leave shadow trail
            self.shadow_trail.append({
                "x": self.rect.x, "y": self.rect.y,
                "timer": 20, "alpha": 150,
            })

            self.state_timer -= 1
            if self.state_timer <= 0 or dist < 20:
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)
                self.float_y = max(250, min(450, self.rect.y))

        elif self.state == "shadow_stinger":
            # Dash forward and attack with a stinger hitbox
            speed = 10 * self.speed_multiplier
            if self.facing_right:
                self.rect.x += speed
            else:
                self.rect.x -= speed

            # Leave trail
            if self.state_timer % 3 == 0:
                self.shadow_trail.append({
                    "x": self.rect.x, "y": self.rect.y,
                    "timer": 15, "alpha": 120,
                })

            self.state_timer -= 1
            # Create stinger hitbox in front
            if self.state_timer == 15:
                if self.facing_right:
                    self.stinger_hitbox = pygame.Rect(
                        self.rect.right, self.rect.centery - 10, 50, 20
                    )
                else:
                    self.stinger_hitbox = pygame.Rect(
                        self.rect.left - 50, self.rect.centery - 10, 50, 20
                    )
                self.stinger_timer = 10

            if self.state_timer <= 0:
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)
                self.float_y = max(250, min(450, self.rect.y))

        elif self.state == "teleport_strike":
            if self.state_timer > 30:
                # Phase 1: Fade out
                self.teleport_fade = max(0, self.teleport_fade - 9)
                if self.teleport_fade <= 0:
                    self.teleport_visible = False
                self.state_timer -= 1
            elif self.state_timer > 10:
                # Phase 2: Invisible — teleport to behind the player
                if self.state_timer == 30:
                    # Calculate position behind the player
                    offset = 80 if not player.facing_right else -80
                    self.teleport_target_x = player.rect.x + offset
                    self.teleport_target_y = player.rect.y
                    self.rect.x = self.teleport_target_x
                    self.rect.y = self.teleport_target_y
                    self.facing_right = player.rect.centerx > self.rect.centerx
                self.state_timer -= 1
            elif self.state_timer > 0:
                # Phase 3: Fade in and immediately attack
                self.teleport_visible = True
                self.teleport_fade = min(255, self.teleport_fade + 30)
                if self.state_timer == 8:
                    # Create stinger attack behind player
                    if self.facing_right:
                        self.stinger_hitbox = pygame.Rect(
                            self.rect.right, self.rect.centery - 10, 50, 20
                        )
                    else:
                        self.stinger_hitbox = pygame.Rect(
                            self.rect.left - 50, self.rect.centery - 10, 50, 20
                        )
                    self.stinger_timer = 10
                self.state_timer -= 1
            if self.state_timer <= 0:
                self.teleport_visible = True
                self.teleport_fade = 255
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)
                self.float_y = max(250, min(450, self.rect.y))

        elif self.state == "shadow_clones":
            self.state_timer -= 1
            if self.state_timer <= 0:
                # Create shadow clones
                hp_ratio = self.hp / self.max_hp
                num_clones = 3 if hp_ratio <= 0.50 else 2
                for i in range(num_clones):
                    offset_x = random.randint(-200, 200)
                    offset_y = random.randint(-50, 50)
                    clone_rect = pygame.Rect(
                        self.rect.x + offset_x,
                        self.rect.y + offset_y,
                        self.rect.width, self.rect.height
                    )
                    # Keep clone in arena
                    if self.arena_left is not None:
                        clone_rect.left = max(self.arena_left, clone_rect.left)
                        clone_rect.right = min(self.arena_right, clone_rect.right)
                    self.clones.append({
                        "rect": clone_rect,
                        "hp": 1,       # One hit reveals it as fake
                        "timer": 300,  # 5 seconds
                        "phase": random.uniform(0, 6.28),
                    })
                self.state = "idle"
                self.state_timer = int(self.idle_time / self.speed_multiplier)

        # Keep floating at a reasonable height
        if self.state == "idle" and self.float_y > 420:
            self.float_y -= 2
        elif self.state == "idle" and self.float_y < 280:
            self.float_y += 2

    def _start_attack(self, player):
        """Initialize whichever attack we're about to do."""
        if self.state == "shadow_charge":
            self.charge_target_x = player.rect.centerx
            self.charge_target_y = player.rect.centery
            self.state_timer = 40
        elif self.state == "shadow_stinger":
            self.facing_right = player.rect.centerx > self.rect.centerx
            # Position at the player's height
            self.rect.y = player.rect.y - 10
            self.state_timer = 30
        elif self.state == "teleport_strike":
            self.teleport_fade = 255
            self.teleport_visible = True
            self.state_timer = 45
        elif self.state == "shadow_clones":
            self.state_timer = 20

    def clone_hit(self, clone):
        """Called when a clone is hit — it disappears."""
        clone["hp"] -= 1
        if clone["hp"] <= 0 and clone in self.clones:
            self.clones.remove(clone)

    def get_all_damage_rects(self):
        """Return list of rects that damage the player (stinger attacks)."""
        rects = []
        if self.stinger_hitbox and self.stinger_timer > 0:
            rects.append(self.stinger_hitbox)
        return rects

    def draw(self, screen, camera_x):
        if not self.alive:
            return

        # Draw shadow trail (afterimages)
        for trail in self.shadow_trail:
            trail_rect = pygame.Rect(trail["x"] - camera_x, trail["y"],
                                      self.rect.width, self.rect.height)
            trail_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            trail_surf.fill((60, 0, 90, trail["alpha"]))
            screen.blit(trail_surf, trail_rect)

        # Draw shadow particles
        for p in self.shadow_particles:
            px = int(p["x"] - camera_x)
            py = int(p["y"])
            alpha = int(255 * (p["timer"] / 30.0))
            particle_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
            particle_surf.fill((80, 20, 120, alpha))
            screen.blit(particle_surf, (px, py))

        # Draw clones (transparent/darker versions)
        for clone in self.clones:
            cr = clone["rect"].move(-camera_x, 0)
            clone_surf = pygame.Surface((cr.width, cr.height), pygame.SRCALPHA)
            # Darker, more transparent version of the boss
            self._draw_hornet_body(clone_surf, pygame.Rect(0, 0, cr.width, cr.height),
                                    alpha=100, is_clone=True)
            screen.blit(clone_surf, cr)

        # Draw the real boss (skip if invisible during teleport)
        if not self.teleport_visible:
            return

        draw_rect = self.rect.move(-camera_x, 0)

        # If fading in/out during teleport, draw with alpha
        if self.teleport_fade < 255:
            boss_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            self._draw_hornet_body(boss_surf, pygame.Rect(0, 0, draw_rect.width, draw_rect.height),
                                    alpha=self.teleport_fade, is_clone=False)
            screen.blit(boss_surf, draw_rect)
        else:
            self._draw_hornet_body(screen, draw_rect, alpha=255, is_clone=False)

        # Draw stinger hitbox (purple slash effect)
        if self.stinger_hitbox and self.stinger_timer > 0:
            sh_rect = self.stinger_hitbox.move(-camera_x, 0)
            slash_surf = pygame.Surface((sh_rect.width, sh_rect.height), pygame.SRCALPHA)
            slash_surf.fill((150, 50, 200, 180))
            screen.blit(slash_surf, sh_rect)

    def _draw_hornet_body(self, surface, rect, alpha=255, is_clone=False):
        """Draw the shadow hornet body on a given surface at the given rect.
        Used for both the real boss and clones."""
        cx, cy = rect.centerx, rect.centery

        # Body color — dark purple, clones are even darker
        if is_clone:
            body_color = (25, 0, 40, alpha)
            accent = (60, 20, 80, alpha)
            eye_color = (120, 40, 160, alpha)
        else:
            body_color = (40, 0, 60, alpha)
            accent = (80, 30, 110, alpha)
            eye_color = (180, 50, 255, alpha)

        # Body — oval
        body_rect = pygame.Rect(rect.x + 8, rect.y + 12, rect.width - 16, rect.height - 16)
        body_surf = pygame.Surface((body_rect.width, body_rect.height), pygame.SRCALPHA)
        pygame.draw.ellipse(body_surf, body_color, (0, 0, body_rect.width, body_rect.height))
        surface.blit(body_surf, body_rect)

        # Dark border
        pygame.draw.ellipse(surface, accent[:3] if len(accent) > 3 else accent, body_rect, 2)

        # Wings — sharp angular wings
        wing_offset = int(math.sin(self.wing_phase) * 6)

        # Left wing
        lw_pts = [
            (cx - 8, cy - 4),
            (cx - 30 - wing_offset, cy - 25 - wing_offset),
            (cx - 25 - wing_offset, cy + 3),
        ]
        wing_col = accent[:3] if len(accent) > 3 else accent
        pygame.draw.polygon(surface, wing_col, lw_pts)

        # Right wing
        rw_pts = [
            (cx + 8, cy - 4),
            (cx + 30 + wing_offset, cy - 25 - wing_offset),
            (cx + 25 + wing_offset, cy + 3),
        ]
        pygame.draw.polygon(surface, wing_col, rw_pts)

        # Glowing eyes — two bright purple dots
        eye_y = rect.y + 20
        eye_col = eye_color[:3] if len(eye_color) > 3 else eye_color
        if self.facing_right:
            pygame.draw.circle(surface, eye_col, (cx + 2, eye_y), 4)
            pygame.draw.circle(surface, eye_col, (cx + 12, eye_y), 4)
            # Glow highlight
            pygame.draw.circle(surface, (255, 200, 255), (cx + 3, eye_y - 1), 2)
            pygame.draw.circle(surface, (255, 200, 255), (cx + 13, eye_y - 1), 2)
        else:
            pygame.draw.circle(surface, eye_col, (cx - 2, eye_y), 4)
            pygame.draw.circle(surface, eye_col, (cx - 12, eye_y), 4)
            pygame.draw.circle(surface, (255, 200, 255), (cx - 1, eye_y - 1), 2)
            pygame.draw.circle(surface, (255, 200, 255), (cx - 11, eye_y - 1), 2)

        # Stinger at the bottom — pointed triangle
        stinger_pts = [
            (cx - 4, rect.bottom - 12),
            (cx, rect.bottom - 2),
            (cx + 4, rect.bottom - 12),
        ]
        stinger_col = (100, 30, 150) if not is_clone else (50, 15, 75)
        pygame.draw.polygon(surface, stinger_col, stinger_pts)

        # Shadow wisp on top of head (dark flame-like effect)
        wisp_offset = int(math.sin(self.wing_phase * 1.5) * 3)
        pygame.draw.line(surface, wing_col,
                         (cx, rect.y + 10),
                         (cx + wisp_offset, rect.y - 2), 3)
        pygame.draw.line(surface, wing_col,
                         (cx - 4, rect.y + 12),
                         (cx - 4 + wisp_offset, rect.y + 2), 2)
