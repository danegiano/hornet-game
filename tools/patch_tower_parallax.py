import os, re

with open("main.py", "r") as f:
    s = f.read()

# 1. Update ParallaxBackground
bg_old = """        elif level_num == 1:
            self.sky_color = (110, 80, 20)
            try:
                l1 = pygame.image.load(os.path.join("sprites", "bg_hive_1.png")).convert_alpha()
                l2 = pygame.image.load(os.path.join("sprites", "bg_hive_2.png")).convert_alpha()
                l3 = pygame.image.load(os.path.join("sprites", "bg_hive_3.png")).convert_alpha()
                self.layers = [(l1, 0.15), (l2, 0.4), (l3, 0.7)]
            except Exception as e:
                pass
        else:
            self.sky_color = (100, 40, 40)"""

bg_new = """        elif level_num == 1:
            self.sky_color = (110, 80, 20)
            try:
                l1 = pygame.image.load(os.path.join("sprites", "bg_hive_1.png")).convert_alpha()
                l2 = pygame.image.load(os.path.join("sprites", "bg_hive_2.png")).convert_alpha()
                l3 = pygame.image.load(os.path.join("sprites", "bg_hive_3.png")).convert_alpha()
                self.layers = [(l1, 0.15), (l2, 0.4), (l3, 0.7)]
            except Exception as e:
                pass
        else:
            self.sky_color = (60, 20, 20)
            try:
                l1 = pygame.image.load(os.path.join("sprites", "bg_tower_1.png")).convert_alpha()
                l2 = pygame.image.load(os.path.join("sprites", "bg_tower_2.png")).convert_alpha()
                l3 = pygame.image.load(os.path.join("sprites", "bg_tower_3.png")).convert_alpha()
                self.layers = [(l1, 0.15), (l2, 0.4), (l3, 0.7)]
            except Exception as e:
                pass"""

if bg_old in s:
    s = s.replace(bg_old, bg_new)

# 2. Add is_tower to Platform __init__
plat_init_old = """    def __init__(self, x, y, width, height, color=(100, 180, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_garden = (color == (100, 180, 100))
        self.is_hive = (color == (160, 120, 60))"""
        
plat_init_new = """    def __init__(self, x, y, width, height, color=(100, 180, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_garden = (color == (100, 180, 100))
        self.is_hive = (color == (160, 120, 60))
        self.is_tower = (color == (80, 80, 80))"""

if plat_init_old in s:
    s = s.replace(plat_init_old, plat_init_new)

# 3. Add Tower rendering to Platform draw
plat_draw_old = """                # A strand of honey connecting the drip
                pygame.draw.line(screen, (255, 200, 0), (draw_rect.x + dx, draw_rect.bottom), (draw_rect.x + dx, draw_rect.bottom + int(drip_y)), 3)
                # The actual drop
                pygame.draw.circle(screen, (255, 210, 50), (draw_rect.x + dx, draw_rect.bottom + int(drip_y)), 4)"""

plat_draw_new = """                # A strand of honey connecting the drip
                pygame.draw.line(screen, (255, 200, 0), (draw_rect.x + dx, draw_rect.bottom), (draw_rect.x + dx, draw_rect.bottom + int(drip_y)), 3)
                # The actual drop
                pygame.draw.circle(screen, (255, 210, 50), (draw_rect.x + dx, draw_rect.bottom + int(drip_y)), 4)

        elif self.is_tower:
            import math
            # Draw stone bricks pattern
            for bx in range(0, self.rect.width, 40):
                pygame.draw.line(screen, (50, 50, 50), (draw_rect.x + bx, draw_rect.y), (draw_rect.x + bx, draw_rect.bottom), 2)
            for by in range(0, self.rect.height, 20):
                pygame.draw.line(screen, (50, 50, 50), (draw_rect.x, draw_rect.y + by), (draw_rect.right, draw_rect.y + by), 2)
            
            # Animated flickering torches along the top edge
            for tx in range(20, self.rect.width, 80):
                world_x = self.rect.x + tx
                flicker = math.sin(time_ms / 50.0 + world_x) * 4 + math.cos(time_ms / 100.0) * 2
                
                # Torch base
                pygame.draw.rect(screen, (60, 40, 20), (draw_rect.x + tx - 4, draw_rect.y - 15, 8, 15))
                # Flames
                flame_y = draw_rect.y - 15 - int(flicker)
                pygame.draw.circle(screen, (255, 100, 0), (draw_rect.x + tx, flame_y), 6 + int(flicker/2))
                pygame.draw.circle(screen, (255, 200, 0), (draw_rect.x + tx, flame_y + 2), 3 + int(flicker/3))"""

if plat_draw_old in s:
    s = s.replace(plat_draw_old, plat_draw_new)

with open("main.py", "w") as f:
    f.write(s)
print("Tower background patched!")
