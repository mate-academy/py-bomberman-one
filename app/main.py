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
        self.image_down = pygame.image.load(
            os.path.join("images", "player_front.png")).convert_alpha()
        self.image_back = pygame.image.load(
            os.path.join("images", "player_back.png")).convert_alpha()
        self.image_right = pygame.image.load(
            os.path.join("images", "player_right.png")).convert_alpha()
        self.image_left = pygame.image.load(
            os.path.join("images", "player_left.png")).convert_alpha()
        self.surf = self.image_right
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.bomb = []
        self.bomb_delay = 1000
        self.last_bomb = pygame.time.get_ticks()

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.surf = self.image_back
            self.rect.move_ip(0, -5)
            self.check_collision(0, 5)
        if pressed_keys[K_DOWN]:
            self.surf = self.image_down
            self.rect.move_ip(0, 5)
            self.check_collision(0, -5)
        if pressed_keys[K_LEFT]:
            self.surf = self.image_left
            self.rect.move_ip(-5, 0)
            self.check_collision(5, 0)
        if pressed_keys[K_RIGHT]:
            self.surf = self.image_right
            self.rect.move_ip(5, 0)
            self.check_collision(-5, 0)
        if pressed_keys[K_SPACE]:
            self.plant_bomb()

        if not pygame.sprite.spritecollideany(self, temp_bombs):
            bombs.add(self.bomb)

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
            x = (self.rect.centerx // DEFAULT_OBJECT_SIZE *
                 DEFAULT_OBJECT_SIZE) + DEFAULT_OBJECT_SIZE // 2
            y = (self.rect.centery // DEFAULT_OBJECT_SIZE *
                 DEFAULT_OBJECT_SIZE) + DEFAULT_OBJECT_SIZE // 2
            self.bomb = Bomb((x, y))
            all_sprites.add(self.bomb)
            temp_bombs.add(self.bomb)

    def check_collision(self, x_speed: int, y_speed: int):
        if (pygame.sprite.spritecollideany(self, walls)
                or pygame.sprite.spritecollideany(self, bombs)):
            self.rect.move_ip(x_speed, y_speed)


player = Player()

walls = pygame.sprite.Group()
bombs = pygame.sprite.Group()
temp_bombs = pygame.sprite.Group()
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
