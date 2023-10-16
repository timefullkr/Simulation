import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1024, 576
gravity = 9.8/10  # Acceleration of gravity. Scale 1:10
restitution = 0.7  # Coefficient of restitution
R = 10  # Radius of ball
X, Y = R, HEIGHT//2  # Starting position (x, y)
angle = 30  # Angle of departure
speed = 45  # Speed of ball

# Velocity calculation
dx = speed * math.cos(math.radians(angle))  # Velocity of x
dy = -speed * math.sin(math.radians(angle))  # Velocity of y

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Simulation")
font = pygame.font.Font(None, 36)

# Classes
class Trace:
    def __init__(self, X, Y, W, H):
        self.x, self.y, self.w, self.h = X, Y, W, H

    def display(self):
        pygame.draw.ellipse(screen, (0, 0, 0, 105), (self.x, self.y, self.w, self.h))


class Ball:
    def __init__(self, X, Y, W, H, DX, DY):
        self.x, self.y, self.w, self.h, self.dx, self.dy = X, Y, W, H, DX, DY

    def move(self):
        # Change of position
        self.dy += gravity
        self.x += self.dx
        self.y += self.dy
        # Left & right wall collision
        if self.x + self.w/2 > WIDTH:
            self.x = WIDTH - self.w/2
            self.dx *= -restitution
        elif self.x - self.w/2 < 0:
            self.x = self.w/2
            self.dx *= -restitution
        # Top & bottom wall collision
        if self.y + self.h/2 > HEIGHT:
            self.y = HEIGHT - self.h/2
            self.dy *= -restitution
        elif self.y - self.h/2 < 0:
            self.y = self.h/2
            self.dy *= -restitution

    def display(self):
        pygame.draw.ellipse(screen, (0, 0, 0, 192), (self.x, self.y, self.w, self.h))

# Instantiate classes
trace = [Trace(X, Y, R*2, R*2) for _ in range(100)]
ball = Ball(X, Y, R*2, R*2, dx, dy)
cnt = 0  # Trace count

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((220, 220, 220))
    
    ball.move()
    ball.display()

    # Update trace
    trace[cnt%100] = Trace(ball.x, ball.y, ball.w, ball.h)
    cnt += 1
    for tr in trace:
        tr.display()

    # Display text
    screen.blit(font.render(f"-Gravity={gravity}", True, (0, 0, 0)), (50, 50))
    screen.blit(font.render(f"-Angle={angle}", True, (0, 0, 0)), (50, 70))
    screen.blit(font.render(f"-Speed={speed}", True, (0, 0, 0)), (50, 90))

    # Refresh screen
    pygame.display.flip()
    pygame.time.Clock().tick(30)

# Cleanup
pygame.quit()
sys.exit()
