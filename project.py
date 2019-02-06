import os
import pygame
import math

from textures import load_map, load_level, textures_spr, blocks, stairs, coins, COUNT_COIN, greys
from activities import Player, Snowball, players, snowballs1, snowballs2

pygame.init()

size = width, height = 1000, 600
screen = pygame.display.set_mode(size)

JUMP_POWER = 50
MOVE_SPEED = 50
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
            
load_map()
textures_spr.draw(screen)
clock = pygame.time.Clock()

team_1, team_2 = pygame.sprite.Group(), pygame.sprite.Group()
player1 = Player((31*24, 62*24))
player1.add(team_1)

running_screen = True
left1 = False
right1 = False
up1 = False

left2 = False
right2 = False
up2 = False

all_sprites = [textures_spr, blocks, stairs, players]

running_screen = True

class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 1000 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 600 // 2)


camera = Camera((0, 0))
pygame.time.set_timer(pygame.USEREVENT, 150)
PAUSE = False
pygame.mouse.set_visible( False )

while running_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                running_screen = False
    screen.fill((0, 0, 150))
    pygame.display.flip()
    clock.tick(30)    

running_screen = True

while running_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_screen = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                up2 = True

            if event.key == pygame.K_LEFT:
                left2 = True

            if event.key == pygame.K_RIGHT:
                right2 = True

            if event.key == pygame.K_w:
                up1 = True

            if event.key == pygame.K_a:
                left1 = True

            if event.key == pygame.K_d:
                right1 = True                
            
            if event.key == pygame.K_p:
                if PAUSE:
                    PAUSE = False
                else:
                    PAUSE = True
                
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:
                up2 = False

            if event.key == pygame.K_LEFT:
                left2 = False

            if event.key == pygame.K_RIGHT:
                right2 = False

            if event.key == pygame.K_w:
                up1 = False

            if event.key == pygame.K_a:
                left1 = False

            if event.key == pygame.K_d:
                right1 = False
                
            if event.key == pygame.K_e:
                Snowball((player1.rect.x, player1.rect.y), 1, 1)
            
            if event.key == pygame.K_q:
                Snowball((player1.rect.x, player1.rect.y), -1, 1) 
                
        if event.type == pygame.USEREVENT:            
            for grey in greys:
                grey.update()
            for coin in coins:
                coin.update()


    screen.fill((0, 0, 0))
    if PAUSE:
        screen.fill((255, 255, 0))
    else:
        camera.update(player1)
        player1.update(left1, right1, up1, blocks, stairs)
        
        player1.count += len(pygame.sprite.spritecollide(player1, coins, True))
        
        for snowball in snowballs1:
            snowball.hurt(team_2)
            snowball.update(blocks)    
            
        for group in all_sprites:
            for sprite in group:
                camera.apply(sprite)
                
        textures_spr.draw(screen)
        blocks.draw(screen)
        stairs.draw(screen)
        players.draw(screen)
        greys.draw(screen)
        snowballs1.draw(screen)
        coins.draw(screen)
    
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
