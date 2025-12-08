import pygame
import sys
import random


def init_pygame(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong Game")
    return screen


def create_game_state(width, height, paddle_width, paddle_height, ball_size):
    left_paddle = pygame.Rect(
        30, (height - paddle_height) // 2, paddle_width, paddle_height
    )
    right_paddle = pygame.Rect(
        width - 40, (height - paddle_height) // 2, paddle_width, paddle_height
    )
    ball = pygame.Rect(width // 2, height // 2, ball_size, ball_size)
    ball_speed = pygame.math.Vector2(512, 512)
    return {
        "left_paddle": left_paddle,
        "right_paddle": right_paddle,
        "ball": ball,
        "ball_speed": ball_speed,
    }


def handle_input(state, delta, paddle_speed, screen_height):
    keys = pygame.key.get_pressed()
    move_amount = paddle_speed * delta

    left_paddle = state["left_paddle"]
    right_paddle = state["right_paddle"]

    # Move left paddle
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y = max(left_paddle.y - move_amount, 0)
    elif keys[pygame.K_s] and left_paddle.bottom < screen_height:
        left_paddle.y = min(
            left_paddle.y + move_amount, screen_height - left_paddle.height
        )

    # Move right paddle
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y = max(right_paddle.y - move_amount, 0)
    elif keys[pygame.K_DOWN] and right_paddle.bottom < screen_height:
        right_paddle.y = min(
            right_paddle.y + move_amount, screen_height - right_paddle.height
        )


def update_ball(state, delta, screen_width, screen_height):
    ball = state["ball"]
    speed = state["ball_speed"]

    # Update ball position using vector math for smooth movement
    ball.x += speed.x * delta
    ball.y += speed.y * delta

    # Bounce off top and bottom
    if ball.top <= 0:
        ball.top = 0
        speed.y = -speed.y
    elif ball.bottom >= screen_height:
        ball.bottom = screen_height
        speed.y = -speed.y

    # Bounce off paddles
    if ball.colliderect(state["left_paddle"]) or ball.colliderect(
        state["right_paddle"]
    ):
        speed.x = -speed.x

    # Reset ball if it goes past left or right edge (score)
    if ball.left <= 0 or ball.right >= screen_width:
        ball.center = (screen_width // 2, screen_height // 2)
        # Randomize initial ball speed direction to make the game less predictable
        speed.x = 512 * random.choice([-1, 1])
        speed.y = 512 * random.choice([-1, 1])


def draw(state, screen, background_color, paddle_ball_color):
    screen.fill(background_color)
    pygame.draw.rect(screen, paddle_ball_color, state["left_paddle"])
    pygame.draw.rect(screen, paddle_ball_color, state["right_paddle"])
    pygame.draw.ellipse(screen, paddle_ball_color, state["ball"])
    pygame.display.flip()


def main():
    WINDOW_WIDTH, WINDOW_HEIGHT = 640, 512
    PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
    PADDLE_SPEED = 512
    BALL_SIZE = 16
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FPS = 60

    screen = init_pygame(WINDOW_WIDTH, WINDOW_HEIGHT)
    clock = pygame.time.Clock()
    state = create_game_state(
        WINDOW_WIDTH, WINDOW_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, BALL_SIZE
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        delta = clock.tick_busy_loop(FPS) / 1000
        handle_input(state, delta, PADDLE_SPEED, WINDOW_HEIGHT)
        update_ball(state, delta, WINDOW_WIDTH, WINDOW_HEIGHT)
        draw(state, screen, BLACK, WHITE)


if __name__ == "__main__":
    main()
