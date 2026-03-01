import pygame
from src.settings import *


def handle_combat(player, enemies, boss=None):
    hit_events = []
    death_positions = []  # (x, y, coin_count) for each enemy that dies

    # Player attack hits enemies
    # Use stinger_damage from player (defaults to 1, becomes 2 with stinger upgrade)
    damage = getattr(player, 'stinger_damage', 1)
    if player.attacking and player.attack_rect:
        for enemy in enemies:
            if enemy.alive and player.attack_rect.colliderect(enemy.rect):
                enemy.take_damage(damage)
                if not enemy.alive:
                    hit_events.append("enemy_die")
                    death_positions.append((enemy.rect.centerx, enemy.rect.y, 2))
                else:
                    hit_events.append("hit_enemy")
        # Player attack hits boss (skip if boss is invisible during teleport)
        boss_visible = getattr(boss, 'teleport_visible', True)
        if boss and boss.alive and boss_visible and player.attack_rect.colliderect(boss.rect):
            boss.take_damage(damage)
            if not boss.alive:
                hit_events.append("boss_die")
                death_positions.append((boss.rect.centerx, boss.rect.y, 5))
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
                # Poison trait — apply poison on contact damage
                if hasattr(enemy, 'has_trait') and enemy.has_trait("poison"):
                    player.apply_poison()

    # Enemy projectiles damage player
    for enemy in enemies:
        if not enemy.alive:
            continue
        for proj in getattr(enemy, 'projectiles', [])[:]:
            if player.rect.colliderect(proj["rect"]):
                hit = player.take_damage(1)
                if hit:
                    player.vel_y = -6
                    hit_events.append("player_hurt")
                    # Poison on projectile hit too
                    if hasattr(enemy, 'has_trait') and enemy.has_trait("poison"):
                        player.apply_poison()
                enemy.projectiles.remove(proj)

    # Boss damages player (skip if boss is invisible during teleport)
    boss_visible = getattr(boss, 'teleport_visible', True) if boss else True
    if boss and boss.alive and boss_visible:
        if player.rect.colliderect(boss.rect):
            if player.take_damage(1):
                if player.rect.centerx < boss.rect.centerx:
                    player.rect.x -= 40
                else:
                    player.rect.x += 40
                player.vel_y = -10
                hit_events.append("player_hurt")
        # Shockwave damages player (supports single or dual shockwaves)
        shockwave_hit = False
        if boss.shockwave and boss.shockwave_timer > 0:
            if player.rect.colliderect(boss.shockwave):
                shockwave_hit = True
        # Check left/right shockwaves (SwampBeetleLord uses these)
        if hasattr(boss, 'shockwave_left') and boss.shockwave_left and boss.shockwave_timer > 0:
            if player.rect.colliderect(boss.shockwave_left):
                shockwave_hit = True
        if hasattr(boss, 'shockwave_right') and boss.shockwave_right and boss.shockwave_timer > 0:
            if player.rect.colliderect(boss.shockwave_right):
                shockwave_hit = True
        if shockwave_hit:
            if player.take_damage(1):
                player.vel_y = -12
                hit_events.append("player_hurt")

    return hit_events, death_positions
