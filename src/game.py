import pygame
import os
import sys
from src.settings import *
from src.entities.player import Player
from src.entities.enemies import Wasp, Fly, Spider
from src.entities.bosses import WaspKing
from src.world.levels import create_level, check_level_complete
from src.world.camera import Camera, ParallaxBackground
from src.systems.combat import handle_combat
from src.ui.hud import draw_hud, draw_boss_hp
from src.ui.menus import draw_title_screen, draw_game_over, draw_transition, draw_victory


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
