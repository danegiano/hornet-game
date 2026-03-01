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
GROUND_Y = SCREEN_HEIGHT - 60  # Temporary ground line

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

    def update(self, keys):
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

        # --- Temporary ground collision ---
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y  # Snap the player back to the ground
            self.vel_y = 0               # Stop falling
            self.on_ground = True
            self.hover_fuel = HOVER_MAX  # Refill hover fuel on landing
        else:
            self.on_ground = False

    def draw(self, screen):
        # Draw the yellow body rectangle
        pygame.draw.rect(screen, YELLOW, self.rect)

        # Draw a darker border around the body so it looks cleaner
        pygame.draw.rect(screen, DARK_YELLOW, self.rect, 2)

        # --- Stinger triangle ---
        # The stinger pokes out from the front of the hornet
        # It's a small triangle made of 3 points (a polygon)

        if self.facing_right:
            # Stinger points to the right
            tip_x = self.rect.right + 10          # The pointy tip
            mid_y = self.rect.centery             # Vertically centered
            stinger_points = [
                (self.rect.right, mid_y - 5),     # Top-left corner of triangle
                (self.rect.right, mid_y + 5),     # Bottom-left corner of triangle
                (tip_x, mid_y),                   # The sharp tip
            ]
        else:
            # Stinger points to the left
            tip_x = self.rect.left - 10           # The pointy tip
            mid_y = self.rect.centery
            stinger_points = [
                (self.rect.left, mid_y - 5),      # Top-right corner of triangle
                (self.rect.left, mid_y + 5),      # Bottom-right corner of triangle
                (tip_x, mid_y),                   # The sharp tip
            ]

        pygame.draw.polygon(screen, DARK_YELLOW, stinger_points)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Create the player, positioned just above the ground
    player = Player(100, GROUND_Y - PLAYER_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Read which keys are currently held down
        keys = pygame.key.get_pressed()

        # Update the player (movement, gravity, collisions)
        player.update(keys)

        # --- Drawing ---
        # Light blue sky background
        screen.fill((135, 200, 235))

        # Temporary green ground
        pygame.draw.rect(
            screen,
            (100, 180, 100),
            (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y)
        )

        # Draw the player on top of everything
        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
