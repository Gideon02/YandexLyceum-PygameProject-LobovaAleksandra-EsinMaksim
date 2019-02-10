import os
import pygame
import math

from textures import load_map, load_level, textures_spr, blocks, stairs, coins, COUNT_COIN, greys, End
from activities import Player, Snowball, players, snowballs1, snowballs2, moobs, Moob

pygame.init()

size = width, height = 1300, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('SnowGame')

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

sn1 = Moob((2496, 1962), -1, 'snowman1_pic.png')
sn1.add(team_2)

sn2 = Moob((2088, 1892), -1, 'snowman2_pic.png')
sn2.add(team_2)

sc1 = Moob((2640, 1438), -1, 'scare_1_pic.png')
sc1.add(team_2)

sc2 = Moob((1320, 2928), -1, 'scare_2_pic.png')
sc2.add(team_2)

sc3 = Moob((2928, 2426), -1, 'scare_3_pic.png')
sc3.add(team_2)

sc4 = Moob((192, 2594), 1, 'scare_4_pic.png')
sc4.add(team_2)

running_screen = True
left1 = False
right1 = False
up1 = False

left2 = False
right2 = False
up2 = False

all_sprites = [textures_spr, blocks, stairs, players, snowballs1, snowballs2, moobs]

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
        self.dx = -(target.rect.x + target.rect.w // 2 - 1200 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 760 // 2)


camera = Camera((0, 0))
pygame.time.set_timer(pygame.USEREVENT, 80)
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
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface1 = myfont.render('SnowGame', False, (0, 0, 0))
    textsurface2 = myfont.render('PRESS F TO START', False, (0, 0, 0))
    screen.blit(textsurface1,(525, 300))
    screen.blit(textsurface2, (450, 350))    
    pygame.display.flip()
    clock.tick(60)    

running_screen = True

count = 0

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
            if count == 15:
                for moob in team_2:
                    moob.update()
                    count = 0
            else:
                count += 1
            for grey in greys:
                grey.update()
            for coin in coins:
                coin.update()
            for snowball in snowballs1:
                snowball.hurt(team_2)
                snowball.update(blocks)
                
            for snowball in snowballs2:
                snowball.hurt(team_1)
                snowball.update(blocks)


    screen.fill((0, 0, 0))
    
    if len(coins) == 0:
        f = True
        while f:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_screen = False
                    f = False
                    
            g = pygame.sprite.Group()
            end_game = End((0, 0))
            end_game.add(g)
            g.draw(screen)
            
            pygame.display.flip()
            clock.tick(60)  
            
    if PAUSE:
        screen.fill((255, 255, 0))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface1 = myfont.render('PAUSE', False, (0, 0, 0))
        textsurface2 = myfont.render('PRESS P TO CONTINUE', False, (0, 0, 0))
        screen.blit(textsurface1,(525, 300))
        screen.blit(textsurface2, (450, 350))
        
    else:
        camera.update(player1)
        player1.update(left1, right1, up1, blocks, stairs)
        
        player1.count += len(pygame.sprite.spritecollide(player1, coins, True))
        
        
            
        for group in all_sprites:
            for sprite in group:
                camera.apply(sprite)
                
        textures_spr.draw(screen)
        blocks.draw(screen)
        stairs.draw(screen)
        players.draw(screen)
        greys.draw(screen)
        snowballs1.draw(screen)
        snowballs2.draw(screen)
        moobs.draw(screen)
        coins.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
