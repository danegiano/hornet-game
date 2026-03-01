import os, re

path = "main.py"
s = open(path).read()

# Replace Fly
fly_idx = s.find("class Fly(Enemy):")
spider_idx = s.find("class Spider(Enemy):")
waspking_idx = s.find("class WaspKing:")

if fly_idx != -1 and spider_idx != -1 and waspking_idx != -1:
    fly_old = s[fly_idx:spider_idx]
    spider_old = s[spider_idx:waspking_idx]

    fly_new = """class Fly(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__(x, y, 24, 20, 1, GREEN)
        self.base_y = y
        self.speed = 2.5
        self.wave_offset = 0
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.moving_right = True

        self.scale = 2
        self.spr0 = pygame.image.load(os.path.join("sprites", "fly_black_0.png")).convert_alpha()
        self.spr1 = pygame.image.load(os.path.join("sprites", "fly_black_1.png")).convert_alpha()
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
        spr = self.spr0 if self.anim_f == 0 else self.spr1
        spr_flip = self.spr0_flip if self.anim_f == 0 else self.spr1_flip

        spr = spr if self.moving_right else spr_flip
        sx = draw_rect.centerx - spr.get_width() // 2
        sy = draw_rect.centery - spr.get_height() // 2
        screen.blit(spr, (sx, sy))


"""

    spider_new = """class Spider(Enemy):
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

        self.scale = 2
        self.spr0 = pygame.image.load(os.path.join("sprites", "spider_brown_0.png")).convert_alpha()
        self.spr1 = pygame.image.load(os.path.join("sprites", "spider_brown_1.png")).convert_alpha()
        self.spr0 = pygame.transform.scale(self.spr0, (self.spr0.get_width()*self.scale, self.spr0.get_height()*self.scale))
        self.spr1 = pygame.transform.scale(self.spr1, (self.spr1.get_width()*self.scale, self.spr1.get_height()*self.scale))
        self.spr0_flip = pygame.transform.flip(self.spr0, True, False)
        self.spr1_flip = pygame.transform.flip(self.spr1, True, False)
        self.anim_t = 0
        self.anim_f = 0
        self.moving_right = True

    def update(self, player_x=None):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

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
        spr = self.spr0 if self.anim_f == 0 else self.spr1
        spr_flip = self.spr0_flip if self.anim_f == 0 else self.spr1_flip

        spr = spr if self.moving_right else spr_flip
        sx = draw_rect.centerx - spr.get_width() // 2
        sy = draw_rect.centery - spr.get_height() // 2
        screen.blit(spr, (sx, sy))


"""

    s = s.replace(fly_old, fly_new)
    s = s.replace(spider_old, spider_new)
    open(path, "w").write(s)
    print("Patched Fly and Spider!")
else:
    print("Could not find classes!")
