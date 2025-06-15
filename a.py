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
PADDLE_SPEED = 0.03
BACKGROUND_COLOR = (0, 0, 0)
CIRCLE_COLOR = (50, 50, 50)
BALL_COLOR = (255, 255, 255)
PADDLE_COLORS = [(255, 100, 100), (100, 100, 255)]

#экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Pong")
clock = pygame.time.Clock()

#инициализация мяча и ракеток
def reset_ball():
    angle = random.uniform(0, 2 * math.pi)
    return {
        'pos': [CENTER[0], CENTER[1]],
        'vel': [BALL_SPEED * math.cos(angle), BALL_SPEED * math.sin(angle)]
    }

ball = reset_ball()

paddles = [
    {'angle': 0.0, 'keys': (pygame.K_a, pygame.K_d)},   # Игрок 1: A/D
    {'angle': math.pi, 'keys': (pygame.K_LEFT, pygame.K_RIGHT)}  # Игрок 2: стрелки
]

#игра
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
        angle = math.atan2(dy, dx)
        normalized_angle = angle % (2 * math.pi)
        
        #проверка на ракетку
        collision = False
        for i, paddle in enumerate(paddles):
            start_angle = paddle['angle'] - PADDLE_LENGTH / 2
            end_angle = paddle['angle'] + PADDLE_LENGTH / 2
            
            #проверка
            if (start_angle <= normalized_angle <= end_angle or 
                (start_angle < 0 and normalized_angle < end_angle) or
                (end_angle > 2 * math.pi and normalized_angle > start_angle)):
                collision = True
                
                #отскок
                normal_angle = angle + math.pi
                ball['vel'][0] = BALL_SPEED * math.cos(normal_angle)
                ball['vel'][1] = BALL_SPEED * math.sin(normal_angle)
                break
        
        #вылет
        if not collision:
            reset_ball()
            ball = reset_ball()
        else:
            correction_angle = angle - math.pi/180
            ball['pos'][0] = CENTER[0] + (CIRCLE_RADIUS - BALL_RADIUS - 1) * math.cos(correction_angle)
            ball['pos'][1] = CENTER[1] + (CIRCLE_RADIUS - BALL_RADIUS - 1) * math.sin(correction_angle)
    
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
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
