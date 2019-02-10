import os
import pygame
import math
from PIL import Image

size = width, height = 1000, 600

COUNT_COIN = 8

pygame.init()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

class Texture_Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(blocks)
        self.image = load_image("block_pic.png")
        self.image.convert_alpha()
        self.rect = pygame.Rect(pos[0], pos[1], 24, 24)
        
class Texture_Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(coins, textures_spr)
        self.q = 1
        self.image = load_image('coin1_pic.png')
        self.rect = pygame.Rect(pos[0], pos[1], 24, 24)
    
    def update(self):
        self.q %= 5
        self.q += 1
        self.image = load_image('coin'+str(self.q)+'_pic.png')
        
class Texture_Left_Stair(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(stairs)
        self.image = load_image('left_stair_pic.png')
        self.image.convert_alpha()
        self.rect = pygame.Rect(pos[0], pos[1], 6, 24)
        
class Texture_Right_Stair(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(stairs)
        self.image = load_image('right_stair_pic.png')
        self.image.convert_alpha()
        self.rect = pygame.Rect(pos[0] + 18, pos[1], 6, 24)
        

class Texture_Map(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(textures_spr)
        self.image = load_image('smth.png')
        self.rect = pygame.Rect(pos[0], pos[1], 4800, 4800)

class End(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image('game_over.png')
        self.rect = pygame.Rect(pos[0], pos[1], 1300, 700)
        
    
class Texture_Grey(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(greys, textures_spr)
        self.image = load_image('grey_1.png')
        self.q = 1
        #self.image.convert_alpha()
        self.rect = pygame.Rect(pos[0], pos[1], 24, 24)
    
    def update(self):
        self.q %= 3
        self.q += 1
        self.image = load_image('grey_'+str(self.q)+'.png')
          
textures_spr = pygame.sprite.Group()
blocks = pygame.sprite.Group()
coins = pygame.sprite.Group()
stairs = pygame.sprite.Group()
greys = pygame.sprite.Group()

def load_level(filename):
    with open(filename + '.txt', 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map

def load_map():
    im = Image.open("data/blocks.png")
    pixels = im.load()
    x, y = im.size
    
    for i in range(x):
        for j in range(y):
            if pixels[i, j] == (0, 0, 0):
                Texture_Block((i*24, j*24))
                
    im = Image.open("data/left_stairs.png")
    pixels = im.load()
    x, y = im.size
    
    for i in range(x):
        for j in range(y):
            if pixels[i, j] == (255, 0, 0):
                Texture_Left_Stair((i*24, j*24))
    
    im = Image.open("data/right_stairs.png")
    pixels = im.load()
    x, y = im.size
    
    for i in range(x):
        for j in range(y):
            if pixels[i, j] == (255, 0, 0):
                Texture_Right_Stair((i*24, j*24))    
    
                
    im = Image.open("data/coins.png")
    pixels = im.load()
    x, y = im.size
    
    for i in range(x):
        for j in range(y):
            if pixels[i, j] == (255, 255, 0):
                Texture_Coin((i*24, j*24))
            
    im = Image.open("data/greys.png")
    pixels = im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            if pixels[i, j] == (0, 0, 128):
                Texture_Grey((i*24, j*24))
                
                
    texture_map = Texture_Map((-864, -864))
