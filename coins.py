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

