import pygame
import pymunk
import sys
import math

# Pygame 초기화
pygame.init()

# 상수들
WIDTH, HEIGHT = 1024, 576
R = 10  # 공의 반지름
X, Y = R, HEIGHT - R  # 시작 위치 (x, y)
restitution = 0.7  # 복원 계수
angle = 47  # 출발 각도
speed = 460  # 공의 속도
friction = 5  # 마찰 계수
air_resistance_coefficient = 0.1  # 공기 저항 계수
velocity_threshold = 10  # 속도 임계값

# 속도 계산
vx = speed * math.cos(math.radians(angle))
vy = -speed * math.sin(math.radians(angle))

# 디스플레이 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pymunk Physics Simulation")

# Pymunk 공간 생성 및 중력 설정
space = pymunk.Space()
space.gravity = 0, -98

def create_ball(space, position, radius, restitution, velocity):
    mass = 1
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    body.position = position
    body.velocity = velocity
    shape = pymunk.Circle(body, radius)
    shape.elasticity = restitution
    shape.friction = friction  # 마찰력 설정
    space.add(body, shape)
    return shape

ball = create_ball(space, (X, HEIGHT - Y), R, restitution, (vx, vy))

def create_wall(space, p0, p1, restitution):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, p0, p1, 1)
    shape.elasticity = restitution
    shape.friction = friction  # 마찰력 설정
    space.add(body, shape)

create_wall(space, (0, HEIGHT), (WIDTH, HEIGHT), restitution)
create_wall(space, (0, 0), (WIDTH, 0), restitution)
create_wall(space, (0, 0), (0, HEIGHT), restitution)
create_wall(space, (WIDTH, 0), (WIDTH, HEIGHT), restitution)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 공기 저항
    air_resistance = (-air_resistance_coefficient * ball.body.velocity[0], 
                      -air_resistance_coefficient * ball.body.velocity[1])
    ball.body.apply_force_at_local_point(air_resistance, (0,0))
    
   

    space.step(1/60)
    # 속도 임계값 확인
    if abs(ball.body.velocity[0]) == 0  and abs(ball.body.velocity[1]) < 50:
        ball.body.velocity = 0, 0
        
    screen.fill((220, 220, 220))
    x, y = int(ball.body.position.x), HEIGHT - int(ball.body.position.y)
    pygame.draw.circle(screen, (0, 0, 0), (x, y), R, 0)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
