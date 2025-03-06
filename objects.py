import pygame
from os.path import join
from utils import get_block

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height) #vytvoření obdélníku kvuli kolizím
        self.image = pygame.Surface((width, height), pygame.SRCALPHA) #vytvoření průhledného (transparentního) povrchu
        self.width = width
        self.height = height
        self.name = name
    
    def draw(self, surface, offset_x):
        surface.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size, image=None):
        super().__init__(x, y, size, size)
        if image: #pokud je obrázek použit
            self.image.blit(pygame.transform.scale(image, (size, size)), (0, 0))
        else:
            block = get_block(size)
            self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image) #vytvoření masky pro kolize

class WaterBlock(Block):
    def __init__(self, x, y, size, image):
        super().__init__(x, y, size)
        self.is_water = True
        self.original_y = y
        self.rect = pygame.Rect(x, y + size // 4, size, size // 4) #nižši vyška vody než bloku
        water_image = pygame.transform.scale(image, (size, size))
        self.image = water_image

    def draw(self, surface, offset_x):
        # Draw at the original position, not the rect position
        surface.blit(self.image, (self.rect.x - offset_x, self.original_y))

class Door(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        path = join("images", "Object", "door.png")
        door_image = pygame.image.load(path).convert_alpha()
        self.image.blit(pygame.transform.scale(door_image, (size, size)), (0, 0))
        self.trigger_rect = pygame.Rect(x, y, size, size) #obdélník pro detekci kolize s hráčem
        self.is_door = True

    def check_trigger(self, player): #kontrola jestli hráč prošel okolo dveří
        return self.trigger_rect.colliderect(player.rect)