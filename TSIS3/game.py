import pygame
import random
import math

class Player:
    def __init__(self, x, y, color="red"):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = color
        self.speed = 5
        self.lane = 1  
        self.lanes = [150, 300, 450]  
        self.x = self.lanes[self.lane]
        self.active_powerup = None
        self.powerup_timer = 0
        self.shield_active = False

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = self.lanes[self.lane]

    def move_right(self):
        if self.lane < 2:
            self.lane += 1
            self.x = self.lanes[self.lane]

    def update(self):
        if self.active_powerup and self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.active_powerup = None
                self.speed = 5

    def apply_powerup(self, ptype):
        if ptype == "nitro":
            self.speed = 10
            self.active_powerup = "nitro"
            self.powerup_timer = 180  
        elif ptype == "shield":
            self.shield_active = True
            self.active_powerup = "shield"
        elif ptype == "repair":
            pass

    def draw(self, screen):
        color_map = {"red": (255,0,0), "blue": (0,0,255), "green": (0,255,0)}
        col = color_map.get(self.color, (255,0,0))
        pygame.draw.rect(screen, col, (self.x - self.width//2, self.y, self.width, self.height))
        if self.shield_active:
            pygame.draw.circle(screen, (0,255,255), (self.x, self.y + self.height//2), 35, 3)

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.speed = speed

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (100,100,100), (self.x - self.width//2, self.y, self.width, self.height))

class Coin:
    def __init__(self, x, y, value=1):
        self.x = x
        self.y = y
        self.radius = 10
        self.value = value

    def update(self):
        self.y += 4

    def draw(self, screen):
        pygame.draw.circle(screen, (255,215,0), (self.x, self.y), self.radius)

class Obstacle:
    def __init__(self, x, y, otype):
        self.x = x
        self.y = y
        self.otype = otype  
        self.width = 40
        self.height = 40

    def update(self):
        self.y += 5

    def draw(self, screen):
        if self.otype == "oil":
            pygame.draw.rect(screen, (50,50,50), (self.x - self.width//2, self.y, self.width, self.height))
        elif self.otype == "hole":
            pygame.draw.rect(screen, (0,0,0), (self.x - self.width//2, self.y, self.width, self.height))
        elif self.otype == "slow":
            pygame.draw.rect(screen, (100,100,200), (self.x - self.width//2, self.y, self.width, self.height))

class PowerUp:
    def __init__(self, x, y, ptype):
        self.x = x
        self.y = y
        self.ptype = ptype  
        self.radius = 15
        self.lifetime = 300

    def update(self):
        self.y += 4
        self.lifetime -= 1

    def is_expired(self):
        return self.lifetime <= 0

    def draw(self, screen):
        colors = {"nitro": (0,255,255), "shield": (0,100,255), "repair": (0,255,0)}
        col = colors.get(self.ptype, (255,255,255))
        pygame.draw.circle(screen, col, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.radius, 2)