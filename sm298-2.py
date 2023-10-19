import pygame
import math
import sys

pygame.init()

# 화면의 너비와 높이 설정
WIDTH, HEIGHT = 1024, 576
gravity = 9.8/10  # 중력 가속도. 스케일 1:10
restitution = 0.7  # 탄성 계수 
R = 10  # 공의 반지름
X, Y = R, HEIGHT//2  # 시작 위치 (x, y)
angle = 30  # 발사 각도
speed = 45  # 공의 속도

# 속도 계산
dx = speed * math.cos(math.radians(angle))  # x축 속도
dy = -speed * math.sin(math.radians(angle))  # y축 속도

# 디스플레이 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("물리 시뮬레이션")
font = pygame.font.Font(None, 36)

# 클래스 정의
class Trace:
    def __init__(self, X, Y, W, H):
        self.x, self.y, self.w, self.h = X, Y, W, H

    def display(self):
        pygame.draw.ellipse(screen, (0, 0, 0, 105), (self.x, self.y, self.w, self.h))

class Ball:
    def __init__(self, X, Y, W, H, DX, DY):
        self.x, self.y, self.w, self.h, self.dx, self.dy = X, Y, W, H, DX, DY

    def move(self):
        # 위치 변화
        self.dy += gravity
        self.x += self.dx
        self.y += self.dy

        # 왼쪽 & 오른쪽 벽 충돌
        if self.x + self.w/2 > WIDTH:
            self.x = WIDTH - self.w/2
            self.dx *= -restitution
        elif self.x - self.w/2 < 0:
            self.x = self.w/2
            self.dx *= -restitution
        # 상단 & 하단 벽 충돌
        if self.y + self.h/2 > HEIGHT:
            self.y = HEIGHT - self.h/2
            self.dy *= -restitution
        elif self.y - self.h/2 < 0:
            self.y = self.h/2
            self.dy *= -restitution

    def display(self):
        pygame.draw.ellipse(screen, (0, 0, 0, 192), (self.x, self.y, self.w, self.h))

# 클래스 인스턴스 생성
trace = [Trace(X, Y, R*2, R*2) for _ in range(100)]
ball = Ball(X, Y, R*2, R*2, dx, dy)
cnt = 0  # 궤적 카운트

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((220, 220, 220))
    
    ball.move()
    ball.display()

    # 궤적 업데이트
    trace[cnt%100] = Trace(ball.x, ball.y, ball.w, ball.h)
    cnt += 1
    for tr in trace:
        tr.display()

    # 텍스트 표시
    screen.blit(font.render(f"-중력={gravity}", True, (0, 0, 0)), (50, 50))
    screen.blit(font.render(f"-각도={angle}", True, (0, 0, 0)), (50, 70))
    screen.blit(font.render(f"-속도={speed}", True, (0, 0, 0)), (50, 90))

    # 화면 갱신
    pygame.display.flip()
    pygame.time.Clock().tick(30)

# 정리
pygame.quit()
sys.exit()
