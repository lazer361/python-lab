import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Clone")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Параметры игры
FPS = 60
clock = pygame.time.Clock()

# Шрифт для отображения счета
font = pygame.font.SysFont("Arial", 24)

# Параметры ракетки
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
paddle_speed = 7
paddle = pygame.Rect((WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Параметры мяча
ball_radius = 8
ball_speed_x = 4
ball_speed_y = -4
ball = pygame.Rect((WIDTH // 2, HEIGHT // 2), (ball_radius*2, ball_radius*2))

# Параметры блоков
brick_rows = 6
brick_cols = 10
brick_width = WIDTH // brick_cols
brick_height = 25

bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        brick = pygame.Rect(col * brick_width, row * brick_height + 50, brick_width, brick_height)
        bricks.append(brick)

# Счет
score = 0

# Функция отрисовки всех игровых объектов
def draw_objects():
    screen.fill(BLACK)
    # Ракетка
    pygame.draw.rect(screen, BLUE, paddle)
    # Мяч
    pygame.draw.circle(screen, WHITE, (ball.centerx, ball.centery), ball_radius)
    # Блоки
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)
    # Счет
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

running = True
while running:
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление ракеткой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # Движение мяча
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Столкновения со стенами
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.bottom >= HEIGHT:
        # Мяч упал вниз — конец игры
        running = False

    # Столкновение с ракеткой
    if ball.colliderect(paddle):
        ball_speed_y *= -1
        # Небольшое смещение скорости в зависимости от места удара по ракетке
        offset = (ball.centerx - paddle.centerx) / (PADDLE_WIDTH // 2)
        ball_speed_x = 4 * offset

    # Столкновение с блоками
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        hit_brick = bricks.pop(hit_index)
        score += 10
        # Определяем сторону столкновения
        # Проверяем, с какой стороны мяч вошел в блок
        if ball.centerx >= hit_brick.left and ball.centerx <= hit_brick.right:
            # Мяч ударил сверху или снизу
            ball_speed_y *= -1
        else:
            # Мяч ударил сбоку
            ball_speed_x *= -1

    # Проверяем, победили ли мы (все блоки удалены)
    if not bricks:
        # Все блоки сбиты — победа
        running = False

    draw_objects()

pygame.quit()
sys.exit()
