import time

import pygame
from bomb import Bomb
from wall import Wall


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
clock = pygame.time.Clock()


SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650
DEFAULT_OBJECT_SIZE = 50

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("./images/player_front.png").convert()
        self.rect = self.surf.get_rect()
        self.counter = 0

    def update(self):
        self.counter += 1
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load("./images/player_left.png").convert()
            self.rect.move_ip(-2, 0)
            if pygame.sprite.spritecollideany(self, group=walls) \
                    or pygame.sprite.spritecollideany(self, group=bombs):
                self.rect.move_ip(2, 0)
        elif pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load("./images/player_right.png").convert()
            self.rect.move_ip(2, 0)
            if pygame.sprite.spritecollideany(self, group=walls) \
                    or pygame.sprite.spritecollideany(self, group=bombs):
                self.rect.move_ip(-2, 0)
        elif pressed_keys[K_UP]:
            self.surf = pygame.image.load("./images/player_back.png").convert()
            self.rect.move_ip(0, -2)
            if pygame.sprite.spritecollideany(self, group=walls) \
                    or pygame.sprite.spritecollideany(self, group=bombs):
                self.rect.move_ip(0, 2)
        elif pressed_keys[K_DOWN]:
            self.surf = pygame.image.load("./images/player_front.png").convert()
            self.rect.move_ip(0, 2)
            if pygame.sprite.spritecollideany(self, group=walls)\
                    or pygame.sprite.spritecollideany(self, group=bombs):
                self.rect.move_ip(0, -2)
        elif pressed_keys[K_SPACE]:
            current_position = (self.rect.x, self.rect.y)
            if self.counter >= 60:
                bomb = Bomb((self.rect.x, self.rect.y))
                all_sprites.add(bomb)
                bombs.add(bomb)
                self.counter = 0
                self.rect.x += 25
                self.rect.y += 25

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


player = Player()


bombs = pygame.sprite.Group()
walls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


for wall_center in Wall.create_centers_of_walls(
    (SCREEN_WIDTH, SCREEN_HEIGHT), (DEFAULT_OBJECT_SIZE, DEFAULT_OBJECT_SIZE)
):
    wall = Wall(wall_center)
    walls.add(wall)
    all_sprites.add(wall)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    player.update()

    walls.update()

    screen.fill((0, 0, 0))

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
