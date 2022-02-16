import os

import pygame
from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

from app.bomb import Bomb
from app.wall import Wall


pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650
DEFAULT_OBJECT_SIZE = 50

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf = pygame.image.load(
            os.path.join("images", "player_right.png")).convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.bomb_delay = 1000
        self.last_bomb = pygame.time.get_ticks()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.surf = pygame.image.load(
                os.path.join("images", "player_back.png")).convert_alpha()
            self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, 5)
        if pressed_keys[K_DOWN]:
            self.surf = pygame.image.load(
                os.path.join("images", "player_front.png")).convert_alpha()
            self.rect.move_ip(0, 5)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, -5)
        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load(
                os.path.join("images", "player_left.png")).convert_alpha()
            self.rect.move_ip(-5, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(5, 0)
        if pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load(
                os.path.join("images", "player_right.png")).convert_alpha()
            self.rect.move_ip(5, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(-5, 0)
        if pressed_keys[K_SPACE]:
            self.plant_bomb()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def plant_bomb(self):
        now = pygame.time.get_ticks()
        if now - self.last_bomb > self.bomb_delay:
            self.last_bomb = now
            x = self.rect.centerx // 50 * 50 + 25
            y = self.rect.centery // 50 * 50 + 25
            bomb = Bomb((x, y))
            all_sprites.add(bomb)
            bombs.add(bomb)


player = Player()

walls = pygame.sprite.Group()
bombs = pygame.sprite.Group()
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

    player.update(pygame.key.get_pressed())

    walls.update()

    screen.fill((0, 0, 0))

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
