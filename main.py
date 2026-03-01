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

    def update(self, keys, platforms):
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

    def draw(self, screen, camera_x):
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

    # Create the player, positioned just above the ground platform
    player = Player(100, SCREEN_HEIGHT - 60 - PLAYER_HEIGHT)

    # Create the camera — it will follow the player smoothly
    camera = Camera()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Read which keys are currently held down
        keys = pygame.key.get_pressed()

        # Update the player (movement, gravity, collisions)
        player.update(keys, platforms)

        # Update the camera to follow the player
        camera.update(player)

        # --- Drawing ---
        # Light blue sky background
        screen.fill((135, 200, 235))

        # Draw all platforms, offset by the camera position
        for p in platforms:
            p.draw(screen, camera.x)

        # Draw the player on top of everything, also offset by camera
        player.draw(screen, camera.x)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
