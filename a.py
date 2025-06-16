import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
CIRCLE_RADIUS = 300
BALL_RADIUS = 10
PADDLE_LENGTH = 0.4  #в радианах
PADDLE_DISTANCE = CIRCLE_RADIUS - 10
BALL_SPEED = 6
PADDLE_SPEED = 0.06
BACKGROUND_COLOR = (0, 0, 0)
CIRCLE_COLOR = (50, 50, 50)
BALL_COLOR = (255, 255, 255)
PADDLE_COLORS = [(255, 100, 100), (100, 100, 255)]
SCORE_COLOR = (200, 200, 200)

#экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 72)

#инициализация мяча и ракеток
def reset_ball():
    angle = random.uniform(0, 2 * math.pi)
    return {
        'pos': [CENTER[0] + random.uniform(-1 * WIDTH / 5, WIDTH / 5), CENTER[1] + random.uniform(-1 * HEIGHT / 5, HEIGHT / 5)],
        'vel': [BALL_SPEED * math.cos(angle), BALL_SPEED * math.sin(angle)]
    }

ball = reset_ball()

paddles = [
    {'angle': 0.0, 'keys': (pygame.K_a, pygame.K_d)},   # Игрок 1: A/D
    {'angle': math.pi, 'keys': (pygame.K_LEFT, pygame.K_RIGHT)}  # Игрок 2: стрелки
]

# Функция для нормализации углов
def normalize_angle(angle):
    while angle < 0:
        angle += 2 * math.pi
    while angle >= 2 * math.pi:
        angle -= 2 * math.pi
    return angle

# Функция для проверки столкновения с ракеткой
def check_paddle_collision(paddle_angle, ball_angle):
    # Нормализуем углы
    paddle_angle = normalize_angle(paddle_angle)
    ball_angle = normalize_angle(ball_angle)
    
    # Рассчитываем границы ракетки
    start_angle = paddle_angle - PADDLE_LENGTH / 2
    end_angle = paddle_angle + PADDLE_LENGTH / 2
    
    # Проверяем пересечение с учётом перехода через 0
    if start_angle < 0:
        return ball_angle <= end_angle or ball_angle >= start_angle + 2 * math.pi
    elif end_angle > 2 * math.pi:
        return ball_angle >= start_angle or ball_angle <= end_angle - 2 * math.pi
    else:
        return start_angle <= ball_angle <= end_angle

#игра
scores = [0, 0]
running = True
while running:
    #выход
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #управление
    keys = pygame.key.get_pressed()
    for paddle in paddles:
        if keys[paddle['keys'][0]]:  #левая клавиша
            paddle['angle'] -= PADDLE_SPEED
        if keys[paddle['keys'][1]]:  #правая клавиша
            paddle['angle'] += PADDLE_SPEED
    
    #движение мяча
    ball['pos'][0] += ball['vel'][0]
    ball['pos'][1] += ball['vel'][1]
    
    #проверка на вылет
    dx = ball['pos'][0] - CENTER[0]
    dy = ball['pos'][1] - CENTER[1]
    distance = math.sqrt(dx*dx + dy*dy)
    
    if distance + BALL_RADIUS >= CIRCLE_RADIUS:
        #гол полета мяча
        ball_angle = math.atan2(dy, dx)
        
        #проверка столкновения с ракеткоей
        collision = False
        paddle_hit = None
        
        for paddle in paddles:
            if check_paddle_collision(paddle['angle'], ball_angle):
                collision = True
                paddle_hit = paddle
                break
        
        if collision:
            #нормаль
            normal_x = dx / distance
            normal_y = dy / distance
            
            dot_product = ball['vel'][0] * normal_x + ball['vel'][1] * normal_y
            
            #отскок
            ball['vel'][0] = ball['vel'][0] - 2 * dot_product * normal_x
            ball['vel'][1] = ball['vel'][1] - 2 * dot_product * normal_y
            
            #коррекция скорости по модулю
            speed = math.sqrt(ball['vel'][0]**2 + ball['vel'][1]**2)
            if speed > 0:
                ball['vel'][0] = ball['vel'][0] / speed * BALL_SPEED
                ball['vel'][1] = ball['vel'][1] / speed * BALL_SPEED
            
            #мяч в круг обратно
            factor = (CIRCLE_RADIUS - BALL_RADIUS - 1) / distance
            ball['pos'][0] = CENTER[0] + dx * factor
            ball['pos'][1] = CENTER[1] + dy * factor
        else:
            #print(ball['pos'][0])
            if ball['pos'][0] > 400:
                scores[0] += 1  #очко первому игроку
            else:
                scores[1] += 1  #очко второму игроку
            ball = reset_ball()
    
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.circle(screen, CIRCLE_COLOR, CENTER, CIRCLE_RADIUS, 2)
    
    #мяч
    pygame.draw.circle(screen, BALL_COLOR, (int(ball['pos'][0]), int(ball['pos'][1])), BALL_RADIUS)
    
    #ракетки
    for i, paddle in enumerate(paddles):
        start_angle = paddle['angle'] - PADDLE_LENGTH / 2
        end_angle = paddle['angle'] + PADDLE_LENGTH / 2
        
        points = []
        for a in range(int(math.degrees(start_angle)), int(math.degrees(end_angle)) + 1):
            rad = math.radians(a)
            x = CENTER[0] + PADDLE_DISTANCE * math.cos(rad)
            y = CENTER[1] + PADDLE_DISTANCE * math.sin(rad)
            points.append((x, y))
        
        if points:
            pygame.draw.lines(screen, PADDLE_COLORS[i], False, points, 5)

    score_text = font.render(f"{scores[0]} : {scores[1]}", True, SCORE_COLOR)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
