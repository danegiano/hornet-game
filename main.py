import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "HORNET"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player constants
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 30
PLAYER_SPEED = 5
GRAVITY = 0.8
JUMP_POWER = -15

HOVER_MAX = 60        # Frames of hover time (~1 second at 60fps)
HOVER_GRAVITY = 0.15  # Much slower fall while hovering

ATTACK_RANGE = 50
ATTACK_WIDTH = 10
ATTACK_DURATION = 10   # Frames the attack hitbox is active
ATTACK_COOLDOWN = 20   # Frames before you can attack again

PLAYER_MAX_HP = 5
INVINCIBILITY_FRAMES = 60  # 1 second of invincibility after hit

YELLOW = (255, 220, 50)
DARK_YELLOW = (200, 170, 0)


class Player:
    def __init__(self, x, y):
        # rect is the rectangle that represents the player's body
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        # vel_y is vertical velocity — positive = falling, negative = rising
        self.vel_y = 0
        # on_ground tracks whether the player is standing on the ground
        self.on_ground = False
        # facing_right tracks which way the player is looking
        self.facing_right = True
        # hover_fuel is how many frames of hover the player has left
        self.hover_fuel = HOVER_MAX
        # is_hovering is True while the player is actively slowing their fall
        self.is_hovering = False
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.attack_rect = None
        self.hp = PLAYER_MAX_HP
        self.invincible_timer = 0

    def update(self, keys, platforms):
        # Invincibility timer
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        # --- Horizontal movement ---
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
            self.facing_right = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
            self.facing_right = False

        # --- Jump ---
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_POWER  # A negative value shoots the player upward
            self.on_ground = False

        # --- Hover (hold space while in the air) ---
        # All four conditions must be true to hover:
        #   1. Holding space
        #   2. Not on the ground (in the air)
        #   3. Have hover fuel left
        #   4. Falling (vel_y > 0) — hover doesn't activate on the way up
        if keys[pygame.K_SPACE] and not self.on_ground and self.hover_fuel > 0 and self.vel_y > 0:
            self.is_hovering = True
            self.hover_fuel -= 1         # Drain 1 frame of fuel
            self.vel_y += HOVER_GRAVITY  # Slow fall instead of normal gravity
        else:
            self.is_hovering = False
            self.vel_y += GRAVITY        # Normal gravity applies

        self.rect.y += self.vel_y

        # --- Platform collision (vertical) ---
        # Reset on_ground each frame — we'll set it back to True if we land
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down onto the platform
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.hover_fuel = HOVER_MAX  # Refill hover fuel on landing
                elif self.vel_y < 0:  # Jumping up into the bottom of a platform
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Attack cooldown — counts down every frame until you can attack again
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Attack timer — counts down while the hitbox is active
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
                self.attack_rect = None

        # Keep the attack hitbox glued to the player while attacking
        if self.attacking and self.attack_rect:
            if self.facing_right:
                self.attack_rect.x = self.rect.right
                self.attack_rect.y = self.rect.top - 5
            else:
                self.attack_rect.x = self.rect.left - ATTACK_RANGE
                self.attack_rect.y = self.rect.top - 5

    def take_damage(self, amount):
        if self.invincible_timer <= 0:
            self.hp -= amount
            self.invincible_timer = INVINCIBILITY_FRAMES
            return True
        return False

    def start_attack(self):
        # Only start a new attack if we're not already attacking and cooldown is done
        if self.attack_cooldown <= 0 and not self.attacking:
            self.attacking = True
            self.attack_timer = ATTACK_DURATION
            self.attack_cooldown = ATTACK_COOLDOWN
            # Create a hitbox rectangle in front of the player
            if self.facing_right:
                self.attack_rect = pygame.Rect(
                    self.rect.right, self.rect.top - 5,
                    ATTACK_RANGE, self.rect.height + 10
                )
            else:
                self.attack_rect = pygame.Rect(
                    self.rect.left - ATTACK_RANGE, self.rect.top - 5,
                    ATTACK_RANGE, self.rect.height + 10
                )

    def draw(self, screen, camera_x):
        # Flash when invincible (skip drawing every other frame)
        if self.invincible_timer > 0 and self.invincible_timer % 4 < 2:
            return

        # Shift the player's draw position left by camera_x so it moves with the world
        draw_rect = self.rect.move(-camera_x, 0)

        # Draw the yellow body rectangle
        pygame.draw.rect(screen, YELLOW, draw_rect)

        # Draw a darker border around the body so it looks cleaner
        pygame.draw.rect(screen, DARK_YELLOW, draw_rect, 2)

        # --- Stinger triangle ---
        # The stinger pokes out from the front of the hornet
        # It's a small triangle made of 3 points (a polygon)
        # We use draw_rect positions (not self.rect) so the stinger scrolls too

        if self.facing_right:
            # Stinger points to the right
            tip_x = draw_rect.right + 8
            base_top = (draw_rect.right, draw_rect.centery - 4)
            base_bot = (draw_rect.right, draw_rect.centery + 4)
        else:
            # Stinger points to the left
            tip_x = draw_rect.left - 8
            base_top = (draw_rect.left, draw_rect.centery - 4)
            base_bot = (draw_rect.left, draw_rect.centery + 4)

        tip = (tip_x, draw_rect.centery)
        pygame.draw.polygon(screen, DARK_YELLOW, [tip, base_top, base_bot])

        # --- Attack visual ---
        # When attacking, show a semi-transparent yellow flash where the hitbox is
        if self.attacking and self.attack_rect:
            atk_draw = self.attack_rect.move(-camera_x, 0)
            # SRCALPHA means the surface supports transparency
            attack_surface = pygame.Surface((atk_draw.width, atk_draw.height), pygame.SRCALPHA)
            attack_surface.fill((255, 255, 200, 120))  # Semi-transparent yellow
            screen.blit(attack_surface, atk_draw)


class Camera:
    def __init__(self):
        self.x = 0

    def update(self, player):
        # Camera follows player, keeping them in the left third of the screen
        target_x = player.rect.centerx - SCREEN_WIDTH // 3
        self.x += (target_x - self.x) * 0.1  # Smooth follow (lerp)
        if self.x < 0:
            self.x = 0  # Don't scroll left past the start of the world


class Platform:
    def __init__(self, x, y, width, height, color=(100, 180, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, camera_x):
        # Shift the platform left by camera_x so it scrolls with the world
        draw_rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(screen, self.color, draw_rect)


RED = (200, 50, 50)

class Enemy:
    def __init__(self, x, y, width, height, hp, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.hp = hp
        self.color = color
        self.alive = True
        self.death_timer = 0  # Flash timer when killed

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            self.death_timer = 15  # Brief flash before disappearing

    def draw(self, screen, camera_x):
        if not self.alive:
            if self.death_timer > 0:
                # Flash white when dying
                draw_rect = self.rect.move(-camera_x, 0)
                pygame.draw.rect(screen, WHITE, draw_rect)
            return
        draw_rect = self.rect.move(-camera_x, 0)
        pygame.draw.rect(screen, self.color, draw_rect)

class Beetle(Enemy):
    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__(x, y, 36, 24, 2, RED)
        self.speed = 1.5
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.moving_right = True

    def update(self):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        if self.moving_right:
            self.rect.x += self.speed
            if self.rect.right >= self.patrol_right:
                self.moving_right = False
        else:
            self.rect.x -= self.speed
            if self.rect.left <= self.patrol_left:
                self.moving_right = True


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


def handle_combat(player, enemies):
    # Player attack hits enemies
    if player.attacking and player.attack_rect:
        for enemy in enemies:
            if enemy.alive and player.attack_rect.colliderect(enemy.rect):
                enemy.take_damage(1)

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


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Platform list — the ground is just a very wide platform at the bottom
    platforms = [
        Platform(0, SCREEN_HEIGHT - 60, 2000, 60),   # Long ground
        Platform(300, 420, 150, 20),                   # Floating platform
        Platform(550, 340, 150, 20),                   # Higher platform
        Platform(800, 400, 200, 20),                   # Another platform
    ]

    enemies = [
        Beetle(400, SCREEN_HEIGHT - 60 - 24, 350, 550),
        Beetle(700, SCREEN_HEIGHT - 60 - 24, 650, 900),
    ]

    # Create the player, positioned just above the ground platform
    player = Player(100, SCREEN_HEIGHT - 60 - PLAYER_HEIGHT)

    # Create the camera — it will follow the player smoothly
    camera = Camera()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_z, pygame.K_x):
                    player.start_attack()

        # Read which keys are currently held down
        keys = pygame.key.get_pressed()

        # Update the player (movement, gravity, collisions)
        player.update(keys, platforms)

        # Update the camera to follow the player
        camera.update(player)

        # Update all enemies (movement, death timer)
        for enemy in enemies:
            enemy.update()

        # Check for combat hits between player and enemies
        handle_combat(player, enemies)

        # --- Drawing ---
        # Light blue sky background
        screen.fill((135, 200, 235))

        # Draw all platforms, offset by the camera position
        for p in platforms:
            p.draw(screen, camera.x)

        # Draw enemies on top of platforms, below the player
        for enemy in enemies:
            enemy.draw(screen, camera.x)

        # Draw the player on top of everything, also offset by camera
        player.draw(screen, camera.x)

        draw_hud(screen, player, "Level 1: The Garden")

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
