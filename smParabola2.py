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
restitution = 0.85  # 복원 계수
angle = 45  # 출발 각도
speed = 360  # 공의 속도
ball_friction = 0.8  # 공의 마찰 계수
floor_friction = 0.5  # 바닥의 마찰 계수

# 속도 계산
vx = speed * math.cos(math.radians(angle))
vy = -speed * math.sin(math.radians(angle))

# 디스플레이 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pymunk Physics Simulation")

# Pymunk 공간 생성 및 중력 설정
space = pymunk.Space()
space.gravity = 0, -98
space.damping = 0.97  # 공기 저항

# Font setup for displaying information
font_path = "C:/Windows/Fonts/malgun.ttf"  # 맑은 고딕 폰트 경로 (경로는 시스템에 따라 달라질 수 있음)
font = pygame.font.Font(font_path, 26)

def display_velocity():
    velocity = ball.body.velocity
    velocity_text = f"속도 : ({velocity[0]:.2f}, {velocity[1]:.2f})"
    text_surface = font.render(velocity_text, True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))

def display_first_touch_position(x):
    touch_text = f"거리 : {x}"
    text_surface = font.render(touch_text, True, (0, 0, 0))
    screen.blit(text_surface, (300, 10))

def create_ball(space, position, radius, restitution, velocity):
    mass = 1
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
    body = pymunk.Body(mass, inertia)
    body.position = position
    body.velocity = velocity
    shape = pymunk.Circle(body, radius)
    shape.elasticity = restitution
    shape.friction = ball_friction
    space.add(body, shape)
    return shape



def create_wall(space, p0, p1, restitution, friction):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, p0, p1, 1)
    shape.elasticity = restitution
    shape.friction = friction
    space.add(body, shape)

create_wall(space, (0, HEIGHT), (WIDTH, HEIGHT), restitution, floor_friction)
create_wall(space, (0, 0), (WIDTH, 0), restitution, floor_friction)
create_wall(space, (0, 0), (0, HEIGHT), restitution, ball_friction)
create_wall(space, (WIDTH, 0), (WIDTH, HEIGHT), restitution, ball_friction)

touched_ground = False
touched_ground_x = None  # 처음으로 바닥에 닿았을 때의 x좌표 저장 변수
last_velocity_y = None  # 이전 프레임의 y속도 저장 변수

running = True
ball = create_ball(space, (X, HEIGHT - Y), R, restitution, (vx, vy))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    space.step(1/60)
    
    screen.fill((220, 220, 220))
    x, y = int(ball.body.position.x), int(ball.body.position.y)

    # 공이 바닥에 처음으로 닿았을 때의 x좌표 저장 및 화면에 출력
    if last_velocity_y is not None and last_velocity_y < 0 and ball.body.velocity.y > 0 and not touched_ground:
        touched_ground_x = x
        touched_ground = True

    last_velocity_y = ball.body.velocity.y

    pygame.draw.circle(screen, (0, 0, 0), (x, HEIGHT - y), R, 0)

    if touched_ground_x:
        display_first_touch_position(touched_ground_x)

    # if abs(ball.body.velocity[1]) < 1 and abs(ball.body.velocity[0]) <= 50:
    #     ball.body.velocity = 0, 0
    
    display_velocity()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()