import pygame
import os
import sys
from src.settings import *
from src.entities.player import Player
from src.entities.enemies import Wasp, Fly, Spider
from src.entities.bosses import WaspKing, SwampBeetleLord, CrystalSpiderQueen, FireMoth
from src.world.levels import create_level, check_level_complete
from src.world.camera import Camera, ParallaxBackground
from src.systems.combat import handle_combat
from src.systems.coins import CoinManager
from src.systems.powers import ISLAND_POWER
from src.save_data import SaveData
from src.ui.hud import draw_hud, draw_boss_hp
from src.ui.menus import draw_title_screen, draw_game_over, draw_transition, draw_victory
from src.ui.island_map import IslandMap
from src.ui.shop import Shop


def apply_powers(player, save_data):
    """Apply unlocked powers to the player based on save data."""
    player.has_double_jump = save_data.has_power("double_jump")
    player.has_dash = save_data.has_power("dash")
    player.has_wall_climb = save_data.has_power("wall_climb")
    if save_data.has_power("shield"):
        player.has_shield = True
        player.shield_active = True
    if save_data.has_power("stinger_upgrade"):
        player.stinger_damage = 2
    # Set HP based on upgrades the player has bought
    player.hp = save_data.get_max_hp()


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

    # Island map tracking
    current_island = 0
    current_level_in_island = 0
    island_map = None
    shop = None

    # Initialize game objects (will be reset when starting/restarting)
    platforms = []
    enemies = []
    player = None
    camera = None
    boss = None
    bg = None
    save_data = SaveData()
    coin_manager = CoinManager()

    def start_level():
        nonlocal platforms, enemies, player, camera, boss, bg, prev_boss_state, boss_music_started, coin_manager
        coin_manager = CoinManager()

        island_info = ISLAND_DATA[current_island]
        is_boss_level = (current_level_in_island == island_info["levels"] - 1)

        # Use the new (island, level) system
        platforms, enemies = create_level(current_island, current_level_in_island)
        player = Player(50, 400)
        apply_powers(player, save_data)  # Give the player any powers they've unlocked
        camera = Camera()

        # Pick the right background theme
        if current_island == 0:
            bg = ParallaxBackground(current_level_in_island)
        elif current_island == 1:
            bg = ParallaxBackground("swamp")
        elif current_island == 2:
            bg = ParallaxBackground("cave")
        elif current_island == 3:
            bg = ParallaxBackground("volcano")
        else:
            bg = ParallaxBackground(current_level_in_island % 3)

        # Spawn boss on the LAST level of each island
        if is_boss_level:
            if current_island == 0:
                boss = WaspKing(2000, 540 - 90)
            elif current_island == 1:
                boss = SwampBeetleLord(2000, 540 - 80)
            elif current_island == 2:
                boss = CrystalSpiderQueen(2100, 350)  # Floats in the arena
            elif current_island == 3:
                boss = FireMoth(2500, 300)  # Flies around the volcano arena
            else:
                boss = WaspKing(2000, 540 - 90)  # Placeholder for future islands
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
            # Island map gets events first (it handles its own keys)
            if game_state == STATE_ISLAND_MAP and island_map:
                result = island_map.handle_input(event)
                if result is not None:
                    if isinstance(result, tuple) and result[0] == "play":
                        current_island = result[1]
                        current_level_in_island = 0
                        start_level()
                        game_state = STATE_PLAYING
                        play_music("level_music")
                    elif result == "shop":
                        shop = Shop(save_data)
                        game_state = "shop"

            if game_state == "shop" and shop:
                result = shop.handle_input(event)
                if result == "close":
                    island_map = IslandMap(save_data)
                    game_state = STATE_ISLAND_MAP

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_state == STATE_TITLE:
                        # Title -> Island Map
                        island_map = IslandMap(save_data)
                        game_state = STATE_ISLAND_MAP
                    elif game_state == STATE_GAME_OVER:
                        # Death -> back to island map (keep coins)
                        island_map = IslandMap(save_data)
                        game_state = STATE_ISLAND_MAP
                    elif game_state == STATE_LEVEL_TRANSITION:
                        start_level()
                        game_state = STATE_PLAYING
                        play_music("level_music")
                    elif game_state == STATE_VICTORY:
                        # Victory -> back to island map
                        island_map = IslandMap(save_data)
                        game_state = STATE_ISLAND_MAP
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
                    if boss.state in ("charge", "flame_dash") and "boss_charge" in sounds:
                        sounds["boss_charge"].play()
                    elif boss.state in ("slam", "stomp", "ceiling_drop", "fireball_rain") and "boss_slam" in sounds:
                        sounds["boss_slam"].play()
                    prev_boss_state = boss.state
                # Add summoned flies/spiders to enemy list
                if boss.summoned_flies:
                    enemies.extend(boss.summoned_flies)
                    boss.summoned_flies = []
                # Crystal Spider Queen projectile + web trap handling
                if hasattr(boss, 'projectiles'):
                    for proj in boss.projectiles:
                        if player.rect.colliderect(proj["rect"]):
                            if player.take_damage(1):
                                player.vel_y = -8
                            if proj in boss.projectiles:
                                boss.projectiles.remove(proj)
                if hasattr(boss, 'web_traps'):
                    for trap in boss.web_traps:
                        if player.rect.colliderect(trap["rect"]):
                            # Slow the player temporarily (halve speed this frame)
                            player.rect.x -= (player.rect.x - player.rect.x) * 0
                            # Apply movement penalty by pulling player back
                            keys_now = pygame.key.get_pressed()
                            if keys_now[pygame.K_LEFT] or keys_now[pygame.K_a]:
                                player.rect.x += 2  # Counter half the movement
                            if keys_now[pygame.K_RIGHT] or keys_now[pygame.K_d]:
                                player.rect.x -= 2  # Counter half the movement
                # Fire Moth — burning patches, fire trail, and flame wall damage
                if hasattr(boss, 'get_all_damage_rects'):
                    for fire_rect in boss.get_all_damage_rects():
                        if player.rect.colliderect(fire_rect):
                            if player.take_damage(1):
                                player.vel_y = -8
                            break  # Only take one hit per frame from fire

            # Switch to boss music when entering boss arena
            if boss and boss.alive and not boss_music_started:
                if player.rect.x > 1700:
                    play_music("boss_music")
                    boss_music_started = True

            combat_events, death_positions = handle_combat(player, enemies, boss)
            for evt in combat_events:
                if evt in sounds:
                    sounds[evt].play()
            # Spawn coins where enemies died
            for dx, dy, count in death_positions:
                coin_manager.spawn(dx, dy, count)
            # Update coins and collect any that reached the player
            collected = coin_manager.update(player.rect)
            if collected > 0:
                save_data.add_coins(collected)
            camera.update(player)

            # Check for death
            if player.hp <= 0:
                game_state = STATE_GAME_OVER
                stop_music()
                if hover_channel and hover_channel.get_busy():
                    hover_channel.stop()
                    hover_channel = None

            # Check for level complete or boss defeat
            island_info = ISLAND_DATA[current_island]
            is_boss_level = (current_level_in_island == island_info["levels"] - 1)

            if is_boss_level and boss and not boss.alive:
                # Boss defeated! Save progress, grant power, unlock next island
                save_data.complete_level(current_island, current_level_in_island)
                power = ISLAND_POWER.get(current_island)
                if power:
                    save_data.unlock_power(power)
                save_data.max_island_unlocked = min(current_island + 1, 4)
                save_data.save()
                game_state = STATE_VICTORY
                stop_music()
                if hover_channel and hover_channel.get_busy():
                    hover_channel.stop()
                    hover_channel = None
            elif not is_boss_level and check_level_complete(player, enemies, current_island, current_level_in_island):
                # Non-boss level complete — advance to next level in this island
                save_data.complete_level(current_island, current_level_in_island)
                save_data.save()
                current_level_in_island += 1
                game_state = STATE_LEVEL_TRANSITION
                stop_music()
                if "level_complete" in sounds:
                    sounds["level_complete"].play()

        # Drawing
        if game_state == STATE_TITLE:
            draw_title_screen(screen)
        elif game_state == STATE_PLAYING:
            time_ms = pygame.time.get_ticks()
            # Get the current theme from the new nested dict
            cur_theme = LEVEL_THEMES.get(current_island, LEVEL_THEMES[0])
            if current_level_in_island < len(cur_theme):
                theme_entry = cur_theme[current_level_in_island]
            else:
                theme_entry = cur_theme[0]

            if bg:
                bg.draw(screen, camera.x)
            else:
                screen.fill(theme_entry["bg"])
            for p in platforms:
                p.draw(screen, camera.x, time_ms)
            for enemy in enemies:
                enemy.draw(screen, camera.x)
            if boss and boss.alive:
                boss.draw(screen, camera.x)
            coin_manager.draw(screen, camera.x)
            player.draw(screen, camera.x)
            draw_hud(screen, player, theme_entry["name"], save_data.coins)
            if boss and boss.alive:
                draw_boss_hp(screen, boss)
        elif game_state == STATE_ISLAND_MAP:
            island_map.draw(screen)
        elif game_state == "shop":
            shop.draw(screen)
        elif game_state == STATE_GAME_OVER:
            draw_game_over(screen)
        elif game_state == STATE_LEVEL_TRANSITION:
            # Look up the NEXT level's name for the transition screen
            next_theme = LEVEL_THEMES.get(current_island, LEVEL_THEMES[0])
            if current_level_in_island < len(next_theme):
                next_name = next_theme[current_level_in_island]["name"]
            else:
                next_name = next_theme[0]["name"]
            draw_transition(screen, next_name)
        elif game_state == STATE_VICTORY:
            draw_victory(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
