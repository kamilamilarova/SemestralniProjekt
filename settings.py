import pygame
import os
pygame.init()
pygame.mixer.init()

# nastaveni okna
WIDTH = 1000
HEIGHT = 800
FPS = 60 #frames per sec
PLAYER_VEL = 5

# vytvoreni okna
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kocourek")

# nastaveni bloku
BLOCK_SIZE = 96
LEVEL_WIDTH = WIDTH * 10 #hra 10x delsi nez okno

# barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#hudba
pygame.mixer.music.load("music/pisnicka.mp3")
pygame.mixer.music.play(-1) #nekonecna smycka
