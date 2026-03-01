import pygame
from src.settings import *


def draw_hud(screen, player, level_name, coins=0):
    # Health bar background
    pygame.draw.rect(screen, (80, 80, 80), (10, 10, 104, 16))
    # Health bar fill
    hp_width = int(100 * player.hp / PLAYER_MAX_HP)
    color = (50, 200, 50) if player.hp > 2 else (200, 50, 50)
    pygame.draw.rect(screen, color, (12, 12, hp_width, 12))

    # Hover meter background
    pygame.draw.rect(screen, (80, 80, 80), (10, 32, 104, 10))
    # Hover meter fill
    hover_width = int(100 * player.hover_fuel / HOVER_MAX)
    pygame.draw.rect(screen, (100, 180, 255), (12, 34, hover_width, 6))

    # Level name
    font = pygame.font.Font(None, 28)
    text = font.render(level_name, True, WHITE)
    screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, 10))

    # Coin counter
    coin_text = font.render(f"Coins: {coins}", True, (255, 220, 50))
    screen.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 36))

    # Poison indicator
    if getattr(player, 'poisoned', False):
        poison_text = font.render("POISONED", True, (0, 200, 0))
        screen.blit(poison_text, (12, 48))


def draw_boss_hp(screen, boss):
    bar_width = 300
    bar_x = SCREEN_WIDTH // 2 - bar_width // 2
    pygame.draw.rect(screen, (80, 80, 80), (bar_x - 2, 10, bar_width + 4, 22))
    hp_width = int(bar_width * boss.hp / boss.max_hp)
    pygame.draw.rect(screen, ORANGE, (bar_x, 12, hp_width, 18))
    font = pygame.font.Font(None, 24)
    label = font.render("WASP KING", True, WHITE)
    screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 36))
