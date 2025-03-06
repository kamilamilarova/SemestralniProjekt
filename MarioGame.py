import pygame
from settings import *
from player import Player
from objects import Block, WaterBlock, Door
from coins import Coin
from windows import create_level_complete_window, create_game_over_window
from utils import get_background, load_level
from os.path import join
from enemy import Enemy

def draw(window, background, player, objects, coins, enemies, door, offset_x, score, font, level):
    window.blit(background, (0, 0))
          
    for coin in coins:
        coin.draw(window, offset_x)
    
    for obj in objects:
        obj.draw(window, offset_x)

    door.draw(window, offset_x)

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
    
    # Load water image
    water_path = join("images", "Tiles", "17.png")
    water_image = pygame.image.load(water_path).convert_alpha()
    
    # Load level data
    level_data = load_level(level)
    objects = []
    coins = []
    enemies = []
    player_start = None
    door = None
    score = 0
    
    # Process level data
    for row_idx, row in enumerate(level_data):
        for col_idx, char in enumerate(row):
            x = col_idx * BLOCK_SIZE
            y = row_idx * BLOCK_SIZE
        
            if char == '=':  # Ground and platforms
                objects.append(Block(x, y, BLOCK_SIZE))
            elif char == '_':  # Water
                objects.append(WaterBlock(x, y, BLOCK_SIZE, water_image))
            elif char == 'C':  # Coin
                coins.append(Coin(x, y))
            elif char == 'E':  # Enemy
                platform_start = x - BLOCK_SIZE * 2
                platform_end = x + BLOCK_SIZE * 2
                enemy_y = y + BLOCK_SIZE - BLOCK_SIZE
                enemies.append(Enemy(x, enemy_y, BLOCK_SIZE, platform_start, platform_end))
            elif char == '&':  # Door
                door = Door(x, y, BLOCK_SIZE)
            elif char == 'H':  # Player starting position
                player_start = (x, y)
    
    # If not player position specified in level, use default
    if not player_start:
        player_start = (100, HEIGHT - BLOCK_SIZE * 2)
    
    player = Player(player_start[0], player_start[1], "cat", objects, LEVEL_WIDTH, BLOCK_SIZE)
    
    # Camera setup
    offset_x = 0
    scroll_area_width = 200
    
    # UI setup
    font = pygame.font.Font(None, 36)
    play_rect = None
    cross_rect = None
    
    # Find rightmost object for max scroll
    last_x = max([obj.rect.right for obj in objects])
    max_scroll = last_x - WIDTH
    
    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONUP:
                if player.won or not player.alive:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_rect and play_rect.collidepoint(mouse_pos):
                        if player.won:
                            run = False
                            main(window, level + 1)
                            return
                        else:
                            run = False
                            main(window, level)
                    elif cross_rect and cross_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
        
        if player.alive and not player.won:
            keys = pygame.key.get_pressed()
            player.handle_move(keys)
            player.loop(objects)
            
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
            
            # Camera movement
            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0):
                if offset_x < max_scroll:
                    offset_x += player.x_vel
            elif ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel
            
            offset_x = max(0, min(max_scroll, offset_x))
        
        (play_rect, cross_rect), is_win = draw(window, background, player, objects, coins, enemies, door, offset_x, score, font, level)
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main(window, 1)