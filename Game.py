""" ESCAPE - PAUSE
    ENTER - LAUNCH BALL
    F5 - START NEW GAME"""

import pygame
from CONSTANS import *
from random import choices
from os import path

pygame.init()
pygame.display.set_caption('Bricka')

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

running = True


class Platform:
    def __init__(self):
        self.platform_velocity_r = 10
        self.platform_velocity_l = 10
        self.song_hit_platform = pygame.mixer.Sound('golf.wav')
        self.platform = pygame.Rect(int(SIZE[0] // 2 - PLATFORM_WIDTH // 2), int(SIZE[1] - PLATFORM_HEIGHT - 10),
                                    PLATFORM_WIDTH,
                                    PLATFORM_HEIGHT)

    def platform_startpos(self):
        self.platform = pygame.Rect(int(SIZE[0] // 2 - PLATFORM_WIDTH // 2), int(SIZE[1] - PLATFORM_HEIGHT - 10),
                                    PLATFORM_WIDTH,
                                    PLATFORM_HEIGHT)

    def render(self):
        pygame.draw.rect(screen, BLUE, self.platform)


class Brick:
    def __init__(self):
        pass


class Ball:
    def __init__(self):
        self.velocity = 5
        self.ball_startpos()
        self.song_hit_brick = pygame.mixer.Sound("bable.wav")

    def ball_startpos(self):
        self.ball_rect = pygame.Rect(int(SIZE[0] // 2), int(SIZE[1] - PLATFORM_HEIGHT - 2.2 * BALL_RADIUS), BALL_RADIUS,
                                     BALL_RADIUS)
        self.ball_view_y = -1
        self.ball_view_x = 1

    def render(self):
        pygame.draw.circle(screen, WHITE, (self.ball_rect.left, self.ball_rect.top), BALL_RADIUS)

    def move_ball(self):
        self.ball_rect.top += self.velocity * self.ball_view_y
        self.ball_rect.left += self.velocity * self.ball_view_x


class Brick_Game:
    def __init__(self):
        # Screen area
        self.area = pygame.Rect(0, 0, SIZE[0], SIZE[1])
        # Inside settinngs
        self.lives = 3
        self.score = 0

        # Create bricks
        self.bricks = self.create_bricks()

        # init ball and platform
        self.ball = Ball()
        self.platform = Platform()

        # STATUS
        self.status = "on_platform"
        self.render_lose = True
        self.render_win = True

        # MUSIC

    # Creature bricks
    def create_bricks(self):
        bricks = []
        for x in range(int(0.8 * SIZE[0]) // BRICK_WIDTH):
            for y in range(int(0.25 * SIZE[1]) // BRICK_HEIGHT):
                brick = Brick()
                brick.rect = pygame.Rect(LEFT + BRICK_WIDTH * x + 10, TOP + BRICK_HEIGHT * y + 10, BRICK_WIDTH,
                                         BRICK_HEIGHT)
                bricks.append(brick
                              )

        return bricks

    # Render bricks
    def render_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(screen, (214, 157, 51), brick.rect, 1)

    # Change the coordinates of the ball

    # Check collision with wall
    def check_collision(self):
        if self.ball.ball_rect.left not in range(SIZE[0]):
            self.ball.ball_view_x = - self.ball.ball_view_x

        if self.ball.ball_rect.top < 0:
            self.ball.ball_view_y = - self.ball.ball_view_y
            self.ball.ball_rect.top = 0

        if self.ball.ball_rect.top > SIZE[1] - PLATFORM_HEIGHT:
            self.lives -= 1
            if self.lives > 0:
                self.status = "on_platform"
                self.ball.ball_startpos()
                self.platform.platform_startpos()

    # Check_collision_with_bricks
    def check_collision_with_bricks(self):
        for brick in self.bricks:
            if brick.rect.colliderect(self.ball.ball_rect):
                self.ball.ball_view_y = -self.ball.ball_view_y
                self.ball.song_hit_brick.play()
                self.score += 5
                self.bricks.remove(brick)

    # Check_collision_with_platform
    def check_collision_with_platform(self):
        if self.ball.ball_rect.colliderect(self.platform.platform):
            self.ball.song_hit_brick.play()
            self.ball.ball_view_y = -self.ball.ball_view_y

    #
    def defeat_or_win(self):
        if len(self.bricks) == 0:
            self.status = "WIN"

        if self.lives == 0:
            self.status = "LOSE"

    # Check Statuses
    def check_statuses(self):

        if self.status == "LOSE" and self.render_lose:
            self.gameover_window()
            pygame.display.flip()
            self.render_lose = False
        elif self.status == "WIN" and self.render_win:
            self.win_window()
            self.render_win = False

    # if player defeat, this window is being showed
    def gameover_window(self):
        screen.fill(0)
        self.draw_text("GAME OVER", (SIZE[0] // 2 - 150, SIZE[1] // 2 - 120), 50)
        self.draw_text("Your score {}".format(self.score), (SIZE[0] // 2 - 80, SIZE[1] // 2 - 50), 30)
        self.draw_text("PRESS F5 TO START NEW GAME", (25, SIZE[1] // 2), 40)

    # If player win
    def win_window(self):
        screen.fill(0)
        self.draw_text("YOU WIN", (SIZE[0] // 2 - 120, SIZE[1] // 2 - 120), 50)
        self.draw_text("Your score {}".format(self.score), (SIZE[0] // 2 - 80, SIZE[1] // 2 - 50), 30)
        self.draw_text("PRESS F5 TO START NEW GAME", (25, SIZE[1] // 2), 40)

    # PAUSE
    def pause(self):
        self.status = "pause"
        self.ball.velocity = 0
        self.platform.platform_velocity_r = 0
        self.platform.platform_velocity_l = 0

    # CONTINUE GAME
    def continue_game(self):
        self.status = "playing"
        self.ball.velocity = 5
        self.platform.platform_velocity_r = 10
        self.platform.platform_velocity_l = 10

    # draw text on field

    def draw_text(self, line, pos, fz, center=True):
        f2 = pygame.font.SysFont('serif', fz)
        text1 = f2.render(line, 1, (255, 255, 255))
        if center:
            pos = (SIZE[0] // 2 - text1.get_width() // 2, pos[1])
        screen.blit(text1, (pos))

    # Render field objects
    def render(self):
        screen.fill(0)

        self.platform.render()
        self.ball.render()
        self.render_bricks()
        self.draw_text("Score {}".format(self.score), (SIZE[0] // 2 - 40, 10), 20)
        self.draw_text("LIVES {}".format(self.lives), (SIZE[0] - 50, SIZE[1] - 20), 10, False)
        clock.tick(60)


game = Brick_Game()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.status == "playing":
                    game.pause()
                elif game.status == "pause":
                    game.continue_game()

    keys = pygame.key.get_pressed()
    if keys[13] and game.lives != 0:
        game.status = "playing"

    if keys[pygame.K_RIGHT]:

        if game.platform.platform.left in range(-10, SIZE[0] - PLATFORM_WIDTH):
            if game.status == "on_platform":
                game.ball.ball_rect.left += game.platform.platform_velocity_r
                game.platform.platform.left += game.platform.platform_velocity_r
            else:
                game.platform.platform.left += game.platform.platform_velocity_r

    if keys[pygame.K_LEFT]:
        if game.platform.platform.left in range(SIZE[0] - PLATFORM_WIDTH + 10):
            if game.status == "on_platform":
                game.ball.ball_rect.left -= game.platform.platform_velocity_r
                game.platform.platform.left -= game.platform.platform_velocity_r
            else:
                game.platform.platform.left -= game.platform.platform_velocity_r

    if keys[pygame.K_F5] and (game.status == "LOSE" or game.status == "WIN"):
        game.__init__()

    if game.status == 'playing':
        game.check_collision()
        game.check_collision_with_bricks()
        game.check_collision_with_platform()
        game.ball.move_ball()
        game.defeat_or_win()

    game.check_statuses()

    if game.status == "playing" or game.status == "on_platform":
        game.render()

    pygame.display.flip()
pygame.quit()
