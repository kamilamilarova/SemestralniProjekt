import pygame
from utils import load_images, flip
from settings import HEIGHT, PLAYER_VEL
  
class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    TERMINAL_VELOCITY = 10 #maximální rychlost pádu   

    def __init__(self, x, y, folder, blocks, level_width, block_size):
        super().__init__()
        self.LEVEL_WIDTH = level_width #vymezení šířky levelu
        self.BLOCK_SIZE = block_size 
        
        # načtení animací hráče
        self.idle_right = load_images(folder, "Idle")
        self.idle_left = flip(self.idle_right)
        self.run_right = load_images(folder, "Run")
        self.run_left = flip(self.run_right)
        self.jump_right = load_images(folder, "Jump")
        self.jump_left = flip(self.jump_right)
        self.fall_right = load_images(folder, "Fall")
        self.fall_left = flip(self.fall_right)
        
        # Initializace hráče
        self.current_images = self.idle_right #aktuální sada obrázků
        self.image = self.current_images[0] #aktuální obrázek
        self.rect = self.image.get_rect(topleft=(x, y)) #obdélník kolize
        self.true_x = float(x) #přesná pozice hráče (x) float = plynulý pohyb
        self.true_y = float(y) #přesná pozice hráče (y)
        
        # vlastnosti pohybu
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        
        
        self.blocks = blocks #seznam bloků v úrovni
        self.alive = True #jestli je hráč žije
        self.won = False #jestli hráč vyhrál

    def jump(self):
        self.y_vel = -self.GRAVITY * 18 #nastaveni vertikalni rychlosti skoku
        self.animation_count = 0
        self.jump_count += 1 #mozny dvojskok
        if self.jump_count == 1: #reset počitadla pádu pri prvním skoku
            self.fall_count = 0

    def move(self, dx, dy): #aktualizace pozice hráče
        self.true_x += dx
        self.true_y += dy

        #kontrola pravé hranici levelu
        if self.true_x > self.LEVEL_WIDTH - self.BLOCK_SIZE: 
            self.true_x = self.LEVEL_WIDTH - self.BLOCK_SIZE
        
        # převod na int kvuli vykreslení
        self.rect.x = int(self.true_x)
        self.rect.y = int(self.true_y)
        
        if self.rect.left < 0: #kontrola leve hranice obrazovky
            self.rect.left = 0
            self.true_x = float(self.rect.x)
            
        if self.rect.top < 0: #kontrola horní hranice obrazovky
            self.rect.top = 0
            self.true_y = float(self.rect.y)

    def update_direction(self, direction):
        if self.direction != direction: #pokud se měni směr, změní se i obrázky
            self.direction = direction
            self.animation_count = 0

    def check_water_collision(self, objects):
        for obj in objects:
            if hasattr(obj, 'is_water') and obj.is_water:
                if self.rect.colliderect(obj.rect):
                    self.alive = False
                    return True
        return False

    def check_door_collision(self, door):
        if door.check_trigger(self):
            self.won = True
            return True
        return False

    def handle_move(self, keys):
        self.x_vel = 0
        if keys[pygame.K_LEFT]:
            self.update_direction("left")
            self.x_vel = -PLAYER_VEL
        if keys[pygame.K_RIGHT]:
            self.update_direction("right")
            self.x_vel = PLAYER_VEL

    def loop(self, objects):
        if not self.alive or self.won:
            return
            
        self.y_vel = min(self.y_vel + self.GRAVITY, self.TERMINAL_VELOCITY) #aplikovani gravitace
        self.move(self.x_vel, 0)
        self.check_horizontal_collision(objects) #kontrola kolize s bloky
        self.move(0, self.y_vel)
        
        if self.check_water_collision(objects):
            return
            
        self.check_collision(objects)

        self.animation_count += 1
        if self.y_vel < 0: # vyber animace podle stavu hráče
            self.current_images = self.jump_right if self.direction == "right" else self.jump_left
        elif self.y_vel > 0:
            self.current_images = self.fall_right if self.direction == "right" else self.fall_left
        elif self.x_vel != 0:
            self.current_images = self.run_right if self.direction == "right" else self.run_left
        else:
            self.current_images = self.idle_right if self.direction == "right" else self.idle_left

        if self.animation_count >= len(self.current_images) * 5: #resetování animace po dokončeni cyklu
            self.animation_count = 0

        index = self.animation_count // 5 #zpomalení animace
        self.image = self.current_images[index % len(self.current_images)] #cyklické vykreslení obrázků

    def check_collision(self, objects):
        water_blocks = [obj for obj in objects if hasattr(obj, 'is_water')]
        feet_rect = pygame.Rect( #obdelnik pro detekci nohou hrace
            self.rect.x,
            self.rect.bottom - 10,  # kontrola pouze spodnich 10 pixelu hráče
            self.rect.width,
            10
        )
        
        for water in water_blocks: #kontrola kolize doteku hrace s vodou
            if feet_rect.colliderect(water.rect):
                self.alive = False
                return
            
        colliding_blocks = [obj for obj in objects if not hasattr(obj, 'is_water')] #seznam pevných bloků
        
        on_ground = False
        for block in colliding_blocks: #kontrola kolize hrace s bloky
            if self.rect.colliderect(block.rect):
                if self.y_vel > 0: # padání
                    self.rect.bottom = block.rect.top #zastavení na vrcholu bloku
                    self.true_y = float(self.rect.y) 
                    self.landed() 
                    on_ground = True
                elif self.y_vel < 0:  # skákání
                    self.rect.top = block.rect.bottom #náraz hlavou do bloku
                    self.true_y = float(self.rect.y)
                    self.hit_head()

        if not on_ground:
            self.fall_count += 1

    def check_horizontal_collision(self, objects):
        colliding_blocks = [obj for obj in objects if not hasattr(obj, 'is_water') and not hasattr(obj, 'is_door')] #kromě vody a dveří
        
        for block in colliding_blocks:
            if self.rect.colliderect(block.rect):
                if self.x_vel > 0: #pohyb vpravo
                    self.rect.right = block.rect.left # zastavení u leve strany bloku
                    self.true_x = float(self.rect.x)
                    self.x_vel = 0
                elif self.x_vel < 0: # pohyb vlevo
                    self.rect.left = block.rect.right # zastavení u prave strany bloku
                    self.true_x = float(self.rect.x)
                    self.x_vel = 0

    def landed(self): #reset pocitadel pri přistani
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self): #zastavení vertikalni rychlosti pri nárazu hlavou
        self.y_vel = 0

    def draw(self, win, offset_x): #vykreslení hráče s ohledem na camera scroll
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

    def check_coin_collisions(self, coins): #kontrola sbíraní mincí
        for coin in coins:
            if not coin.collected and self.rect.colliderect(coin.rect):
                coin.collected = True
                return True
        return False

