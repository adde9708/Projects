import pygame
import random
import math
from enum import Enum
from dataclasses import dataclass
import time


# ---------------------------
# CONSTANTS
# ---------------------------
@dataclass(frozen=True, slots=True)
class Constants:
    PADDLE_SPEED = 512.0
    BALL_BASE_SPEED = 512.0
    BALL_SIZE = 16
    PADDLE_WIDTH = 10
    PADDLE_HEIGHT = 100
    HALO_PULSE_SPEED = 400.0
    HALO_ADAPTIVE_SPEED = 1024.0
    HALO_ALPHA_BASE = 0.8
    HALO_PULSE_AMP = 0.4
    HALO_ADAPTIVE_AMP = 0.2
    WINNING_DISPLAY_TIME = 4.0
    MAX_BOUNCE_ANGLE = math.radians(64.0)


# ---------------------------
# ENUMS
# ---------------------------
class GamePhase(Enum):
    READY = 1
    RUNNING = 2
    PAUSED = 3
    GAME_OVER = 4
    WINNING = 5


class PaddleControlMode(Enum):
    PLAYER = 1
    AI = 2
    NONE = 3


# ---------------------------
# UTILS
# ---------------------------
def clamp(v, lo, hi):
    return max(lo, min(v, hi))


def clamp_int(v, lo, hi):
    return max(lo, min(v, hi))


# ---------------------------
# ENTITIES
# ---------------------------
class Paddle:
    __slots__ = ("x", "y", "width", "height", "rect", "screen_height", "control_mode")

    def __init__(
        self, x, y, width, height, screen_height, control_mode=PaddleControlMode.NONE
    ):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(int(round(self.x)), int(round(self.y)), width, height)
        self.screen_height = screen_height
        self.control_mode = control_mode

    def ai_step(self, delta, speed, target_y):
        move_dist = speed * delta
        center_y = self.y + self.height * 0.5
        diff = target_y - center_y
        if abs(diff) > 1.0:
            step = math.copysign(min(abs(diff), move_dist), diff)
            self.y += step
        self.y = clamp(self.y, 0.0, float(self.screen_height - self.height))
        # update rect
        self.rect.y = int(round(self.y))

    def move(self, delta, speed, keys=None, target_y=None):
        if self.control_mode == PaddleControlMode.PLAYER and keys is not None:
            move_dist = speed * delta
            up = keys[pygame.K_w]
            down = keys[pygame.K_s]
            if up and not down:
                self.y -= move_dist
            elif down and not up:
                self.y += move_dist
            self.y = clamp(self.y, 0.0, float(self.screen_height - self.height))
            self.rect.y = int(round(self.y))
        elif self.control_mode == PaddleControlMode.AI and target_y is not None:
            self.ai_step(delta, speed, target_y)


class Ball:
    __slots__ = (
        "x",
        "y",
        "w",
        "h",
        "rect",
        "base_speed",
        "screen_width",
        "screen_height",
        "vx",
        "vy",
        "rnd",
    )

    def __init__(self, x, y, size, base_speed, screen_width, screen_height):
        self.x = float(x)
        self.y = float(y)
        self.w = size
        self.h = size
        self.rect = pygame.Rect(int(round(self.x)), int(round(self.y)), size, size)
        self.base_speed = base_speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.vx = 0.0
        self.vy = 0.0
        self.rnd = random.Random()
        self.randomize_speed()

    def randomize_speed(self):
        # write directly to vx, vy
        angle_deg = 20.0 + self.rnd.random() * 60.0
        angle = math.radians(angle_deg)
        dir_x = 1 if self.rnd.random() < 0.5 else -1
        dir_y = 1 if self.rnd.random() < 0.5 else -1
        self.vx = math.cos(angle) * self.base_speed * dir_x
        self.vy = math.sin(angle) * self.base_speed * dir_y

    def reset(self):
        self.x = (self.screen_width - self.w) * 0.5
        self.y = (self.screen_height - self.h) * 0.5
        self.rect.x = int(round(self.x))
        self.rect.y = int(round(self.y))
        self.randomize_speed()

    def move(self, delta):
        # update float position then rect
        self.x += self.vx * delta
        self.y += self.vy * delta
        self.rect.x = int(round(self.x))
        self.rect.y = int(round(self.y))

    def bounce_vertical(self):
        self.vy = -self.vy

    def magnitude(self):
        mag = math.hypot(self.vx, self.vy)
        return mag if mag > 1e-6 else self.base_speed

    def nudge_out(self, paddle_rect, dir_x):
        if dir_x > 0:
            self.x = float(paddle_rect.right)
        else:
            self.x = float(paddle_rect.left - self.w)
        self.rect.x = int(round(self.x))

    def bounce_horizontal(self, hit_fraction, paddle_rect):
        # hit_fraction in [0..1], map to angle between -MAX_BOUNCE_ANGLE and +MAX_BOUNCE_ANGLE
        hit_norm = (hit_fraction - 0.5) * 2.0
        angle = hit_norm * Constants.MAX_BOUNCE_ANGLE
        mag = self.magnitude()
        # Determine horizontal direction (invert current horizontal direction)
        if self.vx != 0.0:
            dir_x = -int(math.copysign(1.0, self.vx))
        else:
            dir_x = -1 if self.rnd.random() < 0.5 else 1

        new_dx = math.cos(angle) * dir_x
        new_dy = math.sin(angle)
        norm = math.hypot(new_dx, new_dy)
        new_dx = new_dx / norm * mag
        new_dy = new_dy / norm * mag

        # Remove floating point noise
        if abs(new_dx) < 1e-12:
            new_dx = 0.0
        if abs(new_dy) < 1e-12:
            new_dy = 0.0

        self.vx = new_dx
        self.vy = new_dy
        self.nudge_out(paddle_rect, dir_x)


# ---------------------------
# SCORING
# ---------------------------
class ScoreBoard:
    __slots__ = ("left_score", "right_score")

    def __init__(self):
        self.left_score = 0
        self.right_score = 0

    def score_left(self):
        self.left_score += 1

    def score_right(self):
        self.right_score += 1

    def reset(self):
        self.left_score = 0
        self.right_score = 0


# ---------------------------
# PHYSICS
# ---------------------------
class PhysicsEngine:
    @staticmethod
    def no_overlap(ball_rect, paddle_rect):
        overlap = min(paddle_rect.bottom, ball_rect.bottom) - max(
            paddle_rect.top, ball_rect.top
        )
        return overlap <= 0

    @staticmethod
    def paddle_hit(ball_rect, paddle_rect):
        # If no vertical overlap return center hit
        if PhysicsEngine.no_overlap(ball_rect, paddle_rect):
            return 0.5
        ball_center = ball_rect.centery
        frac = (ball_center - paddle_rect.top) / paddle_rect.height
        return clamp(frac, 0.0, 1.0)


# ---------------------------
# HALO SYSTEM
# ---------------------------
class HaloSystem:
    def __init__(self):
        # halo_color: [r, g, b, alpha(0..1)]
        self.halo_color = [102, 204, 255, Constants.HALO_ALPHA_BASE]
        # single halo surface
        self.halo_diameter = max(1, Constants.BALL_SIZE * 4)
        self.halo_surface = pygame.Surface(
            (self.halo_diameter, self.halo_diameter), pygame.SRCALPHA
        )

    def get_halo_mask(self, enabled: bool) -> float:
        return 1.0 if enabled else 0.0

    def blend_alpha(self, enabled: bool, alpha_on: float, alpha_off: float) -> float:
        mask = self.get_halo_mask(enabled)
        return mask * alpha_on + (1 - mask) * alpha_off

    def update(self, ball: Ball, now_ms: float, halo_enabled: bool):
        mask = self.get_halo_mask(halo_enabled)
        pulse = (
            abs(math.sin(now_ms / Constants.HALO_PULSE_SPEED))
            * Constants.HALO_PULSE_AMP
            + 0.8
        )
        adaptive = 1.0 - (
            Constants.HALO_ADAPTIVE_AMP
            * math.sin(now_ms / Constants.HALO_ADAPTIVE_SPEED)
        )
        speed_factor = clamp(
            math.hypot(ball.vx, ball.vy) / Constants.BALL_BASE_SPEED, 0.8, 1.2
        )
        decay = math.exp(-((now_ms % 2000.0) / 800.0))
        total_alpha = clamp(
            Constants.HALO_ALPHA_BASE * pulse * adaptive * speed_factor * mask * decay,
            0.0,
            1.0,
        )

        dir_factor = (math.copysign(1.0, ball.vx) + 1.0) * 0.5
        r = (1.0 - dir_factor) * 0.4 + dir_factor * 1.0
        g = 0.6
        b = (1.0 - dir_factor) * 1.0 + dir_factor * 0.4

        # update integers for rgb, float for alpha
        self.halo_color[0] = int(r * 255)
        self.halo_color[1] = int(g * 255)
        self.halo_color[2] = int(b * 255)
        self.halo_color[3] = total_alpha

    def handle_toggle(self, halo_enabled: bool):
        self.halo_color[3] = self.blend_alpha(
            halo_enabled, Constants.HALO_ALPHA_BASE, 0.0
        )


# ---------------------------
# RENDERER
# ---------------------------
class Renderer:
    def __init__(self, screen, halo_system: HaloSystem):
        self.screen = screen
        self.halo_system = halo_system
        pygame.font.init()
        self.font_score = pygame.font.SysFont(None, 48)
        self.font_winner = pygame.font.SysFont(None, 64)

        # score surface + last values to avoid re-rendering each frame
        self._cached_score_surf = None
        self._cached_score_value = (-1, -1)

        # winner surface + last winner string
        self._cached_winner_surf = None
        self._cached_winner_string = None

    def draw_background(self):
        # single fill call
        self.screen.fill((0, 0, 0))

    def draw_halo(self, ball: Ball):
        # Clear halo surface and draw a circle with computed alpha
        hs = self.halo_system.halo_surface
        hs.fill((0, 0, 0, 0))
        alpha = clamp(self.halo_system.halo_color[3], 0.0, 1.0)
        r = clamp_int(self.halo_system.halo_color[0], 0, 255)
        g = clamp_int(self.halo_system.halo_color[1], 0, 255)
        b = clamp_int(self.halo_system.halo_color[2], 0, 255)
        a = int(alpha * 255)
        radius = Constants.BALL_SIZE * 2
        # draw one circle into the reusable halo surface
        pygame.draw.circle(
            hs,
            (r, g, b, a),
            (self.halo_system.halo_diameter // 2, self.halo_system.halo_diameter // 2),
            radius,
        )
        # blit at ball center
        cx = ball.rect.centerx
        cy = ball.rect.centery
        halo_rect = hs.get_rect(center=(cx, cy))
        self.screen.blit(hs, halo_rect)

    def draw_paddles(self, left: Paddle, right: Paddle):
        pygame.draw.rect(self.screen, (255, 255, 255), left.rect)
        pygame.draw.rect(self.screen, (255, 255, 255), right.rect)

    def draw_ball(self, ball: Ball):
        # draw ellipse using integer rect
        pygame.draw.ellipse(self.screen, (255, 255, 255), ball.rect)

    def score_surface(self, scoreboard):
        cur = (scoreboard.left_score, scoreboard.right_score)
        if cur != self._cached_score_value:
            text = f"{cur[0]} | {cur[1]}"
            self._cached_score_surf = self.font_score.render(
                text, True, (255, 255, 255)
            )
            self._cached_score_value = cur
        return self._cached_score_surf

    def draw_score(self, scoreboard):
        surf = self.score_surface(scoreboard)
        if surf:
            self.screen.blit(
                surf, (self.screen.get_width() // 2 - surf.get_width() // 2, 20)
            )

    def winner_surface(self, winner_string):
        # return cached or refresh only when string changed
        if winner_string and (
            winner_string != self._cached_winner_string
            or self._cached_winner_surf is None
        ):
            self._cached_winner_surf = self.font_winner.render(
                winner_string, True, (255, 255, 255)
            )
            self._cached_winner_string = winner_string

        return self._cached_winner_surf

    def draw_winner_overlay(self, phase, winner_string, alpha):
        surf = self.winner_surface(winner_string)
        if phase != GamePhase.WINNING or not surf:
            return

        a = clamp_int(int(clamp(alpha, 0.0, 255.0)), 0, 255)
        tmp = surf.copy()  # only copy when actually drawing
        tmp.set_alpha(a)
        self.screen.blit(
            tmp,
            tmp.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
            ),
        )

    def draw_scene(
        self,
        left_paddle: Paddle,
        right_paddle: Paddle,
        ball: Ball,
        scoreboard: ScoreBoard,
        phase: GamePhase,
        winner_string: str,
        winner_text_alpha: float,
    ):

        self.draw_background()
        self.draw_halo(ball)
        self.draw_paddles(left_paddle, right_paddle)
        self.draw_ball(ball)
        self.draw_score(scoreboard)
        self.draw_winner_overlay(phase, winner_string, winner_text_alpha)
        pygame.display.flip()


# ---------------------------
# GAME CONTROLLER
# ---------------------------
class GameController:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height

        self.left_paddle = Paddle(
            30,
            (screen_height - Constants.PADDLE_HEIGHT) / 2.0,
            Constants.PADDLE_WIDTH,
            Constants.PADDLE_HEIGHT,
            screen_height,
            PaddleControlMode.PLAYER,
        )
        self.right_paddle = Paddle(
            screen_width - 40,
            (screen_height - Constants.PADDLE_HEIGHT) / 2.0,
            Constants.PADDLE_WIDTH,
            Constants.PADDLE_HEIGHT,
            screen_height,
            PaddleControlMode.AI,
        )
        self.ball = Ball(
            screen_width / 2.0 - Constants.BALL_SIZE / 2.0,
            screen_height / 2.0 - Constants.BALL_SIZE / 2.0,
            Constants.BALL_SIZE,
            Constants.BALL_BASE_SPEED,
            screen_width,
            screen_height,
        )
        self.scoreboard = ScoreBoard()
        self.phase = GamePhase.READY
        self.winner = ""
        self.winning_start_time = None
        self.winner_text_alpha = 0.0
        # keep halo color state mirrored
        self.halo_color = [102, 204, 255, Constants.HALO_ALPHA_BASE]

    def handle_escape(self, keys):
        if keys[pygame.K_ESCAPE]:
            self.phase = GamePhase.PAUSED
            return True
        return False

    def update_left_paddle(self, delta, keys):
        self.left_paddle.move(delta, Constants.PADDLE_SPEED, keys)

    def update_ai_paddle(self, delta, ai_delay_table):
        total_score = min(
            self.scoreboard.left_score + self.scoreboard.right_score,
            len(ai_delay_table) - 1,
        )
        ai_speed = (
            Constants.PADDLE_SPEED
            * ai_delay_table[total_score]
            * (0.8 + random.random() * 0.2)
        )
        target_y = self.ball.y + self.ball.h * 0.5
        self.right_paddle.move(delta, ai_speed, None, target_y)

    def update_ball_motion(self, delta):
        self.ball.move(delta)
        self.check_vertical_bounce()
        self.check_paddle_collision()

    def reset_paddles(self):
        mid_y = self.height / 2.0
        self.left_paddle.y = mid_y - self.left_paddle.height / 2.0
        self.right_paddle.y = mid_y - self.right_paddle.height / 2.0
        self.left_paddle.rect.y = int(round(self.left_paddle.y))
        self.right_paddle.rect.y = int(round(self.right_paddle.y))

    def reset_ball_and_paddles(self):
        self.ball.reset()
        self.reset_paddles()
        return True

    def handle_scoring(self):
        # use primitive positions for checks (float -> int boundary)
        if self.ball.rect.left <= 0:
            self.scoreboard.score_right()
            return self.reset_ball_and_paddles()
        if self.ball.rect.right >= self.width:
            self.scoreboard.score_left()
            return self.reset_ball_and_paddles()
        return False

    def handle_winner(self, now, winning_score):
        if (self.scoreboard.left_score >= winning_score) or (
            self.scoreboard.right_score >= winning_score
        ):
            if self.scoreboard.left_score > self.scoreboard.right_score:
                self.winner = "Left Player Wins!"
            elif self.scoreboard.right_score > self.scoreboard.left_score:
                self.winner = "Right Player Wins!"
            else:
                self.winner = "It's a tie!"
            self.phase = GamePhase.WINNING
            self.winning_start_time = now
            return True
        return False

    def check_vertical_bounce(self):
        if self.ball.y <= 0.0:
            self.ball.y = 0.0
            self.ball.rect.y = 0
            self.ball.bounce_vertical()
        elif self.ball.y + self.ball.h >= self.height:
            self.ball.y = float(self.height - self.ball.h)
            self.ball.rect.y = int(round(self.ball.y))
            self.ball.bounce_vertical()

    def check_paddle_collision(self):
        # use rect.intersects, physics uses primitive math where possible
        if self.ball.rect.colliderect(self.left_paddle.rect):
            hit = PhysicsEngine.paddle_hit(self.ball.rect, self.left_paddle.rect)
            self.ball.bounce_horizontal(hit, self.left_paddle.rect)
        elif self.ball.rect.colliderect(self.right_paddle.rect):
            hit = PhysicsEngine.paddle_hit(self.ball.rect, self.right_paddle.rect)
            self.ball.bounce_horizontal(hit, self.right_paddle.rect)

    def update_running(self, delta, keys, now, ai_delay_table, winning_score):
        if self.handle_escape(keys):
            return
        self.update_left_paddle(delta, keys)
        self.update_ai_paddle(delta, ai_delay_table)
        self.update_ball_motion(delta)
        if self.handle_scoring():
            return
        self.handle_winner(now, winning_score)

    def update_ready(self, keys):
        if keys[pygame.K_SPACE]:
            self.phase = GamePhase.RUNNING

    def update_paused(self, keys):
        if keys[pygame.K_SPACE]:
            self.phase = GamePhase.RUNNING

    def update_winning(self, delta, now):
        self.winner_text_alpha = clamp(
            self.winner_text_alpha + 128.0 * delta, 0.0, 255.0
        )
        if (
            self.winning_start_time
            and (now - self.winning_start_time) / 1000.0
            >= Constants.WINNING_DISPLAY_TIME
        ):
            self.scoreboard.reset()
            self.ball.reset()
            self.reset_paddles()
            self.phase = GamePhase.READY
            self.winning_start_time = None
            self.winner_text_alpha = 0.0

    def update(self, delta, keys, now, ai_delay_table, winning_score):

        phase = self.phase
        if phase == GamePhase.RUNNING:
            self.update_running(delta, keys, now, ai_delay_table, winning_score)
        elif phase == GamePhase.READY:
            self.update_ready(keys)
        elif phase == GamePhase.PAUSED:
            self.update_paused(keys)
        elif phase == GamePhase.WINNING:
            self.update_winning(delta, now)


# ---------------------------
# PONG GAME (runner)
# ---------------------------
class PongGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 640, 512
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.DOUBLEBUF
        )
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()

        self.game = GameController(self.width, self.height)
        self.halo_system = HaloSystem()
        self.renderer = Renderer(self.screen, self.halo_system)
        self.ai_delay_table = self.create_ai_delay_table()
        self.halo_enabled = True
        self.running = True
        self.winning_score = 10

        # Input state
        self.keys = pygame.key.get_pressed  # function pointer to call once per frame
        # minimize allocation by storing last key for halo
        self._halo_toggled = False

    @staticmethod
    def create_ai_delay_table():
        base = 0.8
        factor = 0.04
        return tuple(base / (1 + factor * i) for i in range(1025))

    def handle_events(self):
        halo_toggled = False
        running = True
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_h:
                    halo_toggled = True
        return running, halo_toggled

    def handle_halo_toggle(self, toggled):
        if toggled:
            self.halo_enabled = not self.halo_enabled
            self.halo_system.handle_toggle(self.halo_enabled)

    def run(self):
        self.game.reset_ball_and_paddles()
        # pre-warm fonts / surfaces
        self.renderer.draw_score(self.game.scoreboard)

        while self.running:
            dt_ms = self.clock.tick_busy_loop(0)
            dt = dt_ms / 1000.0
            now = pygame.time.get_ticks()
            frame_start = time.perf_counter()

            running_events, halo_toggled = self.handle_events()
            if not running_events:
                self.running = False
                break

            keys = pygame.key.get_pressed()
            self.handle_halo_toggle(halo_toggled)

            # --- PROFILING START ---
            t0 = time.perf_counter()

            # Update
            self.game.update(dt, keys, now, self.ai_delay_table, self.winning_score)

            t1 = time.perf_counter()

            # Halo
            self.halo_system.update(self.game.ball, now, self.halo_enabled)

            t2 = time.perf_counter()

            # Render
            self.renderer.draw_scene(
                self.game.left_paddle,
                self.game.right_paddle,
                self.game.ball,
                self.game.scoreboard,
                self.game.phase,
                self.game.winner,
                self.game.winner_text_alpha,
            )

            t3 = time.perf_counter()
            # --- PROFILING END ---

            # section timing (always show during stutter)

        frame_end = time.perf_counter()
        frame_time = (frame_end - frame_start) * 1000
        if frame_time > 20:
            print(
                f"update={(t1-t0)*1000:.2f}ms  "
                f"halo={(t2-t1)*1000:.2f}ms  "
                f"render={(t3-t2)*1000:.2f}ms  "
                f"total={frame_time:.2f}ms"
            )

        pygame.quit()


def main():
    PongGame().run()


if __name__ == "__main__":
    main()
