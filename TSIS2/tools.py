import pygame
import math

def draw_line(surf, start, end, color, size):
    pygame.draw.line(surf, color, start, end, size)

def draw_rectangle(surf, start, end, color, size):
    x1, y1 = start
    x2, y2 = end
    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(surf, color, rect, size)

def draw_square(surf, start, end, color, size):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))
    if x2 >= x1:
        x = x1
    else:
        x = x1 - side
    if y2 >= y1:
        y = y1
    else:
        y = y1 - side
    rect = pygame.Rect(x, y, side, side)
    pygame.draw.rect(surf, color, rect, size)

def draw_circle(surf, start, end, color, size):
    center = start
    radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
    pygame.draw.circle(surf, color, center, radius, size)

def draw_right_triangle(surf, start, end, color, size):
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(surf, color, points, size)

def draw_equilateral_triangle(surf, start, end, color, size):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    height = length * math.sqrt(3) / 2
    if dx == 0:
        p1 = (start[0], start[1] + length)
        p2 = (start[0], start[1] - length)
    else:
        slope = dy / dx
        angle = math.atan(slope)
        p1 = (start[0] + height * math.cos(angle + math.pi/2),
              start[1] + height * math.sin(angle + math.pi/2))
        p2 = (start[0] + height * math.cos(angle - math.pi/2),
              start[1] + height * math.sin(angle - math.pi/2))
    points = [start, p1, p2]
    pygame.draw.polygon(surf, color, points, size)

def draw_rhombus(surf, start, end, color, size):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    dx = abs(end[0] - start[0]) // 2
    dy = abs(end[1] - start[1]) // 2
    points = [(cx, start[1]), (end[0], cy), (cx, end[1]), (start[0], cy)]
    pygame.draw.polygon(surf, color, points, size)

def flood_fill(surf, x, y, target_color, replacement_color):
    if target_color == replacement_color:
        return
    w, h = surf.get_size()
    stack = [(x, y)]
    while stack:
        px, py = stack.pop()
        if px < 0 or px >= w or py < 0 or py >= h:
            continue
        try:
            if surf.get_at((px, py)) == target_color:
                surf.set_at((px, py), replacement_color)
                stack.append((px + 1, py))
                stack.append((px - 1, py))
                stack.append((px, py + 1))
                stack.append((px, py - 1))
        except:
            continue