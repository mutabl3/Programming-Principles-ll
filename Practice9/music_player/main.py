import pygame
import os
from player import MusicPlayer

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Music Player")
font = pygame.font.SysFont("Arial", 24)

base_path = os.path.dirname(__file__)
music_folder = os.path.join(base_path, 'music')
player = MusicPlayer(music_folder)

running = True
while running:
    screen.fill((30, 30, 30)) 
    
    info_text = player.get_current_info()
    text_surf = font.render(info_text, True, (255, 255, 255))
    screen.blit(text_surf, (50, 150))
    
    controls_text = "P: Play | S: Stop | N: Next | B: Back | Q: Quit"
    ctrl_surf = font.render(controls_text, True, (150, 150, 150))
    screen.blit(ctrl_surf, (50, 300))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play_track()
            elif event.key == pygame.K_s:
                player.stop_track()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.prev_track()
            elif event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()