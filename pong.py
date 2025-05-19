import pygame
import sys


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

    return {
        "left_paddle": left_paddle,
        "right_paddle": right_paddle,
        "ball": ball,
        "ball_speed": [512, 512],  # Speed stays fixed, but could be a parameter too
    }


def handle_input(state, delta, speed, height):
    keys = pygame.key.get_pressed()
    move_amount = int(speed * delta)

    left_paddle = state["left_paddle"]
    right_paddle = state["right_paddle"]

    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= move_amount
    elif keys[pygame.K_s] and left_paddle.bottom < height:
        left_paddle.y += move_amount

    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= move_amount
    elif keys[pygame.K_DOWN] and right_paddle.bottom < height:
        right_paddle.y += move_amount


def update_ball(state, delta, width, height):

    ball = state["ball"]
    speed = state["ball_speed"]

    ball.x += int(speed[0] * delta)
    ball.y += int(speed[1] * delta)

    if ball.top <= 0 or ball.bottom >= height:
        speed[1] = -speed[1]

    ball_did_colide = check_collison(state, ball)

    if ball_did_colide:
        speed[0] = -speed[0]

    if ball.left <= 0 or ball.right >= width:
        speed[0] = -speed[0]
        ball.center = (width // 2, height // 2)


def check_collison(state, ball):
    return ball.colliderect(state["left_paddle"]) or ball.colliderect(
        state["right_paddle"]
    )


def draw(state, screen, black, white):
    screen.fill(black)
    pygame.draw.rect(screen, white, state["left_paddle"])
    pygame.draw.rect(screen, white, state["right_paddle"])
    pygame.draw.ellipse(screen, white, state["ball"])
    pygame.display.flip()


def main():

    WINDOW_WIDTH, WINDOW_HEIGHT = 640, 512
    PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
    PADDLE_SPEED = 512
    BALL_SIZE = 15
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    screen = init_pygame(WINDOW_WIDTH, WINDOW_HEIGHT)
    clock = pygame.time.Clock()
    state = create_game_state(
        WINDOW_WIDTH, WINDOW_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, BALL_SIZE
    )

    while True:
        delta = clock.tick_busy_loop(60) / 1024

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        handle_input(state, delta, PADDLE_SPEED, WINDOW_HEIGHT)
        update_ball(state, delta, WINDOW_WIDTH, WINDOW_HEIGHT)
        draw(state, screen, BLACK, WHITE)


if __name__ == "__main__":
    main()
