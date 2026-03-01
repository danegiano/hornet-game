import os, re

with open("main.py", "r") as f:
    s = f.read()

# Replace the bg loading block inside ParallaxBackground.__init__
bg_block_old = """        if level_num == 0:
            self.sky_color = (135, 200, 235)
            try:
                l1 = pygame.image.load(os.path.join("sprites", "bg_garden_1.png")).convert_alpha()
                l2 = pygame.image.load(os.path.join("sprites", "bg_garden_2.png")).convert_alpha()
                l3 = pygame.image.load(os.path.join("sprites", "bg_garden_3.png")).convert_alpha()
                self.layers = [(l1, 0.15), (l2, 0.4), (l3, 0.7)]
            except Exception as e:
                print("Could not load parallax:", e)
        elif level_num == 1:
            self.sky_color = (180, 160, 80)
        else:"""

bg_block_new = """        if level_num == 0:
            self.sky_color = (135, 200, 235)
            try:
                l1 = pygame.image.load(os.path.join("sprites", "bg_garden_1.png")).convert_alpha()
                l2 = pygame.image.load(os.path.join("sprites", "bg_garden_2.png")).convert_alpha()
                l3 = pygame.image.load(os.path.join("sprites", "bg_garden_3.png")).convert_alpha()
                self.layers = [(l1, 0.15), (l2, 0.4), (l3, 0.7)]
            except Exception as e:
                pass
        elif level_num == 1:
            self.sky_color = (110, 80, 20)
            try:
                l1 = pygame.image.load(os.path.join("sprites", "bg_hive_1.png")).convert_alpha()
                l2 = pygame.image.load(os.path.join("sprites", "bg_hive_2.png")).convert_alpha()
                l3 = pygame.image.load(os.path.join("sprites", "bg_hive_3.png")).convert_alpha()
                self.layers = [(l1, 0.15), (l2, 0.4), (l3, 0.7)]
            except Exception as e:
                pass
        else:"""

if bg_block_old in s:
    s = s.replace(bg_block_old, bg_block_new)

# Add is_hive to Platform init
plat_init_old = """    def __init__(self, x, y, width, height, color=(100, 180, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_garden = (color == (100, 180, 100))"""
plat_init_new = """    def __init__(self, x, y, width, height, color=(100, 180, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_garden = (color == (100, 180, 100))
        self.is_hive = (color == (160, 120, 60))"""

if plat_init_old in s:
    s = s.replace(plat_init_old, plat_init_new)

# Add Hive drippy honey drawing to Platform draw
plat_draw_old = """        if self.is_garden:
            import math
            for gx in range(0, self.rect.width, 10):
                world_x = self.rect.x + gx
                wind = math.sin(time_ms / 300.0 + world_x / 50.0) * 8
                start_pos = (draw_rect.x + gx, draw_rect.y)
                end_pos = (draw_rect.x + gx + int(wind), draw_rect.y - 12)
                pygame.draw.line(screen, (60, 200, 60), start_pos, end_pos, 2)"""

plat_draw_new = """        if self.is_garden:
            import math
            for gx in range(0, self.rect.width, 10):
                world_x = self.rect.x + gx
                wind = math.sin(time_ms / 300.0 + world_x / 50.0) * 8
                start_pos = (draw_rect.x + gx, draw_rect.y)
                end_pos = (draw_rect.x + gx + int(wind), draw_rect.y - 12)
                pygame.draw.line(screen, (60, 200, 60), start_pos, end_pos, 2)

        elif self.is_hive:
            import math
            # Draw honey comb pattern inside the platform
            for hx in range(10, self.rect.width, 30):
                pygame.draw.ellipse(screen, (180, 140, 40), (draw_rect.x + hx, draw_rect.y + 5, 20, 15))
            
            # Draw dripping honey off the bottom edge!
            for dx in range(15, self.rect.width, 40):
                world_x = self.rect.x + dx
                # Make honey drip down slowly over time and snap back
                drip_y = (time_ms / 20.0 + world_x * 7) % 30
                
                # A strand of honey connecting the drip
                pygame.draw.line(screen, (255, 200, 0), (draw_rect.x + dx, draw_rect.bottom), (draw_rect.x + dx, draw_rect.bottom + int(drip_y)), 3)
                # The actual drop
                pygame.draw.circle(screen, (255, 210, 50), (draw_rect.x + dx, draw_rect.bottom + int(drip_y)), 4)"""

if plat_draw_old in s:
    s = s.replace(plat_draw_old, plat_draw_new)

with open("main.py", "w") as f:
    f.write(s)
print("Hive background patched!")
