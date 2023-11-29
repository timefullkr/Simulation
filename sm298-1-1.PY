import pygame
import math
import sys

# Pygame 초기화
pygame.init()

# 상수들
WIDTH, HEIGHT = 1024, 576
gravity = 9.8/10  # 중력 가속도. 스케일은 1:10
restitution = 0.7  # 복원 계수
R = 10  # 공의 반지름
X, Y = R, HEIGHT  # 시작 위치

# 디스플레이 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Simulation")

# 폰트 설정
font = pygame.font.Font(None, 36)

# 입력 필드 및 버튼 상태
input_box1 = pygame.Rect(250, 100, 140, 32)
input_box2 = pygame.Rect(250, 150, 140, 32)
button = pygame.Rect(100, 200, 100, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active1 = False
active2 = False
text1 = ''
text2 = ''
start = False
clock = pygame.time.Clock()

# 레이블 텍스트
label_angle = font.render("Angle:", True, pygame.Color('black'))
label_speed = font.render("Speed:", True, pygame.Color('black'))

# 클래스
class Ball:
    def __init__(self, X, Y, W, H, DX, DY):
        self.x, self.y, self.w, self.h, self.dx, self.dy = X, Y, W, H, DX, DY

    def move(self):
        # 위치 변화
        self.dy += gravity
        self.x += self.dx
        self.y += self.dy

        # 벽 충돌 처리
        if self.x + self.w/2 > WIDTH:
            self.x = WIDTH - self.w/2
            self.dx *= -restitution
        elif self.x - self.w/2 < 0:
            self.x = self.w/2
            self.dx *= -restitution

        if self.y + self.h/2 > HEIGHT:
            self.y = HEIGHT - self.h/2
            self.dy *= -restitution
        elif self.y - self.h/2 < 0:
            self.y = self.h/2
            self.dy *= -restitution

    def display(self):
        pygame.draw.ellipse(screen, (0, 0, 0, 192), (self.x - self.w/2, self.y - self.h/2, self.w, self.h))

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box1.collidepoint(event.pos):
                active1 = True
            else:
                active1 = False
            if input_box2.collidepoint(event.pos):
                active2 = True
            else:
                active2 = False
            if button.collidepoint(event.pos):
                # 시작 버튼 클릭 처리
                try:
                    angle = float(text1)
                    speed = float(text2)
                    dx = speed * math.cos(math.radians(angle))
                    dy = -speed * math.sin(math.radians(angle))
                    ball = Ball(X, Y, R*2, R*2, dx, dy)
                    start = True
                except ValueError:
                    print("Invalid input")
        if event.type == pygame.KEYDOWN:
            if active1:
                if event.key == pygame.K_BACKSPACE:
                    text1 = text1[:-1]
                else:
                    text1 += event.unicode
            if active2:
                if event.key == pygame.K_BACKSPACE:
                    text2 = text2[:-1]
                else:
                    text2 += event.unicode

    screen.fill((220, 220, 220))
    
    # 레이블 그리기
    screen.blit(label_angle, (100, 100))
    screen.blit(label_speed, (100, 150))

    # 텍스트 입력 상자 그리기
    txt_surface1 = font.render(text1, True, pygame.Color('black'))
    txt_surface2 = font.render(text2, True, pygame.Color('black'))
    width = max(200, txt_surface1.get_width()+10)
    input_box1.w = width
    input_box2.w = width
    screen.blit(txt_surface1, (input_box1.x+5, input_box1.y+5))
    screen.blit(txt_surface2, (input_box2.x+5, input_box2.y+5))
    pygame.draw.rect(screen, color, input_box1, 2)
    pygame.draw.rect(screen, color, input_box2, 2)

    # 시작 버튼 그리기
    pygame.draw.rect(screen, color, button)

    if start:
        ball.move()
        ball.display()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
