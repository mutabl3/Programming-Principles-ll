import pygame
import sys
import random
from persistence import load_leaderboard, save_leaderboard, add_score, load_settings, save_settings
from ui import main_menu, leaderboard_screen, settings_screen, game_over_screen, get_username
from game import Player, Enemy, Coin, Obstacle, PowerUp

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RACER GAME")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def run_game(settings):
    lanes = [150, 300, 450]
    player = Player(300, 500, settings["car_color"])
    
    enemies = []
    coins = []
    obstacles = []
    powerups = []
    
    score = 0
    distance = 0
    coins_collected = 0
    enemy_speed = 3
    spawn_counter = 0
    difficulty = settings["difficulty"]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()
        
        spawn_counter += 1
        if spawn_counter > 30:
            spawn_counter = 0
            if random.random() < 0.3:
                lane = random.randint(0,2)
                x = lanes[lane]
                enemies.append(Enemy(x, -60, enemy_speed))
            if random.random() < 0.2:
                lane = random.randint(0,2)
                x = lanes[lane]
                coins.append(Coin(x, -20, random.choice([1,2,3])))
            if random.random() < 0.15:
                lane = random.randint(0,2)
                x = lanes[lane]
                otype = random.choice(["oil", "hole", "slow"])
                obstacles.append(Obstacle(x, -40, otype))
            if random.random() < 0.05:
                lane = random.randint(0,2)
                x = lanes[lane]
                ptype = random.choice(["nitro", "shield", "repair"])
                powerups.append(PowerUp(x, -30, ptype))
        
        player.update()
        for e in enemies[:]:
            e.update()
            if e.y > HEIGHT:
                enemies.remove(e)
            if (abs(player.x - e.x) < 40 and abs(player.y - e.y) < 60):
                if player.shield_active:
                    player.shield_active = False
                    player.active_powerup = None
                    enemies.remove(e)
                else:
                    running = False
        
        for c in coins[:]:
            c.update()
            if c.y > HEIGHT:
                coins.remove(c)
            if abs(player.x - c.x) < 30 and abs(player.y - c.y) < 40:
                coins_collected += c.value
                score += c.value * 10
                coins.remove(c)
        
        for o in obstacles[:]:
            o.update()
            if o.y > HEIGHT:
                obstacles.remove(o)
            if abs(player.x - o.x) < 30 and abs(player.y - o.y) < 50:
                if o.otype == "oil":
                    player.speed = max(2, player.speed - 2)
                elif o.otype == "hole":
                    running = False
                elif o.otype == "slow":
                    player.speed = max(2, player.speed - 1)
                obstacles.remove(o)
        
        for p in powerups[:]:
            p.update()
            if p.is_expired() or p.y > HEIGHT:
                powerups.remove(p)
            if abs(player.x - p.x) < 25 and abs(player.y - p.y) < 35:
                player.apply_powerup(p.ptype)
                if p.ptype == "repair":
                    score += 50
                powerups.remove(p)
        
        distance += player.speed
        score = coins_collected * 10 + distance // 10
        
        if difficulty == "easy":
            enemy_speed = 3 + coins_collected // 20
        elif difficulty == "normal":
            enemy_speed = 4 + coins_collected // 15
        else:
            enemy_speed = 5 + coins_collected // 10
        
        screen.fill((30,30,30))

        for lane_x in lanes:
            pygame.draw.line(screen, (100,100,100), (lane_x, 0), (lane_x, HEIGHT), 3)
        
        player.draw(screen)
        for e in enemies:
            e.draw(screen)
        for c in coins:
            c.draw(screen)
        for o in obstacles:
            o.draw(screen)
        for p in powerups:
            p.draw(screen)
        
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        dist_text = font.render(f"Distance: {distance//10}m", True, (255,255,255))
        coin_text = font.render(f"Coins: {coins_collected}", True, (255,215,0))
        screen.blit(score_text, (10,10))
        screen.blit(dist_text, (10,50))
        screen.blit(coin_text, (10,90))
        
        if player.active_powerup:
            power_text = font.render(f"Power: {player.active_powerup} {player.powerup_timer//60}s", True, (0,255,255))
            screen.blit(power_text, (WIDTH - 200, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    return score, distance, coins_collected

def main():
    settings = load_settings()
    while True:
        action = main_menu(screen, font)
        if action == "play":
            username = get_username(screen, font)
            score, distance, coins = run_game(settings)
            add_score(username, score, distance)
            action2 = game_over_screen(screen, font, score, distance, coins)
            if action2 == "quit":
                break
            elif action2 == "menu":
                continue
            elif action2 == "retry":
                continue
        elif action == "leaderboard":
            lb = load_leaderboard()
            leaderboard_screen(screen, font, lb)
        elif action == "settings":
            settings_screen(screen, font, settings)
            save_settings(settings)
        elif action == "quit":
            break

if __name__ == "__main__":
    main()