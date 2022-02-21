import pygame
import time
from groups import walls, bombs, all_sprites
from bomb import Bomb

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, \
    PLAYER_FRONT, PLAYER_BACK, PLAYER_LEFT, PLAYER_RIGHT

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)


class Player(pygame.sprite.Sprite):
    timeout = 0

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(PLAYER_FRONT)
        self.rect = self.surf.get_rect()
        self.speed = 5
        self.is_on_bomb = False

    def update(self, pressed_keys):
        if time.time() - Player.timeout >= 1 and pressed_keys[K_SPACE]:
            self.plant_bomb()

        if not pygame.sprite.spritecollideany(
                player, bombs
        ):
            self.is_on_bomb = False

        if pressed_keys[K_UP]:
            self.surf = pygame.image.load(PLAYER_BACK)
            self.rect.move_ip(0, -self.speed)
            self.move_collision_out(0, -self.speed)

        if pressed_keys[K_DOWN]:
            self.surf = pygame.image.load(PLAYER_FRONT)
            self.rect.move_ip(0, self.speed)
            self.move_collision_out(0, self.speed)

        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load(PLAYER_LEFT)
            self.rect.move_ip(-self.speed, 0)
            self.move_collision_out(-self.speed, 0)

        if pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load(PLAYER_RIGHT)
            self.rect.move_ip(self.speed, 0)
            self.move_collision_out(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def plant_bomb(self):
        bomb = Bomb(self.rect.center)
        bombs.add(bomb)
        all_sprites.add(bomb)
        self.is_on_bomb = True
        Player.timeout = time.time()

    def move_collision_out(self, x, y):
        if pygame.sprite.spritecollideany(self, walls)\
                or pygame.sprite.spritecollideany(self, bombs):
            if not self.is_on_bomb:
                player.rect.move_ip(-x, -y)


player = Player()
