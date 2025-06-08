import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout - Cihan Ege")

BLUE = (0, 102, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 40, 120, 15)
paddle_speed = 12

balls = [pygame.Rect(WIDTH // 15 - 40, HEIGHT // 2, 30, 30)]
ball_speeds = [[5, -5]]

blocks = []
block_rows = 5
block_cols = 10
block_width = WIDTH // block_cols
block_height = 30

for row in range(block_rows):
    for col in range(block_cols):
        block = pygame.Rect(col * block_width, row * block_height + 60, block_width - 2, block_height - 2)
        blocks.append(block)

clock = pygame.time.Clock()
running = True

# Gecikmeli top üretim kuyruğu: [(zaman, x, y, [vx, vy])]
delayed_spawns = []

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # TOP HAREKETLERİ
    for i in range(len(balls)):
        ball = balls[i]
        speed = ball_speeds[i]

        ball.x += speed[0]
        ball.y += speed[1]

        if ball.left <= 0 or ball.right >= WIDTH:
            speed[0] *= -1
        if ball.top <= 0:
            speed[1] *= -1
        if ball.bottom >= HEIGHT:
            print("Kaybettin!")
            pygame.quit()
            sys.exit()

        if ball.colliderect(paddle):
            speed[1] *= -1

        for block in blocks[:]:
            if block.colliderect(ball):
                blocks.remove(block)
                speed[1] *= -1

                # 3 saniye (3000 ms) sonra top oluşturulacak şekilde sıraya ekle
                delay_time = pygame.time.get_ticks() + 2000
                spawn_info = (delay_time, ball.x, ball.y, [speed[0], -speed[1]])
                delayed_spawns.append(spawn_info)
                break

    # GECİKMELİ TOP OLUŞTURMA
    current_time = pygame.time.get_ticks()
    for spawn in delayed_spawns[:]:
        spawn_time, x, y, vel = spawn
        if current_time >= spawn_time:
            new_ball = pygame.Rect(x, y, 30, 30)
            balls.append(new_ball)
            ball_speeds.append(vel)
            delayed_spawns.remove(spawn)

    # ÇİZİMLER
    pygame.draw.rect(screen, BLUE, paddle)
    for ball in balls:
        pygame.draw.ellipse(screen, RED, ball)
    for block in blocks:
        pygame.draw.rect(screen, GREEN, block)

    pygame.display.flip()
    clock.tick(60)
