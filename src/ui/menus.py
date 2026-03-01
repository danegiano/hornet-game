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

def draw_victory(screen):
    screen.fill(BLACK)
    font_big = pygame.font.Font(None, 56)
    font_small = pygame.font.Font(None, 36)
    title = font_big.render("You defeated the Wasp King!", True, YELLOW)
    prompt = font_small.render("Press ENTER to play again", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 240))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 330))
