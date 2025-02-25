import pygame
import random
import math
from os.path import join
from settings import HEIGHT

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        path = join("images", "Gold", "Gold_1.png")
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40)) #změna velikosti mince
        self.rect = self.image.get_rect(topleft=(x, y)) #nastavení pozice mince
        self.start_y = y #počáteční pozice mince(vznášení)

        # Animace mince
        self.float_offset = 0
        self.float_speed = 0.05 
        self.float_range = 10 
        self.collected = False #zda byla mince sebrána

    def animate(self): #vytvoření animace mince
        if not self.collected:
            self.float_offset += self.float_speed #pomoci sinusové funkce
            self.rect.y = self.start_y + math.sin(self.float_offset) * self.float_range

    def draw(self, window, offset_x): #vykreslení mince
        if not self.collected:
            window.blit(self.image, (self.rect.x - offset_x, self.rect.y))

def spawn_coins(num_coins, objects, block_size, last_platform_x):
    coins = [] #seznam mincí
    min_spacing = 100
    max_x = last_platform_x  # dveře jako hranice pro mince
    
    for _ in range(num_coins):
        while True:
            x = random.randint(block_size * 2, max_x - block_size)  # mince se mohou objevit pouze mezi první a poslední platformou
            y = random.randint(HEIGHT // 2, HEIGHT - block_size * 2) # mince se mohou objevit pouze mezi polovinou obrazovky a zemí
            valid_position = True
            
            for coin in coins: #kontrola jestli se mince nepřekrývají
                if abs(coin.rect.x - x) < min_spacing and abs(coin.rect.y - y) < min_spacing:
                    valid_position = False
                    break
            
            test_rect = pygame.Rect(x, y, 40, 40) #kontrola jestli neni mince uprostřed bloku
            for obj in objects:
                if test_rect.colliderect(obj.rect):
                    valid_position = False
                    break
            
            if valid_position: #pokud je pozice mince v poradku, vytvoří se mince
                coins.append(Coin(x, y))
                break
    
    return coins
