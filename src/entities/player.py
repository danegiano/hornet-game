import pygame
import os
from src.settings import *


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
