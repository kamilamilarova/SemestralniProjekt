import pygame
import random
from settings import *
from player import Player
from objects import Block, WaterBlock, Door
from coins import spawn_coins, Coin
from windows import create_level_complete_window, create_game_over_window
from utils import get_background
from os.path import join
from enemy import Enemy

def draw(window, background, player, objects, coins, enemies, offset_x, score, font, level):
    window.blit(background, (0, 0))
          
    for coin in coins:
        coin.draw(window, offset_x)
    
    for obj in objects:
        obj.draw(window, offset_x)

    for enemy in enemies:
        enemy.draw(window, offset_x)
    
    player.draw(window, offset_x)
    
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    window.blit(score_text, (10, 10))
    level_text = font.render(f"Level {level}", True, (0, 0, 0))
    window.blit(level_text, (WIDTH - 120, 10))

    if player.won:
        return create_level_complete_window(window, WIDTH, HEIGHT), True
    elif not player.alive:
        return create_game_over_window(window, WIDTH, HEIGHT), False
        
    return (None, None), None   

def main(window, level=1):
    clock = pygame.time.Clock()
    background = get_background("BG.png")
    random.seed(level) #dostaneme stejne nahodne rozmisteni (diky čisla levelu)

    water_path = join("images", "Tiles", "17.png")
    water_image = pygame.image.load(water_path).convert_alpha()
    
    platform_positions = [] #generování platforem
    last_x = BLOCK_SIZE * 3 #tri pozice od startu prvni platforma
    min_gap = 3
    max_gap = 4
    platform_heights = [
        HEIGHT - BLOCK_SIZE * 3,
        HEIGHT - BLOCK_SIZE * 4
    ]

    while len(platform_positions) < 9: #nahodne rozmisteni platforem
        gap = random.randint(min_gap, max_gap) * BLOCK_SIZE
        last_x += gap
        platform_y = random.choice(platform_heights)
        platform_positions.append((last_x, platform_y))

    floor = []
    last_platform_x = platform_positions[-1][0] #najde pozici posledni platformy
    
    i = 0
    while i < LEVEL_WIDTH // BLOCK_SIZE:
        if i <= 1 or i >= (last_platform_x // BLOCK_SIZE) - 1: # na zacatku a na konci levelu je pevna zem 
            floor.append(Block(i * BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE))
            i += 1
        else:
            if i + 1 < (last_platform_x // BLOCK_SIZE) - 1:
                if random.random() < 0.3: # 30% šance na vodu
                    floor.append(WaterBlock(i * BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE, water_image))
                    floor.append(WaterBlock((i+1) * BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE, water_image))
                    i += 2
                else:
                    floor.append(Block(i * BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE))
                    i += 1
            else:
                floor.append(Block(i * BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE))
                i += 1

    #koncove dvere
    door = Door(last_platform_x, HEIGHT - BLOCK_SIZE * 2, BLOCK_SIZE)
    objects = [*floor, door]

    for pos in platform_positions:
        objects.append(Block(pos[0], pos[1], BLOCK_SIZE))
    

    ground_sections = []
    current_section = []

    # najdi sekce zeme
    for i, block in enumerate(floor):
        if not hasattr(block, 'is_water'):  # jestli je to pevna zem
            current_section.append(block)
        else:
            if len(current_section) >= 4:  # Sekce je dostatecne dlouha
                ground_sections.append(current_section)
            current_section = []

    # posledni sekce
    if len(current_section) >= 4:
        ground_sections.append(current_section)

    # vytvori nepritele na zemi
    enemies = []
    player_safe_zone = BLOCK_SIZE * 4  # bezpecna zona na zacatku levelu
    for section in ground_sections:
        if section[0].rect.x < player_safe_zone:
            continue
        if random.random() < 0.8:  # 80% sance objeveni nepritele
            start_x = section[0].rect.x
            end_x = section[-2].rect.x + BLOCK_SIZE #dva bloky od kraje
            enemy = Enemy(
                start_x, #počatecni pozice
                HEIGHT - BLOCK_SIZE * 1.75,  # nepritel na zemi
                BLOCK_SIZE,
                start_x, #leva hranice
                end_x
            )
            enemies.append(enemy)

    player = Player(100, HEIGHT - BLOCK_SIZE * 2, "cat", objects, LEVEL_WIDTH, BLOCK_SIZE)
    coins = spawn_coins(10, objects, BLOCK_SIZE, last_platform_x)
    score = 0

    #nastavení scroll camera
    offset_x = 0
    scroll_area_width = 200 #zona na okrajich obrazovky, ktera spusti scroll

    font = pygame.font.Font(None, 36)
    initial_player_pos = (100, HEIGHT - BLOCK_SIZE * 2) #vychozi pozice hrace
    initial_coins = coins.copy()
    initial_enemies = enemies.copy()
    play_rect = None
    cross_rect = None
    

    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ukončení hry krizkem
                run = False

            #kliknutí na tlačitka
            if event.type == pygame.MOUSEBUTTONUP:
                if player.won or not player.alive:
                    mouse_pos = pygame.mouse.get_pos() #získání pozice touchpadu
                    if play_rect and play_rect.collidepoint(mouse_pos):
                        if player.won: #pokud hráč vyhrál, spustí se nová hra
                            run = False
                            main(window, level + 1) #přidání levelu a spuštění hry znovu
                            return
                        else: 
                            run = False
                            main(window, level) #reset levelu
                    elif cross_rect and cross_rect.collidepoint(mouse_pos): 
                        pygame.quit()
                        exit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        ## Aktualizace herní logiky (pouze když hráč žije a nevyhrál)
        if player.alive and not player.won:
            keys = pygame.key.get_pressed() #zjisti ktere klavesy jsou stisknute
            player.handle_move(keys) # podle toho zpracuje pohyb hrace
            player.loop(objects) #aktualizuje kolize s objekty 

            for coin in coins: 
                coin.animate()
            if player.check_coin_collisions(coins): 
                score += 1
            if player.check_door_collision(door): 
                player.won = True

            for enemy in enemies:
                enemy.update()
                if enemy.check_collision(player):
                    break

            max_scroll = last_platform_x + BLOCK_SIZE - WIDTH
    
            #posun kamery doprava a doleva
            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0):
                if offset_x < max_scroll:
                    offset_x += player.x_vel
            elif ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel

            offset_x = max(0, min(max_scroll, offset_x))

        # Vykreslení vsech prvků
        (play_rect, cross_rect), is_win = draw(window, background, player, objects, coins, enemies, offset_x, score, font, level)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main(window, 1)
