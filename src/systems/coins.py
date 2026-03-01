import pygame
import math


class CoinDrop:
    """A coin that floats up then flies toward the player."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.collected = False
        self.float_timer = 20  # float up for 20 frames first
        self.speed = 6

    def update(self, player_rect):
        if self.collected:
            return
        if self.float_timer > 0:
            self.y -= 2  # float upward
            self.float_timer -= 1
        else:
            # Fly toward player
            dx = player_rect.centerx - self.x
            dy = player_rect.centery - self.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < 15:
                self.collected = True
                return
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self, screen, camera_x):
        if self.collected:
            return
        sx = int(self.x - camera_x)
        sy = int(self.y)
        pygame.draw.circle(screen, (255, 220, 50), (sx, sy), 6)
        pygame.draw.circle(screen, (200, 170, 0), (sx, sy), 6, 2)


class CoinManager:
    """Manages all active coin drops."""
    def __init__(self):
        self.coins = []

    def spawn(self, x, y, count):
        """Spawn `count` coin drops at a position."""
        for i in range(count):
            self.coins.append(CoinDrop(x + i * 10 - count * 5, y))

    def update(self, player_rect):
        """Update all coins, return how many were collected this frame."""
        collected = 0
        for coin in self.coins:
            coin.update(player_rect)
            if coin.collected:
                collected += 1
        self.coins = [c for c in self.coins if not c.collected]
        return collected

    def draw(self, screen, camera_x):
        for coin in self.coins:
            coin.draw(screen, camera_x)
