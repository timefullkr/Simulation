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
X, Y = R, HEIGHT//2 # Starting position (x, y)
angle = 45  # 출발 각도
speed = 45  # 공의 속도

# 속도 계산
dx = speed * math.cos(math.radians(angle))  # x 축의 속도
dy = -speed * math.sin(math.radians(angle))  # y 축의 속도

# 디스플레이 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Simulation")


# 클래스
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

        # 위 & 아래 벽 충돌
        if self.y + self.h/2 > HEIGHT:
            self.y = HEIGHT - self.h/2
            self.dy *= -restitution
        elif self.y - self.h/2 < 0:
            self.y = self.h/2
            self.dy *= -restitution

    def display(self):
        pygame.draw.ellipse(screen, (0, 0, 0, 192), (self.x - self.w/2, self.y - self.h/2, self.w, self.h))

# 클래스 인스턴스 생성
ball = Ball(X, Y, R*2, R*2, dx, dy)

# 메인 루프
running = True
index=0
while running:
    for event in pygame.event.get():  
            if event.type == pygame.QUIT: 
                running = False  

    #if index==2 :
    #    continue
    screen.fill((220, 220, 220))
    
    ball.move()
    ball.display()

    # 화면 갱신
    pygame.display.flip()
    pygame.time.Clock().tick(30)
    index +=1
   
# 정리
pygame.quit()
sys.exit()
