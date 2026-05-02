import pygame
import sys
import datetime
import os
from enum import Enum

pygame.init()
WIDTH, HEIGHT = 1000, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 - Paint Tool")
CLOCK = pygame.time.Clock()

WHITE, BLACK, RED, GREEN, BLUE = (255,255,255), (0,0,0), (255,0,0), (0,255,0), (0,0,255)
GRAY, LIGHT_GRAY = (128,128,128), (200,200,200)
COLORS = [BLACK, RED, GREEN, BLUE]

class Tool(Enum):
    PENCIL = 0
    LINE = 1
    RECT = 2
    SQUARE = 3
    CIRCLE = 4
    RIGHT_TRIANGLE = 5
    RHOMBUS = 6
    ERASER = 7
    FILL = 8
    TEXT = 9

SIZES = {1:2, 2:5, 3:10}
brush = 2
tool = Tool.PENCIL
color = BLACK

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)
font = pygame.font.SysFont("Arial", 24)

# icons
def load_icon(filename, size=(40,40)):
    path = os.path.join("assets", filename)
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    return None

icons = {
    Tool.PENCIL: load_icon("pencil.png"),
    Tool.LINE: load_icon("line.png"),
    Tool.RECT: load_icon("rect.png"),
    Tool.SQUARE: load_icon("square.png"),
    Tool.CIRCLE: load_icon("circle.png"),
    Tool.RIGHT_TRIANGLE: load_icon("triangle.png"),
    Tool.RHOMBUS: load_icon("rhombus.png"),
    Tool.ERASER: load_icon("eraser.png"),
    Tool.FILL: load_icon("fill.png"),
    Tool.TEXT: load_icon("text.png"),
}

def draw_tool_button(x, t, label):
    icon = icons.get(t)
    if icon:
        SCREEN.blit(icon, (x+7, 10))
        if tool == t:
            pygame.draw.rect(SCREEN, (0,255,0), (x, 10, 54, 40), 3)
    else:
        bg = (0,255,0) if tool == t else GRAY
        pygame.draw.rect(SCREEN, bg, (x, 10, 55, 40))
        SCREEN.blit(font.render(label, True, BLACK), (x+5, 22))

drawing = False
start = end = None
preview = None
last_pos = None
text_active, text_pos, text_input = False, None, ""

def draw_ui():
    pygame.draw.rect(SCREEN, LIGHT_GRAY, (0,0,WIDTH,60))
    
    buttons = [
        (10, Tool.PENCIL, "PEN"), (70, Tool.LINE, "LINE"),
        (130, Tool.RECT, "RECT"), (190, Tool.SQUARE, "SQ"),
        (250, Tool.CIRCLE, "CIRC"), (310, Tool.RIGHT_TRIANGLE, "R-TRI"),
        (370, Tool.RHOMBUS, "RHO"), (430, Tool.ERASER, "ERASE"),
        (490, Tool.FILL, "FILL"), (550, Tool.TEXT, "TEXT")
    ]
    
    for x, t, label in buttons:
        draw_tool_button(x, t, label)
    
    # Brush size indicator 
    pygame.draw.rect(SCREEN, GRAY, (620, 10, 100, 40))
    SCREEN.blit(font.render(f"Size:{SIZES[brush]}", True, BLACK), (630, 22))
    
    # Colors
    for i, c in enumerate(COLORS):
        pygame.draw.rect(SCREEN, c, (WIDTH-100+i*25, 10, 25, 25))
        if color == c:
            pygame.draw.rect(SCREEN, BLACK, (WIDTH-100+i*25, 10, 25, 25), 2)
    
    SCREEN.blit(font.render(f"{tool.name}", True, BLACK), (10, HEIGHT-30))

def draw_shape(surf, s, e, col, sz, t):
    if t == Tool.LINE:
        pygame.draw.line(surf, col, s, e, sz)
    elif t == Tool.RECT:
        x1, y1 = s; x2, y2 = e
        pygame.draw.rect(surf, col, (min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1)), sz)
    elif t == Tool.SQUARE:
        x1, y1 = s; x2, y2 = e
        side = min(abs(x2-x1), abs(y2-y1))
        x = x1 if x2 >= x1 else x1 - side
        y = y1 if y2 >= y1 else y1 - side
        pygame.draw.rect(surf, col, (x, y, side, side), sz)
    elif t == Tool.CIRCLE:
        r = int(((e[0]-s[0])**2 + (e[1]-s[1])**2)**0.5)
        pygame.draw.circle(surf, col, s, r, sz)
    elif t == Tool.RIGHT_TRIANGLE:
        points = [s, (s[0], e[1]), e]
        pygame.draw.polygon(surf, col, points, sz)
    elif t == Tool.RHOMBUS:
        cx, cy = (s[0]+e[0])//2, (s[1]+e[1])//2
        dx, dy = abs(e[0]-s[0])//2, abs(e[1]-s[1])//2
        points = [(cx, s[1]), (e[0], cy), (cx, e[1]), (s[0], cy)]
        pygame.draw.polygon(surf, col, points, sz)

def flood_fill(surf, x, y, target, repl):
    if target == repl:
        return
    w, h = surf.get_size()
    stack = [(x, y)]
    while stack:
        px, py = stack.pop()
        if 0 <= px < w and 0 <= py < h and surf.get_at((px, py)) == target:
            surf.set_at((px, py), repl)
            stack.extend([(px+1, py), (px-1, py), (px, py+1), (px, py-1)])

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                brush = [1,2,3][e.key - pygame.K_1]
            elif e.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                name = f"canvas_{datetime.datetime.now():%Y%m%d_%H%M%S}.png"
                pygame.image.save(canvas, name)
                print(f"Saved {name}")
            elif text_active:
                if e.key == pygame.K_RETURN and text_input and text_pos:
                    canvas.blit(font.render(text_input, True, color), text_pos)
                    text_active = False
                    text_input = ""
                    text_pos = None
                elif e.key == pygame.K_ESCAPE:
                    text_active = False
                    text_input = ""
                    text_pos = None
                elif e.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += e.unicode
        elif e.type == pygame.MOUSEBUTTONDOWN:
            x, y = e.pos
            if y < 60:
                buttons = [(10, Tool.PENCIL), (70, Tool.LINE), (130, Tool.RECT), (190, Tool.SQUARE),
                           (250, Tool.CIRCLE), (310, Tool.RIGHT_TRIANGLE), (370, Tool.RHOMBUS),
                           (430, Tool.ERASER), (490, Tool.FILL), (550, Tool.TEXT)]
                for bx, bt in buttons:
                    if bx <= x <= bx+55:
                        tool = bt
                        if tool == Tool.ERASER:
                            color = WHITE
                        elif tool != Tool.ERASER and color == WHITE:
                            color = BLACK
                # Brush size indicator click 
                if 620 <= x <= 720:
                    brush = (brush % 3) + 1
                for i, c in enumerate(COLORS):
                    if WIDTH-100+i*25 <= x <= WIDTH-100+i*25+25:
                        color = c
                continue
            
            if tool == Tool.FILL:
                target = canvas.get_at((x, y))
                if target != color:
                    flood_fill(canvas, x, y, target, color)
            elif tool == Tool.TEXT:
                text_active = True
                text_pos = (x, y)
                text_input = ""
            else:
                drawing = True
                start = (x, y)
                end = (x, y)
                preview = canvas.copy()
                if tool in (Tool.PENCIL, Tool.ERASER):
                    last_pos = (x, y)
        elif e.type == pygame.MOUSEMOTION and drawing:
            x, y = e.pos
            if tool in (Tool.PENCIL, Tool.ERASER) and last_pos:
                pygame.draw.line(canvas, color, last_pos, (x, y), SIZES[brush])
                last_pos = (x, y)
            elif tool not in (Tool.PENCIL, Tool.ERASER):
                end = (x, y)
                preview = canvas.copy()
                draw_shape(preview, start, end, color, SIZES[brush], tool)
        elif e.type == pygame.MOUSEBUTTONUP and drawing:
            if tool not in (Tool.PENCIL, Tool.ERASER):
                draw_shape(canvas, start, e.pos, color, SIZES[brush], tool)
            drawing = False
            last_pos = None

    SCREEN.blit(canvas, (0, 0))
    if drawing and tool not in (Tool.PENCIL, Tool.ERASER):
        SCREEN.blit(preview, (0, 0))
    if text_active and text_pos:
        SCREEN.blit(font.render(text_input + "|", True, color), text_pos)
    draw_ui()
    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()
sys.exit()