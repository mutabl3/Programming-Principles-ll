import pygame
import sys
import math
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

def draw_clock_face():
    pygame.draw.circle(screen, WHITE, (CENTER_X, CENTER_Y), 250, 0)
    pygame.draw.circle(screen, BLACK, (CENTER_X, CENTER_Y), 250, 3)
    
    for hour in range(12):
        angle = math.radians(90 - hour * 30)  
        x1 = CENTER_X + 230 * math.cos(angle)
        y1 = CENTER_Y - 230 * math.sin(angle)
        x2 = CENTER_X + 210 * math.cos(angle)
        y2 = CENTER_Y - 210 * math.sin(angle)
        pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 5)
    
    for minute in range(60):
        angle = math.radians(90 - minute * 6) 
        x1 = CENTER_X + 235 * math.cos(angle)
        y1 = CENTER_Y - 235 * math.sin(angle)
        x2 = CENTER_X + 225 * math.cos(angle)
        y2 = CENTER_Y - 225 * math.sin(angle)
        pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 2)
    
    pygame.draw.circle(screen, BLACK, (CENTER_X, CENTER_Y), 15)

def draw_mickey_hand(angle, length, width):
    rad = math.radians(90 - angle)
    x = CENTER_X + length * math.cos(rad)
    y = CENTER_Y - length * math.sin(rad)
    
    # Рисуем линию (руку)
    pygame.draw.line(screen, BLACK, (CENTER_X, CENTER_Y), (x, y), width)
    # Рисуем перчатку на конце
    pygame.draw.circle(screen, BLACK, (int(x), int(y)), width + 4)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    now = datetime.now()
    seconds = now.second
    minutes = now.minute + seconds / 60.0
    hours = now.hour % 12 + minutes / 60.0
    
    seconds_angle = seconds * 6       
    minutes_angle = minutes * 6        
    hours_angle = hours * 30           
    
    screen.fill((240, 240, 240))  
    draw_clock_face()
    
    draw_mickey_hand(hours_angle, 120, 8)      # часовая
    draw_mickey_hand(minutes_angle, 180, 6)    # минутная
    draw_mickey_hand(seconds_angle, 210, 3)    # секундная
    
    font = pygame.font.Font(None, 36)
    time_text = font.render(f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}", True, BLACK)
    screen.blit(time_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()