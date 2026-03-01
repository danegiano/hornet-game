import re, os

with open("main.py", "r") as f:
    s = f.read()

bg_class = """class ParallaxBackground:
    def __init__(self, level_num):
        self.layers = []
        self.level_num = level_num
        if level_num == 0:
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
        else:
            self.sky_color = (100, 40, 40)

    def draw(self, screen, camera_x):
        screen.fill(self.sky_color)
        for img, speed in self.layers:
            w = img.get_width()
            offset_x = (camera_x * speed) % w
            screen.blit(img, (-offset_x, 0))
            if offset_x > 0:
                screen.blit(img, (-offset_x + w, 0))

"""

if "class ParallaxBackground:" not in s:
    s = s.replace("class Camera:", bg_class + "class Camera:")

plat_pattern = r"class Platform:\n    def __init__.*?def draw\(self, screen, camera_x\):.*?pygame\.draw\.rect\(screen, self\.color, draw_rect\)"
plat_new = """class Platform:
    def __init__(self, x, y, width, height, color=(100, 180, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_garden = (color == (100, 180, 100))

    def draw(self, screen, camera_x, time_ms=0):
        draw_rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(screen, self.color, draw_rect)
        pygame.draw.rect(screen, (30,50,30), draw_rect, 2)

        if self.is_garden:
            import math
            for gx in range(0, self.rect.width, 10):
                world_x = self.rect.x + gx
                wind = math.sin(time_ms / 300.0 + world_x / 50.0) * 8
                start_pos = (draw_rect.x + gx, draw_rect.y)
                end_pos = (draw_rect.x + gx + int(wind), draw_rect.y - 12)
                pygame.draw.line(screen, (60, 200, 60), start_pos, end_pos, 2)"""

s = re.sub(plat_pattern, plat_new, s, flags=re.DOTALL)

if "boss = None\n    bg = None" not in s:
    s = s.replace("boss = None", "boss = None\n    bg = None")
    
if "nonlocal platforms, enemies, player, camera, boss, bg" not in s:
    s = s.replace("nonlocal platforms, enemies, player, camera, boss", "nonlocal platforms, enemies, player, camera, boss, bg")

if "bg = ParallaxBackground(current_level)" not in s:
    s = s.replace("camera = Camera()", "camera = Camera()\n        bg = ParallaxBackground(current_level)")

old_fill = "screen.fill(LEVEL_THEMES[current_level][\"bg\"])"
new_fill = """time_ms = pygame.time.get_ticks()
            if bg:
                bg.draw(screen, camera.x)
            else:
                screen.fill(LEVEL_THEMES[current_level][\"bg\"])"""

if new_fill not in s:
    s = s.replace(old_fill, new_fill)

if "p.draw(screen, camera.x, time_ms)" not in s:
    s = s.replace("p.draw(screen, camera.x)", "p.draw(screen, camera.x, time_ms)")

with open("main.py", "w") as f:
    f.write(s)
print("Patched main.py for Level 1 Parallax and Wind Grass!")
