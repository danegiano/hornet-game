import pygame
from src.settings import *


def draw_title_screen(screen):
    screen.fill(BLACK)
    font_big = pygame.font.Font(None, 80)
    font_small = pygame.font.Font(None, 36)
    title = font_big.render("HORNET", True, YELLOW)
    prompt = font_small.render("Press ENTER to start", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 350))

def draw_game_over(screen):
    screen.fill(BLACK)
    font_big = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 36)
    title = font_big.render("GAME OVER", True, RED)
    prompt = font_small.render("Press ENTER to retry", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 220))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 330))

def draw_transition(screen, level_name):
    screen.fill(BLACK)
    font_big = pygame.font.Font(None, 56)
    font_small = pygame.font.Font(None, 36)
    title = font_big.render(level_name, True, WHITE)
    prompt = font_small.render("Press ENTER to continue", True, (180, 180, 180))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 240))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 330))

def draw_victory(screen, island=0):
    screen.fill(BLACK)
    font_big = pygame.font.Font(None, 56)
    font_small = pygame.font.Font(None, 36)

    if island == 4:
        # Final boss defeated — GAME COMPLETE!
        font_huge = pygame.font.Font(None, 72)
        title = font_huge.render("GAME COMPLETE!", True, (180, 80, 255))
        subtitle = font_big.render("The Shadow Hornet is defeated!", True, YELLOW)
        power_text = font_small.render("Stinger Upgrade unlocked!", True, (150, 50, 200))
        prompt = font_small.render("Press ENTER to continue", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 240))
        screen.blit(power_text, (SCREEN_WIDTH // 2 - power_text.get_width() // 2, 310))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 400))
    elif island == 3:
        title = font_big.render("The Fire Moth is defeated!", True, (255, 150, 50))
        power_text = font_small.render("Shield unlocked!", True, (100, 200, 255))
        prompt = font_small.render("Press ENTER to continue", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 220))
        screen.blit(power_text, (SCREEN_WIDTH // 2 - power_text.get_width() // 2, 290))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 360))
    elif island == 2:
        title = font_big.render("The Spider Queen is defeated!", True, (180, 100, 255))
        power_text = font_small.render("Wall Climb unlocked!", True, (100, 200, 100))
        prompt = font_small.render("Press ENTER to continue", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 220))
        screen.blit(power_text, (SCREEN_WIDTH // 2 - power_text.get_width() // 2, 290))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 360))
    elif island == 1:
        title = font_big.render("The Beetle Lord is defeated!", True, (100, 200, 80))
        power_text = font_small.render("Dash unlocked!", True, (100, 200, 255))
        prompt = font_small.render("Press ENTER to continue", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 220))
        screen.blit(power_text, (SCREEN_WIDTH // 2 - power_text.get_width() // 2, 290))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 360))
    else:
        title = font_big.render("You defeated the Wasp King!", True, YELLOW)
        power_text = font_small.render("Double Jump unlocked!", True, (100, 200, 255))
        prompt = font_small.render("Press ENTER to continue", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 220))
        screen.blit(power_text, (SCREEN_WIDTH // 2 - power_text.get_width() // 2, 290))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 360))
