import pygame
import sys
import json
import os
import random
from game import Snake, Food, PowerUp, ObstacleManager
from db import init_db, save_game_result, get_top_10, get_personal_best

pygame.init()
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE GAME")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

SETTINGS_FILE = "settings.json"
default_settings = {"snake_color": [0,255,0], "grid_overlay": True, "sound": False}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return default_settings.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

def draw_button(text, x, y, w, h, color, hover=False):
    pygame.draw.rect(screen, color, (x, y, w, h))
    if hover:
        pygame.draw.rect(screen, (255,255,255), (x, y, w, h), 3)
    surf = font.render(text, True, (0,0,0))
    screen.blit(surf, (x + w//2 - surf.get_width()//2, y + h//2 - surf.get_height()//2))

def get_username():
    username = ""
    while True:
        screen.fill((30,30,40))
        prompt = font.render("ENTER YOUR NAME:", True, (255,255,255))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 200))
        name_surf = font.render(username + "_", True, (255,255,0))
        screen.blit(name_surf, (WIDTH//2 - name_surf.get_width()//2, 280))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "PLAYER"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and username:
                    return username
                elif e.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += e.unicode

def main_menu():
    settings = load_settings()
    while True:
        screen.fill((30,30,40))
        title = pygame.font.Font(None, 72).render("SNAKE GAME", True, (255,255,0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        mx, my = pygame.mouse.get_pos()
        play_hover = (WIDTH//2-100 <= mx <= WIDTH//2+100 and 200 <= my <= 260)
        lead_hover = (WIDTH//2-100 <= mx <= WIDTH//2+100 and 280 <= my <= 340)
        sett_hover = (WIDTH//2-100 <= mx <= WIDTH//2+100 and 360 <= my <= 420)
        quit_hover = (WIDTH//2-100 <= mx <= WIDTH//2+100 and 440 <= my <= 500)
        draw_button("PLAY", WIDTH//2-100, 200, 200, 60, (0,150,0), play_hover)
        draw_button("LEADERBOARD", WIDTH//2-100, 280, 200, 60, (0,100,200), lead_hover)
        draw_button("SETTINGS", WIDTH//2-100, 360, 200, 60, (200,100,0), sett_hover)
        draw_button("QUIT", WIDTH//2-100, 440, 200, 60, (150,0,0), quit_hover)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.MOUSEBUTTONDOWN:
                if play_hover:
                    return "play"
                if lead_hover:
                    leaderboard_screen()
                if sett_hover:
                    settings = settings_screen(settings)
                if quit_hover:
                    return "quit"

def leaderboard_screen():
    rows = get_top_10()
    while True:
        screen.fill((30,30,40))
        title = font.render("TOP 10 SCORES", True, (255,255,255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        y = 120
        for i, row in enumerate(rows):
            text = small_font.render(f"{i+1}. {row[0]} - Score: {row[1]} - Level: {row[2]} - {row[3].strftime('%Y-%m-%d')}", True, (255,255,255))
            screen.blit(text, (50, y))
            y += 40
        mx, my = pygame.mouse.get_pos()
        back_hover = (WIDTH//2-80 <= mx <= WIDTH//2+80 and HEIGHT-80 <= my <= HEIGHT-20)
        draw_button("BACK", WIDTH//2-80, HEIGHT-80, 160, 60, (100,100,100), back_hover)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN and back_hover:
                return

def settings_screen(settings):
    colors = [[0,255,0], [255,0,0], [0,0,255], [255,255,0]]
    color_names = ["Green", "Red", "Blue", "Yellow"]
    color_idx = 0
    for i, c in enumerate(colors):
        if c == settings["snake_color"]:
            color_idx = i
            break
    grid = settings["grid_overlay"]
    sound = settings["sound"]
    while True:
        screen.fill((40,40,40))
        title = font.render("SETTINGS", True, (255,255,255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        mx, my = pygame.mouse.get_pos()
        color_hover = (WIDTH//2-150 <= mx <= WIDTH//2+150 and 150 <= my <= 210)
        grid_hover = (WIDTH//2-150 <= mx <= WIDTH//2+150 and 250 <= my <= 310)
        sound_hover = (WIDTH//2-150 <= mx <= WIDTH//2+150 and 350 <= my <= 410)
        save_hover = (WIDTH//2-80 <= mx <= WIDTH//2+80 and 500 <= my <= 560)
        draw_button(f"Snake: {color_names[color_idx]}", WIDTH//2-150, 150, 300, 60, (100,100,200), color_hover)
        draw_button(f"Grid: {'ON' if grid else 'OFF'}", WIDTH//2-150, 250, 300, 60, (100,100,200), grid_hover)
        draw_button(f"Sound: {'ON' if sound else 'OFF'}", WIDTH//2-150, 350, 300, 60, (100,100,200), sound_hover)
        draw_button("SAVE & BACK", WIDTH//2-80, 500, 160, 60, (0,150,0), save_hover)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return settings
            if e.type == pygame.MOUSEBUTTONDOWN:
                if color_hover:
                    color_idx = (color_idx + 1) % len(colors)
                    settings["snake_color"] = colors[color_idx]
                elif grid_hover:
                    grid = not grid
                    settings["grid_overlay"] = grid
                elif sound_hover:
                    sound = not sound
                    settings["sound"] = sound
                elif save_hover:
                    save_settings(settings)
                    return settings

def game_over_screen(score, level):
    while True:
        screen.fill((50,0,0))
        title = font.render("GAME OVER", True, (255,0,0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        info = font.render(f"Score: {score} | Level: {level}", True, (255,255,255))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, 200))
        mx, my = pygame.mouse.get_pos()
        retry_hover = (WIDTH//2-180 <= mx <= WIDTH//2-20 and 300 <= my <= 360)
        menu_hover = (WIDTH//2+20 <= mx <= WIDTH//2+180 and 300 <= my <= 360)
        draw_button("RETRY", WIDTH//2-180, 300, 160, 60, (0,150,0), retry_hover)
        draw_button("MENU", WIDTH//2+20, 300, 160, 60, (150,150,0), menu_hover)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.MOUSEBUTTONDOWN:
                if retry_hover:
                    return "retry"
                if menu_hover:
                    return "menu"

def run_game(username, settings):
    snake = Snake((GRID_WIDTH//2 * CELL_SIZE, GRID_HEIGHT//2 * CELL_SIZE), settings["snake_color"])
    food = Food(CELL_SIZE)
    poison = Food(CELL_SIZE)
    powerup = PowerUp(CELL_SIZE)
    obstacles = ObstacleManager(CELL_SIZE)
    food.randomize(WIDTH, HEIGHT, snake.body, obstacles.blocks, is_poison=False)
    poison.randomize(WIDTH, HEIGHT, snake.body, obstacles.blocks, is_poison=True)
    powerup.active = False
    score = 0
    level = 1
    food_count = 0
    speed = 10
    last_move = pygame.time.get_ticks()
    move_delay = 1000 // speed
    powerup_effect_end = 0
    powerup_type = None
    shield_active = False
    running = True
    while running:
        now = pygame.time.get_ticks()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and snake.dy == 0:
                    snake.dx, snake.dy = 0, -CELL_SIZE
                elif e.key == pygame.K_DOWN and snake.dy == 0:
                    snake.dx, snake.dy = 0, CELL_SIZE
                elif e.key == pygame.K_LEFT and snake.dx == 0:
                    snake.dx, snake.dy = -CELL_SIZE, 0
                elif e.key == pygame.K_RIGHT and snake.dx == 0:
                    snake.dx, snake.dy = CELL_SIZE, 0
        if now - last_move >= move_delay:
            snake.move()
            last_move = now
            if snake.check_collision(WIDTH, HEIGHT) or snake.check_obstacle_collision(obstacles.blocks):
                if shield_active:
                    shield_active = False
                else:
                    running = False
            if snake.body[0] == food.position:
                score += food.value
                snake.grow()
                food_count += 1
                if food_count >= level * 3:
                    level += 1
                    speed = min(20, speed + 2)
                    move_delay = 1000 // speed
                    obstacles.generate(level, WIDTH, HEIGHT, snake.body)
                    food_count = 0
                food.randomize(WIDTH, HEIGHT, snake.body, obstacles.blocks)
                poison.randomize(WIDTH, HEIGHT, snake.body, obstacles.blocks, is_poison=True)
            if snake.body[0] == poison.position:
                snake.eat_poison()
                if len(snake.body) <= 1:
                    running = False
                poison.randomize(WIDTH, HEIGHT, snake.body, obstacles.blocks, is_poison=True)
            if powerup.active and snake.body[0] == powerup.position:
                powerup_type = powerup.ptype
                if powerup_type == "speed":
                    move_delay = 1000 // (speed + 5)
                    powerup_effect_end = now + 5000
                elif powerup_type == "slow":
                    move_delay = 1000 // max(3, speed - 3)
                    powerup_effect_end = now + 5000
                elif powerup_type == "shield":
                    shield_active = True
                    powerup_effect_end = 0
                powerup.active = False
            if powerup_effect_end and now > powerup_effect_end:
                move_delay = 1000 // speed
                powerup_effect_end = 0
                powerup_type = None
            if not powerup.active and random.random() < 0.005:
                powerup.spawn(WIDTH, HEIGHT, snake.body, obstacles.blocks)
            if powerup.active and powerup.expired(now):
                powerup.active = False
            if food.expired(now):
                food.randomize(WIDTH, HEIGHT, snake.body, obstacles.blocks)
        screen.fill((0,0,0))
        if settings["grid_overlay"]:
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(screen, (40,40,40), (x,0), (x,HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(screen, (40,40,40), (0,y), (WIDTH,y))
        snake.draw(screen, CELL_SIZE)
        food.draw(screen)
        poison.draw(screen)
        powerup.draw(screen)
        obstacles.draw(screen)
        # UI
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        level_text = font.render(f"Level: {level}", True, (255,255,255))
        best_text = small_font.render(f"Best: {get_personal_best(username)}", True, (255,255,0))
        screen.blit(score_text, (10,10))
        screen.blit(level_text, (10,50))
        screen.blit(best_text, (10,90))
        if powerup_type:
            effect_text = small_font.render(f"Power: {powerup_type} {max(0,(powerup_effect_end-now)//1000)}s", True, (0,255,255))
            screen.blit(effect_text, (WIDTH-200, 10))
        if shield_active:
            shield_text = small_font.render("SHIELD ACTIVE", True, (0,255,255))
            screen.blit(shield_text, (WIDTH-200, 50))
        pygame.display.flip()
        clock.tick(60)
    # Game over
    save_game_result(username, score, level)
    return score, level

def main():
    init_db()
    while True:
        action = main_menu()
        if action == "play":
            username = get_username()
            score, level = run_game(username, load_settings())
            action2 = game_over_screen(score, level)
            if action2 == "quit":
                break
        elif action == "quit":
            break

if __name__ == "__main__":
    main()