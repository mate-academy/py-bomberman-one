import pygame


from app.bomb import Bomb
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)

from app.settings import SCREEN_WIDTH, \
    SCREEN_HEIGHT, DEFAULT_OBJECT_SIZE, DEFAULT_SPEED


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 40))
        self.surf = pygame.image.load("images/player_front.png").\
            convert_alpha()
        self.rect = self.surf.get_rect()
        self.timer = 60

    def update(self, pressed_keys, walls, bombs_group, all_sprites_group):

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -DEFAULT_SPEED)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, DEFAULT_SPEED)
            self.surf = pygame.image.load("images/player_back.png").\
                convert_alpha()

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, DEFAULT_SPEED)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, -DEFAULT_SPEED)
            self.surf = pygame.image.load("images/player_front.png").\
                convert_alpha()

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-DEFAULT_SPEED, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(DEFAULT_SPEED, 0)
            self.surf = pygame.image.load("images/player_left.png").\
                convert_alpha()

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(DEFAULT_SPEED, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(-DEFAULT_SPEED, 0)
            self.surf = pygame.image.load("images/player_right.png").\
                convert_alpha()

        if pressed_keys[K_SPACE]:
            self.plant_bomb(bombs_group, all_sprites_group)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        self.timer -= 1

        if self.timer < 0:
            self.timer = 0

    def plant_bomb(self, bombs_group, all_sprites_group):
        if self.timer == 0:
            bomb = Bomb((self.rect.x + DEFAULT_OBJECT_SIZE // 4,
                         self.rect.y + DEFAULT_OBJECT_SIZE // 4))
            bombs_group.add(bomb)
            all_sprites_group.add(bomb)
            self.timer = 60
