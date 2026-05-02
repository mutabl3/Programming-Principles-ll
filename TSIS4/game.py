import pygame
import random
import math

class Snake:
    def __init__(self, start_pos, color=(0,255,0)):
        self.body = [start_pos]
        self.dx = 20
        self.dy = 0
        self.color = color
        self.grow_flag = False
        self.speed = 10  

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.dx, head[1] + self.dy)
        self.body.insert(0, new_head)
        if not self.grow_flag:
            self.body.pop()
        else:м
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def check_collision(self, width, height):
        head = self.body[0]
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            return True
        if head in self.body[1:]:
            return True
        return False

    def check_obstacle_collision(self, obstacles):
        return self.body[0] in obstacles

    def eat_poison(self):
        if len(self.body) > 2:
            for _ in range(2):
                if len(self.body) > 1:
                    self.body.pop()
        else:
            self.body = []

    def draw(self, screen, cell_size):
        for segment in self.body:
            pygame.draw.rect(screen, self.color,
                            (segment[0], segment[1], cell_size-2, cell_size-2))

class Food:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.position = (0,0)
        self.value = 1
        self.timer = None
        self.is_poison = False

    def randomize(self, width, height, snake_body, obstacles, is_poison=False):
        self.is_poison = is_poison
        self.value = -1 if is_poison else random.choice([1,2,3])
        if not is_poison and random.random() < 0.3:
            self.timer = pygame.time.get_ticks() + 5000  
        else:
            self.timer = None
        while True:
            x = random.randint(0, (width//self.cell_size)-1) * self.cell_size
            y = random.randint(0, (height//self.cell_size)-1) * self.cell_size
            if (x,y) not in snake_body and (x,y) not in obstacles:
                self.position = (x,y)
                break

    def expired(self, now):
        return self.timer and now > self.timer

    def draw(self, screen):
        color = (255,0,0) if self.is_poison else (255,255,0)
        if self.value == 2:
            color = (255,165,0)
        elif self.value == 3:
            color = (0,255,255)
        pygame.draw.rect(screen, color,
                        (self.position[0], self.position[1], self.cell_size-2, self.cell_size-2))

class PowerUp:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.position = (0,0)
        self.ptype = None
        self.spawn_time = 0
        self.active = False

    def spawn(self, width, height, snake_body, obstacles):
        self.ptype = random.choice(["speed", "slow", "shield"])
        while True:
            x = random.randint(0, (width//self.cell_size)-1) * self.cell_size
            y = random.randint(0, (height//self.cell_size)-1) * self.cell_size
            if (x,y) not in snake_body and (x,y) not in obstacles:
                self.position = (x,y)
                break
        self.spawn_time = pygame.time.get_ticks()
        self.active = True

    def expired(self, now):
        return self.active and now - self.spawn_time > 8000

    def draw(self, screen):
        if not self.active:
            return
        color = {"speed": (0,255,255), "slow": (255,255,0), "shield": (0,100,255)}[self.ptype]
        pygame.draw.rect(screen, color,
                        (self.position[0], self.position[1], self.cell_size-2, self.cell_size-2))

class ObstacleManager:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.blocks = []

    def generate(self, level, width, height, snake_body):
        if level < 3:
            self.blocks = []
            return
        num_blocks = 3 + (level - 3)
        self.blocks = []
        while len(self.blocks) < num_blocks:
            x = random.randint(0, (width//self.cell_size)-1) * self.cell_size
            y = random.randint(0, (height//self.cell_size)-1) * self.cell_size
            if (x,y) not in snake_body and (x,y) not in self.blocks:
                head = snake_body[0]
                if abs(head[0]-x)//self.cell_size + abs(head[1]-y)//self.cell_size > 1:
                    self.blocks.append((x,y))

    def draw(self, screen):
        for block in self.blocks:
            pygame.draw.rect(screen, (100,100,100),
                            (block[0], block[1], self.cell_size-2, self.cell_size-2))