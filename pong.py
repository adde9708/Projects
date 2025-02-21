import pygame
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    WIDTH, HEIGHT = 640, 480


@dataclass(frozen=True)
class Players:
    PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
    PADDLE_SPEED = 500


@dataclass(frozen=True)
class Ball:
    BALL_SIZE = 15


@dataclass(frozen=True)
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


# Initialize Pygame
def init_pygame():
    pygame.init()


def setup_display():
    # Set up the display
    screen = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT))
    pygame.display.set_caption("Pong Game")
    return screen


# Create initial ball and players positions
def create_ball_and_players():
    left_paddle = pygame.Rect(
        30,
        (Window.HEIGHT - Players.PADDLE_HEIGHT) // 2,
        Players.PADDLE_WIDTH,
        Players.PADDLE_HEIGHT,
    )
    right_paddle = pygame.Rect(
        Window.WIDTH - 40,
        (Window.HEIGHT - Players.PADDLE_HEIGHT) // 2,
        Players.PADDLE_WIDTH,
        Players.PADDLE_HEIGHT,
    )
    ball = pygame.Rect(
        Window.WIDTH // 2,
        Window.HEIGHT // 2,
        Ball.BALL_SIZE,
        Ball.BALL_SIZE,
    )

    return left_paddle, right_paddle, ball


# Function to handle player movement
def player_movement(left_paddle, right_paddle, delta_time):

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= Players.PADDLE_SPEED * delta_time

    elif keys[pygame.K_s] and left_paddle.bottom < Window.HEIGHT:
        left_paddle.y += Players.PADDLE_SPEED * delta_time

    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= Players.PADDLE_SPEED * delta_time

    elif keys[pygame.K_DOWN] and right_paddle.bottom < Window.HEIGHT:
        right_paddle.y += Players.PADDLE_SPEED * delta_time


def set_ball_speed():
    ball_speed_x, ball_speed_y = 500, 500
    return ball_speed_x, ball_speed_y


# Function to draw objects on screen
def draw_screen(left_paddle, right_paddle, ball, screen):
    screen.fill(Colors.BLACK)
    pygame.draw.rect(screen, Colors.WHITE, left_paddle)
    pygame.draw.rect(screen, Colors.WHITE, right_paddle)
    pygame.draw.ellipse(screen, Colors.WHITE, ball)
    pygame.display.flip()


# Main game loop
def main():
    init_pygame()
    screen = setup_display()
    clock = pygame.time.Clock()
    # Initial ball speeds
    ball_speed_x, ball_speed_y = set_ball_speed() 
    # Create players and ball
    left_paddle, right_paddle, ball = create_ball_and_players()

    while True:
        delta_time = clock.tick_busy_loop(240) / 1024
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        player_movement(left_paddle, right_paddle, delta_time)

        ball.x += ball_speed_x * delta_time
        ball.y += ball_speed_y * delta_time

        if ball.top <= 0 or ball.bottom >= Window.HEIGHT:
            ball_speed_y = -ball_speed_y

        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x = -ball_speed_x

        if ball.left <= 0 or ball.right >= Window.WIDTH:
            ball_speed_x = -ball_speed_x
            ball.x = Window.WIDTH // 2
            ball.y = Window.HEIGHT // 2

        draw_screen(left_paddle, right_paddle, ball, screen)


if __name__ == "__main__":
    main()
