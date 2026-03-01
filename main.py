import pygame
import os
import sys
import math

from src.settings import *


from src.entities.player import Player


from src.world.camera import Camera, ParallaxBackground


from src.world.platforms import Platform


from src.entities.enemies import Enemy, Wasp, Fly, Spider


from src.entities.bosses import WaspKing

def create_level(level_num):
    """Return (platforms, enemies) for the given level number (0-indexed)."""
    theme = LEVEL_THEMES[level_num]
    color = theme["platform"]

    if level_num == 0:  # The Garden
        platforms = [
            Platform(0, 540, 600, 60, color),
            Platform(250, 440, 150, 20, color),
            Platform(500, 380, 200, 20, color),
            Platform(750, 540, 400, 60, color),
            Platform(900, 440, 150, 20, color),
            Platform(1200, 540, 600, 60, color),
            Platform(1400, 420, 150, 20, color),
            Platform(1700, 540, 400, 60, color),
            Platform(2000, 540, 200, 60, color),
        ]
        enemies = [
            Wasp(300, 540 - 24, 250, 500),
            Wasp(800, 540 - 24, 750, 1050),
            Wasp(1300, 540 - 24, 1200, 1500),
            Wasp(1750, 540 - 24, 1700, 1950),
        ]
    elif level_num == 1:  # The Hive
        platforms = [
            Platform(0, 540, 300, 60, color),
            Platform(200, 420, 120, 20, color),
            Platform(400, 340, 120, 20, color),
            Platform(550, 450, 150, 20, color),
            Platform(750, 540, 200, 60, color),
            Platform(850, 380, 120, 20, color),
            Platform(1050, 300, 150, 20, color),
            Platform(1250, 420, 120, 20, color),
            Platform(1400, 540, 300, 60, color),
            Platform(1600, 380, 150, 20, color),
            Platform(1850, 540, 400, 60, color),
        ]
        enemies = [
            Wasp(100, 540 - 24, 50, 250),
            Wasp(800, 540 - 24, 750, 900),
            Fly(450, 280, 400, 600),
            Fly(900, 320, 850, 1100),
            Fly(1650, 320, 1600, 1850),
            Wasp(1500, 540 - 24, 1400, 1650),
        ]
    elif level_num == 2:  # The Throne Room
        platforms = [
            Platform(0, 540, 300, 60, color),
            Platform(200, 420, 100, 20, color),
            Platform(400, 350, 80, 20, color),
            Platform(550, 440, 100, 20, color),
            Platform(700, 540, 150, 60, color),
            Platform(900, 380, 100, 20, color),
            Platform(1050, 300, 100, 20, color),
            Platform(1200, 420, 80, 20, color),
            Platform(1350, 540, 200, 60, color),
            Platform(1500, 400, 100, 20, color),
            Platform(1700, 540, 800, 60, color),  # Boss arena
        ]
        enemies = [
            Wasp(100, 540 - 24, 50, 250),
            Spider(450, 350 - 28, 400, 530),
            Fly(600, 380, 550, 750),
            Wasp(750, 540 - 24, 700, 830),
            Spider(950, 380 - 28, 900, 1050),
            Fly(1100, 250, 1050, 1250),
            Wasp(1400, 540 - 24, 1350, 1530),
        ]
    else:
        platforms = []
        enemies = []

    return platforms, enemies


def check_level_complete(player, enemies):
    """Check if all enemies are dead and player reached end of level."""
    all_dead = all(not e.alive and e.death_timer <= 0 for e in enemies)
    # Player past the rightmost reasonable point
    past_end = player.rect.x > 1900
    return all_dead and past_end


def draw_hud(screen, player, level_name):
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


def handle_combat(player, enemies, boss=None):
    hit_events = []

    # Player attack hits enemies
    if player.attacking and player.attack_rect:
        for enemy in enemies:
            if enemy.alive and player.attack_rect.colliderect(enemy.rect):
                enemy.take_damage(1)
                if not enemy.alive:
                    hit_events.append("enemy_die")
                else:
                    hit_events.append("hit_enemy")
        # Player attack hits boss
        if boss and boss.alive and player.attack_rect.colliderect(boss.rect):
            boss.take_damage(1)
            if not boss.alive:
                hit_events.append("boss_die")
            else:
                hit_events.append("hit_enemy")

    # Enemies damage player on contact
    for enemy in enemies:
        if enemy.alive and player.rect.colliderect(enemy.rect):
            if player.take_damage(1):
                # Knockback: push player away from enemy
                if player.rect.centerx < enemy.rect.centerx:
                    player.rect.x -= 30
                else:
                    player.rect.x += 30
                player.vel_y = -8  # Small bounce up
                hit_events.append("player_hurt")

    # Boss damages player
    if boss and boss.alive:
        if player.rect.colliderect(boss.rect):
            if player.take_damage(1):
                if player.rect.centerx < boss.rect.centerx:
                    player.rect.x -= 40
                else:
                    player.rect.x += 40
                player.vel_y = -10
                hit_events.append("player_hurt")
        # Shockwave damages player
        if boss.shockwave and boss.shockwave_timer > 0:
            if player.rect.colliderect(boss.shockwave):
                if player.take_damage(1):
                    player.vel_y = -12
                    hit_events.append("player_hurt")

    return hit_events


def draw_boss_hp(screen, boss):
    bar_width = 300
    bar_x = SCREEN_WIDTH // 2 - bar_width // 2
    pygame.draw.rect(screen, (80, 80, 80), (bar_x - 2, 10, bar_width + 4, 22))
    hp_width = int(bar_width * boss.hp / boss.max_hp)
    pygame.draw.rect(screen, ORANGE, (bar_x, 12, hp_width, 18))
    font = pygame.font.Font(None, 24)
    label = font.render("WASP KING", True, WHITE)
    screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 36))


def main():
    pygame.init()
    pygame.mixer.init()

    # Load sound effects
    sound_dir = os.path.join("assets", "sounds")
    sounds = {}
    sound_names = [
        "jump", "hover", "attack", "hit_enemy", "player_hurt",
        "enemy_die", "boss_charge", "boss_slam", "boss_die", "level_complete"
    ]
    for name in sound_names:
        path = os.path.join(sound_dir, f"{name}.wav")
        if os.path.exists(path):
            sounds[name] = pygame.mixer.Sound(path)
            sounds[name].set_volume(0.5)
    # Hover sound needs to loop, set it quieter
    if "hover" in sounds:
        sounds["hover"].set_volume(0.3)

    def play_music(track_name):
        """Load and play background music on loop."""
        path = os.path.join(sound_dir, f"{track_name}.wav")
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # -1 = loop forever

    def stop_music():
        pygame.mixer.music.stop()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    game_state = STATE_TITLE
    current_level = 0

    # Initialize game objects (will be reset when starting/restarting)
    platforms = []
    enemies = []
    player = None
    camera = None
    boss = None
    bg = None

    def start_level():
        nonlocal platforms, enemies, player, camera, boss, bg, prev_boss_state, boss_music_started
        platforms, enemies = create_level(current_level)
        player = Player(50, 400)
        player.hp = PLAYER_MAX_HP
        camera = Camera()
        bg = ParallaxBackground(current_level)
        # Spawn boss on level 3 (index 2)
        if current_level == 2:
            boss = WaspKing(2000, 540 - 90)  # In the boss arena
        else:
            boss = None
        prev_boss_state = "idle"
        boss_music_started = False

    hover_channel = None
    prev_boss_state = "idle"
    boss_music_started = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_state == STATE_TITLE:
                        current_level = 0
                        start_level()
                        game_state = STATE_PLAYING
                        play_music("level_music")
                    elif game_state == STATE_GAME_OVER:
                        start_level()
                        game_state = STATE_PLAYING
                        play_music("level_music")
                    elif game_state == STATE_LEVEL_TRANSITION:
                        start_level()
                        game_state = STATE_PLAYING
                        play_music("level_music")
                    elif game_state == STATE_VICTORY:
                        current_level = 0
                        game_state = STATE_TITLE
                if event.key in (pygame.K_z, pygame.K_x) and game_state == STATE_PLAYING:
                    player.start_attack()
                    if "attack" in sounds:
                        sounds["attack"].play()

        if game_state == STATE_PLAYING:
            keys = pygame.key.get_pressed()
            player.update(keys, platforms)

            # Jump sound — fires the frame the player leaves the ground
            if player.just_jumped and "jump" in sounds:
                sounds["jump"].play()

            # Hover sound — loop while hovering, stop when done
            if player.is_hovering and "hover" in sounds:
                if hover_channel is None or not hover_channel.get_busy():
                    hover_channel = sounds["hover"].play(-1)
            else:
                if hover_channel and hover_channel.get_busy():
                    hover_channel.stop()
                    hover_channel = None

            for enemy in enemies:
                if isinstance(enemy, Spider):
                    enemy.update(player.rect.centerx)
                else:
                    enemy.update()
            if boss and boss.alive:
                boss.update(player, platforms)
                # Boss attack sounds
                if boss.state != prev_boss_state:
                    if boss.state == "charge" and "boss_charge" in sounds:
                        sounds["boss_charge"].play()
                    elif boss.state == "slam" and "boss_slam" in sounds:
                        sounds["boss_slam"].play()
                    prev_boss_state = boss.state
                # Add summoned flies to enemy list
                if boss.summoned_flies:
                    enemies.extend(boss.summoned_flies)
                    boss.summoned_flies = []
            # Switch to boss music when entering arena on level 3
            if current_level == 2 and boss and boss.alive and not boss_music_started:
                if player.rect.x > 1700:
                    play_music("boss_music")
                    boss_music_started = True

            combat_events = handle_combat(player, enemies, boss)
            for evt in combat_events:
                if evt in sounds:
                    sounds[evt].play()
            camera.update(player)

            # Check for death
            if player.hp <= 0:
                game_state = STATE_GAME_OVER
                stop_music()
                if hover_channel and hover_channel.get_busy():
                    hover_channel.stop()
                    hover_channel = None

            # Check for level complete or boss defeat
            if current_level == 2 and boss and not boss.alive:
                game_state = STATE_VICTORY
                stop_music()
                if hover_channel and hover_channel.get_busy():
                    hover_channel.stop()
                    hover_channel = None
            elif current_level < 2 and check_level_complete(player, enemies):
                current_level += 1
                game_state = STATE_LEVEL_TRANSITION
                stop_music()
                if "level_complete" in sounds:
                    sounds["level_complete"].play()

        # Drawing
        if game_state == STATE_TITLE:
            draw_title_screen(screen)
        elif game_state == STATE_PLAYING:
            time_ms = pygame.time.get_ticks()
            if bg:
                bg.draw(screen, camera.x)
            else:
                screen.fill(LEVEL_THEMES[current_level]["bg"])
            for p in platforms:
                p.draw(screen, camera.x, time_ms)
            for enemy in enemies:
                enemy.draw(screen, camera.x)
            if boss and boss.alive:
                boss.draw(screen, camera.x)
            player.draw(screen, camera.x)
            draw_hud(screen, player, LEVEL_THEMES[current_level]["name"])
            if boss and boss.alive:
                draw_boss_hp(screen, boss)
        elif game_state == STATE_GAME_OVER:
            draw_game_over(screen)
        elif game_state == STATE_LEVEL_TRANSITION:
            draw_transition(screen, LEVEL_THEMES[current_level]["name"])
        elif game_state == STATE_VICTORY:
            draw_victory(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
