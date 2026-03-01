import pygame
from src.settings import *


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
