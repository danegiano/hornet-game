import pygame
import os
import math
from src.settings import *


class Enemy:
    def __init__(self, x, y, width, height, hp, color, traits=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.hp = hp
        self.color = color
        self.alive = True
        self.death_timer = 0  # Flash timer when killed
        self.hurt_flash_timer = 0

        # --- Trait system ---
        self.traits = traits or []

        # Shadow trait state
        self.shadow_active = False
        self.shadow_timer = 0
        self.shadow_solid_time = 300   # 5 seconds solid at 60fps
        self.shadow_fade_time = 180    # 3 seconds shadow at 60fps

        # Armor trait state
        self.armor_hp = 2 if "armor" in self.traits else 0
        self.armor_flash_timer = 0

        # Ranged trait state
        self.ranged_cooldown = 0
        self.ranged_cooldown_max = 180  # 3 seconds between shots
        self.projectiles = []

    def has_trait(self, trait_name):
        return trait_name in self.traits

    def update_traits(self, player_x=None, player_y=None):
        """Update trait timers and projectiles. Called from subclass update()."""
        # Shadow form toggle
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
        # Hurt flash countdown
        if self.hurt_flash_timer > 0:
            self.hurt_flash_timer -= 1

        # Ranged attack
        if self.has_trait("ranged") and player_x is not None:
            self.ranged_cooldown -= 1
            dist = abs(self.rect.centerx - player_x)
            if dist < 200 and self.ranged_cooldown <= 0:
                self.ranged_cooldown = self.ranged_cooldown_max
                dx = player_x - self.rect.centerx
                dy = (player_y if player_y is not None else self.rect.centery) - self.rect.centery
                length = max(1, (dx**2 + dy**2) ** 0.5)
                speed = 3
                self.projectiles.append({
                    "rect": pygame.Rect(self.rect.centerx - 4, self.rect.centery - 4, 8, 8),
                    "dx": dx / length * speed,
                    "dy": dy / length * speed,
                    "timer": 120,
                })

        # Update projectile positions
        for proj in self.projectiles[:]:
            proj["rect"].x += int(proj["dx"])
            proj["rect"].y += int(proj["dy"])
            proj["timer"] -= 1
            if proj["timer"] <= 0:
                self.projectiles.remove(proj)

    def take_damage(self, amount):
        # Can't be hit in shadow form
        if self.shadow_active:
            return
        # Armor absorbs damage first
        if self.armor_hp > 0:
            self.armor_hp -= amount
            if self.armor_hp <= 0:
                self.armor_flash_timer = 20
                overflow = abs(self.armor_hp)
                self.armor_hp = 0
                if overflow > 0:
                    self.hp -= overflow
                    if self.hp <= 0:
                        self.alive = False
                        self.death_timer = 15
            return
        self.hp -= amount
        self.hurt_flash_timer = 8
        if self.hp <= 0:
            self.alive = False
            self.death_timer = 15

    def draw(self, screen, camera_x):
        if not self.alive:
            if self.death_timer > 0:
                draw_rect = self.rect.move(-camera_x, 0)
                pygame.draw.rect(screen, WHITE, draw_rect)
            return
        draw_rect = self.rect.move(-camera_x, 0)
        # Shadow form — semi-transparent
        if self.shadow_active:
            s = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            s.fill((*self.color, 80))
            screen.blit(s, draw_rect)
        else:
            pygame.draw.rect(screen, self.color, draw_rect)
        # Armor outline
        if self.armor_hp > 0:
            pygame.draw.rect(screen, (180, 180, 180), draw_rect, 3)
        elif self.armor_flash_timer > 0 and self.armor_flash_timer % 4 < 2:
            pygame.draw.rect(screen, WHITE, draw_rect, 2)
        # Draw projectiles
        for proj in self.projectiles:
            proj_draw = proj["rect"].move(-camera_x, 0)
            pygame.draw.circle(screen, self.color, proj_draw.center, 4)

class Wasp(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right, traits=None):
        super().__init__(x, y, 36, 24, 2, WASP_YELLOW, traits)
        self.speed = 2.2
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.moving_right = True

        # Load wasp sprites
        self.scale = 2
        self.spr0 = pygame.image.load(os.path.join("sprites", "wasp_yellow_0.png")).convert_alpha()
        self.spr1 = pygame.image.load(os.path.join("sprites", "wasp_yellow_1.png")).convert_alpha()
        self.spr2 = pygame.image.load(os.path.join("sprites", "wasp_yellow_2.png")).convert_alpha()
        self.spr0 = pygame.transform.scale(self.spr0, (self.spr0.get_width()*self.scale, self.spr0.get_height()*self.scale))
        self.spr1 = pygame.transform.scale(self.spr1, (self.spr1.get_width()*self.scale, self.spr1.get_height()*self.scale))
        self.spr2 = pygame.transform.scale(self.spr2, (self.spr2.get_width()*self.scale, self.spr2.get_height()*self.scale))
        self.spr0_flip = pygame.transform.flip(self.spr0, True, False)
        self.spr1_flip = pygame.transform.flip(self.spr1, True, False)
        self.spr2_flip = pygame.transform.flip(self.spr2, True, False)
        self.player_x = None

        self.anim_t = 0
        self.anim_f = 0

    def update(self, player_x=None, player_y=None):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        self.update_traits(player_x, player_y)
        self.player_x = player_x

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
        close_to_player = (self.player_x is not None and abs(self.rect.centerx - self.player_x) < 60)
        if close_to_player:
            spr      = self.spr2
            spr_flip = self.spr2_flip
        elif self.anim_f == 0:
            spr      = self.spr0
            spr_flip = self.spr0_flip
        else:
            spr      = self.spr1
            spr_flip = self.spr1_flip

        spr = spr if self.moving_right else spr_flip

        sx = draw_rect.centerx - spr.get_width() // 2
        sy = draw_rect.centery - spr.get_height() // 2

        # Shadow form — draw sprite semi-transparent
        if self.shadow_active:
            ghost = spr.copy()
            ghost.set_alpha(80)
            screen.blit(ghost, (sx, sy))
        else:
            screen.blit(spr, (sx, sy))
            if self.hurt_flash_timer > 0 and self.hurt_flash_timer % 4 < 2:
                flash = pygame.Surface(spr.get_size(), pygame.SRCALPHA)
                flash.fill((255, 255, 255, 180))
                screen.blit(flash, (sx, sy), special_flags=pygame.BLEND_RGBA_ADD)

        # Armor outline
        if self.armor_hp > 0:
            pygame.draw.rect(screen, (180, 180, 180), draw_rect.inflate(4, 4), 3)
        elif self.armor_flash_timer > 0 and self.armor_flash_timer % 4 < 2:
            pygame.draw.rect(screen, WHITE, draw_rect.inflate(4, 4), 2)

        # Draw projectiles
        for proj in self.projectiles:
            proj_draw = proj["rect"].move(-camera_x, 0)
            pygame.draw.circle(screen, self.color, proj_draw.center, 4)


class Fly(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right, traits=None):
        super().__init__(x, y, 24, 20, 1, GREEN, traits)
        self.base_y = y
        self.speed = 2.5
        self.wave_offset = 0
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.moving_right = True

        self.scale = 2
        self.spr0 = pygame.image.load(os.path.join("sprites", "fly_black_0.png")).convert_alpha()
        self.spr1 = pygame.image.load(os.path.join("sprites", "fly_black_1.png")).convert_alpha()
        self.spr2 = pygame.image.load(os.path.join("sprites", "fly_black_2.png")).convert_alpha()
        self.spr0 = pygame.transform.scale(self.spr0, (self.spr0.get_width()*self.scale, self.spr0.get_height()*self.scale))
        self.spr1 = pygame.transform.scale(self.spr1, (self.spr1.get_width()*self.scale, self.spr1.get_height()*self.scale))
        self.spr2 = pygame.transform.scale(self.spr2, (self.spr2.get_width()*self.scale, self.spr2.get_height()*self.scale))
        self.spr0_flip = pygame.transform.flip(self.spr0, True, False)
        self.spr1_flip = pygame.transform.flip(self.spr1, True, False)
        self.spr2_flip = pygame.transform.flip(self.spr2, True, False)
        self.player_x = None
        self.anim_t = 0
        self.anim_f = 0

    def update(self, player_x=None, player_y=None):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        self.update_traits(player_x, player_y)
        self.player_x = player_x

        self.anim_t += 1
        if self.anim_t >= 4:
            self.anim_t = 0
            self.anim_f = 1 - self.anim_f

        if self.moving_right:
            self.rect.x += self.speed
            if self.rect.right >= self.patrol_right:
                self.moving_right = False
        else:
            self.rect.x -= self.speed
            if self.rect.left <= self.patrol_left:
                self.moving_right = True

        import math
        self.wave_offset += 0.05
        self.rect.y = self.base_y + int(math.sin(self.wave_offset) * 30)

    def draw(self, screen, camera_x):
        if not self.alive:
            if self.death_timer > 0:
                draw_rect = self.rect.move(-camera_x, 0)
                pygame.draw.rect(screen, WHITE, draw_rect)
            return

        draw_rect = self.rect.move(-camera_x, 0)
        close_to_player = (self.player_x is not None and abs(self.rect.centerx - self.player_x) < 60)
        if close_to_player:
            spr      = self.spr2
            spr_flip = self.spr2_flip
        elif self.anim_f == 0:
            spr      = self.spr0
            spr_flip = self.spr0_flip
        else:
            spr      = self.spr1
            spr_flip = self.spr1_flip

        spr = spr if self.moving_right else spr_flip
        sx = draw_rect.centerx - spr.get_width() // 2
        sy = draw_rect.centery - spr.get_height() // 2

        # Shadow form — draw sprite semi-transparent
        if self.shadow_active:
            ghost = spr.copy()
            ghost.set_alpha(80)
            screen.blit(ghost, (sx, sy))
        else:
            screen.blit(spr, (sx, sy))
            if self.hurt_flash_timer > 0 and self.hurt_flash_timer % 4 < 2:
                flash = pygame.Surface(spr.get_size(), pygame.SRCALPHA)
                flash.fill((255, 255, 255, 180))
                screen.blit(flash, (sx, sy), special_flags=pygame.BLEND_RGBA_ADD)

        # Armor outline
        if self.armor_hp > 0:
            pygame.draw.rect(screen, (180, 180, 180), draw_rect.inflate(4, 4), 3)
        elif self.armor_flash_timer > 0 and self.armor_flash_timer % 4 < 2:
            pygame.draw.rect(screen, WHITE, draw_rect.inflate(4, 4), 2)

        # Draw projectiles
        for proj in self.projectiles:
            proj_draw = proj["rect"].move(-camera_x, 0)
            pygame.draw.circle(screen, self.color, proj_draw.center, 4)


class Spider(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right, traits=None):
        super().__init__(x, y, 28, 28, 1, PURPLE, traits)
        self.home_x = x
        self.speed = 6
        self.lunge_range = 150
        self.lunging = False
        self.lunge_target_x = 0
        self.returning = False
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right

        self.scale = 2
        self.spr0 = pygame.image.load(os.path.join("sprites", "spider_brown_0.png")).convert_alpha()
        self.spr1 = pygame.image.load(os.path.join("sprites", "spider_brown_1.png")).convert_alpha()
        self.spr2 = pygame.image.load(os.path.join("sprites", "spider_brown_2.png")).convert_alpha()
        self.spr0 = pygame.transform.scale(self.spr0, (self.spr0.get_width()*self.scale, self.spr0.get_height()*self.scale))
        self.spr1 = pygame.transform.scale(self.spr1, (self.spr1.get_width()*self.scale, self.spr1.get_height()*self.scale))
        self.spr2 = pygame.transform.scale(self.spr2, (self.spr2.get_width()*self.scale, self.spr2.get_height()*self.scale))
        self.spr0_flip = pygame.transform.flip(self.spr0, True, False)
        self.spr1_flip = pygame.transform.flip(self.spr1, True, False)
        self.spr2_flip = pygame.transform.flip(self.spr2, True, False)
        self.anim_t = 0
        self.anim_f = 0
        self.moving_right = True

    def update(self, player_x=None, player_y=None):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        self.update_traits(player_x, player_y)

        moving = False
        old_x = self.rect.x

        if self.lunging:
            moving = True
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
            moving = True
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

        if self.rect.x > old_x:
            self.moving_right = True
        elif self.rect.x < old_x:
            self.moving_right = False

        if moving:
            self.anim_t += 1
            if self.anim_t >= 6:
                self.anim_t = 0
                self.anim_f = 1 - self.anim_f
        else:
            self.anim_t = 0
            self.anim_f = 0

    def draw(self, screen, camera_x):
        if not self.alive:
            if self.death_timer > 0:
                draw_rect = self.rect.move(-camera_x, 0)
                pygame.draw.rect(screen, WHITE, draw_rect)
            return

        draw_rect = self.rect.move(-camera_x, 0)
        if self.lunging:
            spr      = self.spr2
            spr_flip = self.spr2_flip
        elif self.anim_f == 0:
            spr      = self.spr0
            spr_flip = self.spr0_flip
        else:
            spr      = self.spr1
            spr_flip = self.spr1_flip

        spr = spr if self.moving_right else spr_flip
        sx = draw_rect.centerx - spr.get_width() // 2
        sy = draw_rect.centery - spr.get_height() // 2

        # Shadow form — draw sprite semi-transparent
        if self.shadow_active:
            ghost = spr.copy()
            ghost.set_alpha(80)
            screen.blit(ghost, (sx, sy))
        else:
            screen.blit(spr, (sx, sy))
            if self.hurt_flash_timer > 0 and self.hurt_flash_timer % 4 < 2:
                flash = pygame.Surface(spr.get_size(), pygame.SRCALPHA)
                flash.fill((255, 255, 255, 180))
                screen.blit(flash, (sx, sy), special_flags=pygame.BLEND_RGBA_ADD)

        # Armor outline
        if self.armor_hp > 0:
            pygame.draw.rect(screen, (180, 180, 180), draw_rect.inflate(4, 4), 3)
        elif self.armor_flash_timer > 0 and self.armor_flash_timer % 4 < 2:
            pygame.draw.rect(screen, WHITE, draw_rect.inflate(4, 4), 2)

        # Draw projectiles
        for proj in self.projectiles:
            proj_draw = proj["rect"].move(-camera_x, 0)
            pygame.draw.circle(screen, self.color, proj_draw.center, 4)
