import pygame
import os
from src.settings import *


class ParallaxBackground:
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
        else:
            self.sky_color = (60, 20, 20)
            try:
                l1 = pygame.image.load(os.path.join("sprites", "bg_tower_1.png")).convert_alpha()
                l2 = pygame.image.load(os.path.join("sprites", "bg_tower_2.png")).convert_alpha()
                l3 = pygame.image.load(os.path.join("sprites", "bg_tower_3.png")).convert_alpha()
                self.layers = [(l1, 0.15), (l2, 0.4), (l3, 0.7)]
            except Exception as e:
                pass

    def draw(self, screen, camera_x):
        screen.fill(self.sky_color)
        for img, speed in self.layers:
            w = img.get_width()
            offset_x = (camera_x * speed) % w
            screen.blit(img, (-offset_x, 0))
            if offset_x > 0:
                screen.blit(img, (-offset_x + w, 0))

class Camera:
    def __init__(self):
        self.x = 0

    def update(self, player):
        # Camera follows player, keeping them in the left third of the screen
        target_x = player.rect.centerx - SCREEN_WIDTH // 3
        self.x += (target_x - self.x) * 0.1  # Smooth follow (lerp)
        if self.x < 0:
            self.x = 0  # Don't scroll left past the start of the world
