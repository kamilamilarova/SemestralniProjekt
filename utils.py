import pygame
from os import listdir
from os.path import isfile, join

def flip(images): #převrácení obrázků
    return [pygame.transform.flip(image, True, False) for image in images]

def load_images(base_folder, sub_folder=None, scale_factor=0.20): #načtení obrázků
    path = join("images", "characters", base_folder) #cesta k obrázkům
    if sub_folder:
        path = join(path, sub_folder)
    images = [f for f in listdir(path) if isfile(join(path, f))] #seznam obrázků
    loaded_images = [pygame.transform.scale(  #načteni a změna velikosti obrázků
        pygame.image.load(join(path, img)).convert_alpha(),
        (int(pygame.image.load(join(path, img)).get_width() * scale_factor),
         int(pygame.image.load(join(path, img)).get_height() * scale_factor))
    ) for img in images]
    return loaded_images

def get_block(size):
    path = join("images", "Tiles", "2.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32) #transparentni povrch
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect) #vykreslení obrázku na povrch
    return pygame.transform.scale2x(surface) #zvětšení obrázku

def get_background(name):
    return pygame.image.load(join("images", "BG", name)).convert_alpha()