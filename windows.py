import pygame
from settings import WIDTH, HEIGHT

def create_level_complete_window(window, WIDTH, HEIGHT):
    # vytvořeni polopruhledneho cerneho overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128) # nastaveni pruhlednosti
    window.blit(overlay, (0, 0))

    #nacteni obrazku tlacitek
    play_img = pygame.image.load("images/Blue-Square/Play.png").convert_alpha()
    cross_img = pygame.image.load("images/Blue-Square/Cross.png").convert_alpha()
    
    # uprava velikosti
    button_size = 64
    play_img = pygame.transform.scale(play_img, (button_size, button_size))
    cross_img = pygame.transform.scale(cross_img, (button_size, button_size))

    # umisteni tlacitek
    button_spacing = 50 # mezera mezi tlacitky
    play_rect = play_img.get_rect(center=(WIDTH//2 - button_spacing, HEIGHT//2 + 50))
    cross_rect = cross_img.get_rect(center=(WIDTH//2 + button_spacing, HEIGHT//2 + 50))

    # text
    font = pygame.font.Font(None, 72)
    text = font.render("Level Completed!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))

    # vykresleni
    window.blit(text, text_rect)
    window.blit(play_img, play_rect)
    window.blit(cross_img, cross_rect)

    return play_rect, cross_rect

def create_game_over_window(window, WIDTH, HEIGHT):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    window.blit(overlay, (0, 0))

    repeat_img = pygame.image.load("images/Blue-Square/Repeat.png").convert_alpha()
    cross_img = pygame.image.load("images/Blue-Square/Cross.png").convert_alpha()
    
    button_size = 64
    repeat_img = pygame.transform.scale(repeat_img, (button_size, button_size))
    cross_img = pygame.transform.scale(cross_img, (button_size, button_size))

    button_spacing = 50
    repeat_rect = repeat_img.get_rect(center=(WIDTH//2 - button_spacing, HEIGHT//2 + 50)) #posun o 50 dolu
    cross_rect = cross_img.get_rect(center=(WIDTH//2 + button_spacing, HEIGHT//2 + 50))

    font = pygame.font.Font(None, 72)
    text = font.render("Ooops, try again!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))

    window.blit(text, text_rect)
    window.blit(repeat_img, repeat_rect)
    window.blit(cross_img, cross_rect)

    return repeat_rect, cross_rect 