import pygame
from os.path import join
from utils import load_images, flip

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, platform_start, platform_end):
        super().__init__()
        # animace nepritele
        self.walk_right = load_images("dog", "Walk", scale_factor=0.15)
        self.walk_left = flip(self.walk_right)
        
        #nastaveni vzhledu
        self.current_images = self.walk_right #aktualni sada animací
        self.image = self.current_images[0] #aktualni obrazek
        self.rect = self.image.get_rect(topleft=(x, y))
        self.true_x = float(x)
        
        # nastaeni pohybu
        self.speed = 2
        self.direction = "right"
        self.animation_count = 0
        
        # hranice pohybu
        self.platform_start = platform_start
        self.platform_end = platform_end
        
    def move(self):
        if self.direction == "right":
            self.true_x += self.speed
            if self.true_x >= self.platform_end: #dosazeni prave hranice
                self.direction = "left"
                self.current_images = self.walk_left
        else:
            self.true_x -= self.speed
            if self.true_x <= self.platform_start: #dosazeni leve hranice
                self.direction = "right"
                self.current_images = self.walk_right
                
        self.rect.x = int(self.true_x)
        
    def animate(self): #aktualizace animace nepritele
        self.animation_count += 1
        if self.animation_count >= len(self.current_images) * 5:
            self.animation_count = 0
            
        index = self.animation_count // 5 #zpomaleni animace
        self.image = self.current_images[index % len(self.current_images)]
        
    def update(self):
        self.move()
        self.animate()
        
    def draw(self, window, offset_x):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))
        

    def check_collision(self, player):
    # box na kolize
        enemy_collision = pygame.Rect(
            self.rect.x + 10,  
            self.rect.y + 5,
            self.rect.width - 20,
            self.rect.height - 10
        )
    
        # box na kolize
        player_collision = pygame.Rect(
            player.rect.x + 10,
            player.rect.y + 5,
            player.rect.width - 20,
            player.rect.height - 10
        )
    
        if enemy_collision.colliderect(player_collision):
            player.alive = False
            return True
        return False