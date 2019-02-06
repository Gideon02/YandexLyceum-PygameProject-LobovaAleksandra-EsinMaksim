import os
import pygame
import math

pygame.init()

size = width, height = 1000, 600

JUMP_POWER = 25
STAIR_POWER = 15
MOVE_SPEED = 15
GRAVITY = 5
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(players)
        self.init_image(pos)
        self.init_info()
        
    def init_image(self, pos):
        self.image = pygame.Surface((24, 48))
        pygame.draw.rect(self.image, (40, 40, 40), (0, 0, 24, 48))
        self.rect = pygame.Rect(0, 0, 24, 48)
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.rect.w, self.rect.h = 24, 48
    
    def init_info(self):
        self.onGround, self.onStair, self.up, self.left, self.right = False, False, False, False, False
        self.xvel, self.yvel, self.count = 0, 0, 0
        self.health = 10
                
    def update(self, left, right, up, platforms, stairs):
        if up:
            if self.onStair:
                self.yvel = -STAIR_POWER
            elif self.onGround: 
                self.yvel = -JUMP_POWER
        if left:
            self.xvel = -MOVE_SPEED 
        if right:
            self.xvel = MOVE_SPEED
        if not(right or left):
            self.xvel = 0
        if not self.onGround:
            self.yvel += GRAVITY
            
        if pygame.sprite.spritecollideany(self, stairs):
            self.onStair = True
        else:
            self.onStair = False

        self.onGround = False   
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, stairs)

        self.rect.x += self.xvel 
        self.collide(self.xvel, 0, platforms, stairs)

    def collide(self, xvel, yvel, platforms, stairs):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:                      
                    self.rect.right = p.rect.left 
                if xvel < 0:                      
                    self.rect.left = p.rect.right 
                if yvel > 0:                      
                    self.rect.bottom = p.rect.top 
                    self.onGround = True          
                    self.yvel = 0                 
                if yvel < 0:                      
                    self.rect.top = p.rect.bottom 
                    self.yvel = 0
                 
    def wound(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.kill()
                    
class Snowball(pygame.sprite.Sprite):
    def __init__(self, start_pos, napr, pl):
        if pl == 1:
            super().__init__(snowballs1)
        else:
            super().__init__(snowballs2)
        self.init_image()
        self.init_info(start_pos, napr)
    
    def init_image(self):
        self.image = load_image('snowball.png')
        self.rect = pygame.Rect(0, 0, 12, 12)

    def init_info(self, start_pos, napr):
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.start_speed_x = 30 * napr
        self.start_speed_y = 0
        self.start_angle = 3.14/20
        self.time = 0.0
    
    def update(self, platforms):
        time = self.time + 0.01
        vx = self.start_speed_x
        vy = self.start_speed_y
        angle = self.start_angle
        self.rect.x += vx * GRAVITY * 0.2 
        self.rect.y -= vy * time * math.sin(angle) - (9.8 * GRAVITY * time ** 2)/2
        
        if pygame.sprite.spritecollideany(self, platforms):
            self.kill()
    
    def hurt(self, players):
        if len(pygame.sprite.spritecollide(self, players, False)) > 0:
            for pl in pygame.sprite.spritecollide(self, players, False):
                self.kill()
                pl.wound()
        
players = pygame.sprite.Group()
snowballs1 = pygame.sprite.Group()
snowballs2 = pygame.sprite.Group()
