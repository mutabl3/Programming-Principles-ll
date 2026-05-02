import pygame

def draw_button(screen, font, text, x, y, w, h, color, hover=False):
    pygame.draw.rect(screen, color, (x, y, w, h))
    if hover:
        pygame.draw.rect(screen, (255,255,255), (x, y, w, h), 3)
    text_surf = font.render(text, True, (0,0,0))
    screen.blit(text_surf, (x + w//2 - text_surf.get_width()//2, y + h//2 - text_surf.get_height()//2))

def main_menu(screen, font):
    title_font = pygame.font.Font(None, 72)
    running = True
    while running:
        screen.fill((50,50,50))
        title = title_font.render("RACER GAME", True, (255,255,0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 100))
        
        mx, my = pygame.mouse.get_pos()
        play_hover = (screen.get_width()//2 - 100 <= mx <= screen.get_width()//2 + 100 and
                      250 <= my <= 310)
        lead_hover = (screen.get_width()//2 - 100 <= mx <= screen.get_width()//2 + 100 and
                      330 <= my <= 390)
        settings_hover = (screen.get_width()//2 - 100 <= mx <= screen.get_width()//2 + 100 and
                          410 <= my <= 470)
        quit_hover = (screen.get_width()//2 - 100 <= mx <= screen.get_width()//2 + 100 and
                      490 <= my <= 550)
        
        draw_button(screen, font, "PLAY", screen.get_width()//2 - 100, 250, 200, 60, (0,200,0), play_hover)
        draw_button(screen, font, "LEADERBOARD", screen.get_width()//2 - 100, 330, 200, 60, (0,100,200), lead_hover)
        draw_button(screen, font, "SETTINGS", screen.get_width()//2 - 100, 410, 200, 60, (200,100,0), settings_hover)
        draw_button(screen, font, "QUIT", screen.get_width()//2 - 100, 490, 200, 60, (200,0,0), quit_hover)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_hover:
                    return "play"
                if lead_hover:
                    return "leaderboard"
                if settings_hover:
                    return "settings"
                if quit_hover:
                    return "quit"

def leaderboard_screen(screen, font, leaderboard):
    running = True
    while running:
        screen.fill((30,30,40))
        title = font.render("TOP 10 SCORES", True, (255,255,255))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 50))
        
        y = 120
        for i, entry in enumerate(leaderboard[:10]):
            text = font.render(f"{i+1}. {entry['name']} - Score: {entry['score']} - Distance: {entry['distance']}m", True, (255,255,255))
            screen.blit(text, (50, y))
            y += 40
        
        mx, my = pygame.mouse.get_pos()
        back_hover = (screen.get_width()//2 - 80 <= mx <= screen.get_width()//2 + 80 and
                      screen.get_height() - 80 <= my <= screen.get_height() - 20)
        draw_button(screen, font, "BACK", screen.get_width()//2 - 80, screen.get_height() - 80, 160, 60, (100,100,100), back_hover)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and back_hover:
                return "menu"

def settings_screen(screen, font, settings):
    running = True
    options = ["Sound: ON", "Sound: OFF"]
    sound_idx = 0 if settings["sound"] else 1
    colors = ["red", "blue", "green"]
    color_idx = colors.index(settings["car_color"])
    difficulties = ["easy", "normal", "hard"]
    diff_idx = difficulties.index(settings["difficulty"])
    
    while running:
        screen.fill((40,40,40))
        title = font.render("SETTINGS", True, (255,255,255))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 50))
        
        mx, my = pygame.mouse.get_pos()
        
        sound_hover = (screen.get_width()//2 - 150 <= mx <= screen.get_width()//2 + 150 and 150 <= my <= 210)
        color_hover = (screen.get_width()//2 - 150 <= mx <= screen.get_width()//2 + 150 and 250 <= my <= 310)
        diff_hover = (screen.get_width()//2 - 150 <= mx <= screen.get_width()//2 + 150 and 350 <= my <= 410)
        back_hover = (screen.get_width()//2 - 80 <= mx <= screen.get_width()//2 + 80 and 500 <= my <= 560)
        
        draw_button(screen, font, options[sound_idx], screen.get_width()//2 - 150, 150, 300, 60, (100,100,200), sound_hover)
        draw_button(screen, font, f"Car: {colors[color_idx]}", screen.get_width()//2 - 150, 250, 300, 60, (100,100,200), color_hover)
        draw_button(screen, font, f"Difficulty: {difficulties[diff_idx]}", screen.get_width()//2 - 150, 350, 300, 60, (100,100,200), diff_hover)
        draw_button(screen, font, "BACK", screen.get_width()//2 - 80, 500, 160, 60, (100,100,100), back_hover)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_hover:
                    sound_idx = 1 - sound_idx
                    settings["sound"] = (sound_idx == 0)
                elif color_hover:
                    color_idx = (color_idx + 1) % 3
                    settings["car_color"] = colors[color_idx]
                elif diff_hover:
                    diff_idx = (diff_idx + 1) % 3
                    settings["difficulty"] = difficulties[diff_idx]
                elif back_hover:
                    return "menu"

def game_over_screen(screen, font, score, distance, coins):
    running = True
    while running:
        screen.fill((50,0,0))
        title = font.render("GAME OVER", True, (255,0,0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 80))
        
        info = font.render(f"Score: {score} | Distance: {distance}m | Coins: {coins}", True, (255,255,255))
        screen.blit(info, (screen.get_width()//2 - info.get_width()//2, 200))
        
        mx, my = pygame.mouse.get_pos()
        retry_hover = (screen.get_width()//2 - 180 <= mx <= screen.get_width()//2 - 20 and 300 <= my <= 360)
        menu_hover = (screen.get_width()//2 + 20 <= mx <= screen.get_width()//2 + 180 and 300 <= my <= 360)
        
        draw_button(screen, font, "RETRY", screen.get_width()//2 - 180, 300, 160, 60, (0,150,0), retry_hover)
        draw_button(screen, font, "MENU", screen.get_width()//2 + 20, 300, 160, 60, (150,150,0), menu_hover)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_hover:
                    return "retry"
                if menu_hover:
                    return "menu"

def get_username(screen, font):
    username = ""
    active = True
    while active:
        screen.fill((50,50,70))
        prompt = font.render("ENTER YOUR NAME:", True, (255,255,255))
        screen.blit(prompt, (screen.get_width()//2 - prompt.get_width()//2, 200))
        name_surf = font.render(username + "_", True, (255,255,0))
        screen.blit(name_surf, (screen.get_width()//2 - name_surf.get_width()//2, 280))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "PLAYER"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
    return "PLAYER"