import pygame
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # Constants
    WIDTH, HEIGHT = 640, 480
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
    BALL_SIZE = 15
    PADDLE_SPEED = 10


# Initialize Pygame
def init_pygame():
    pygame.init()


def setup_display():
    # Set up the display
    screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    pygame.display.set_caption("Pong Game")
    return screen


# Create initial ball and players positions
def create_ball_and_players():
    left_paddle = pygame.Rect(
        30,
        (Settings.HEIGHT - Settings.PADDLE_HEIGHT) // 2,
        Settings.PADDLE_WIDTH,
        Settings.PADDLE_HEIGHT,
    )
    right_paddle = pygame.Rect(
        Settings.WIDTH - 40,
        (Settings.HEIGHT - Settings.PADDLE_HEIGHT) // 2,
        Settings.PADDLE_WIDTH,
        Settings.PADDLE_HEIGHT,
    )
    ball = pygame.Rect(
        Settings.WIDTH // 2,
        Settings.HEIGHT // 2,
        Settings.BALL_SIZE,
        Settings.BALL_SIZE,
    )

    return left_paddle, right_paddle, ball


def get_keys():
    return pygame.key.get_pressed()


# Function to handle player movement
def player_movement(left_paddle, right_paddle):

    keys = get_keys()

    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= Settings.PADDLE_SPEED

    elif keys[pygame.K_s] and left_paddle.bottom < Settings.HEIGHT:
        left_paddle.y += Settings.PADDLE_SPEED

    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= Settings.PADDLE_SPEED

    elif keys[pygame.K_DOWN] and right_paddle.bottom < Settings.HEIGHT:
        right_paddle.y += Settings.PADDLE_SPEED


def set_ball_speed():
    ball_speed_x, ball_speed_y = 10, 10
    return ball_speed_x, ball_speed_y


# Function to draw objects on screen
def draw_screen(left_paddle, right_paddle, ball, screen):
    screen.fill(Settings.BLACK)
    pygame.draw.rect(screen, Settings.WHITE, left_paddle)
    pygame.draw.rect(screen, Settings.WHITE, right_paddle)
    pygame.draw.ellipse(screen, Settings.WHITE, ball)
    pygame.display.flip()
    pygame.time.delay(16)


# Main game loop
def main():
    init_pygame()
    screen = setup_display()

    left_paddle, right_paddle, ball = create_ball_and_players()
    ball_speed_x, ball_speed_y = set_ball_speed()  # Initial ball speeds
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        player_movement(left_paddle, right_paddle)

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= Settings.HEIGHT:
            ball_speed_y = -ball_speed_y

        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x = -ball_speed_x

        if ball.left <= 0 or ball.right >= Settings.WIDTH:
            ball_speed_x = -ball_speed_x
            ball.x = Settings.WIDTH // 2
            ball.y = Settings.HEIGHT // 2

        draw_screen(left_paddle, right_paddle, ball, screen)


if __name__ == "__main__":
    main()
