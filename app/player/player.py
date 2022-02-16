import pygame
from app.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPEED
)
from app.bomb.bomb import Bomb
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("./images/player_front.png")
        self.rect = self.surf.get_rect()
        self.bomb_reload = 30

    def update(self, walls, bombs, all_sprites):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP]:
            self.surf = pygame.image.load("./images/player_back.png")
            self.rect.move_ip(0, -SPEED)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, SPEED)
        elif pressed_keys[K_DOWN]:
            self.surf = pygame.image.load("./images/player_front.png")
            self.rect.move_ip(0, SPEED)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, -SPEED)

        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load("./images/player_left.png")
            self.rect.move_ip(-SPEED, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(SPEED, 0)
        elif pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load("./images/player_right.png")
            self.rect.move_ip(SPEED, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(-SPEED, 0)

        if pressed_keys[K_SPACE] and self.bomb_reload > 30:
            self.bomb_reload = 0
            bomb = Bomb((self.rect.center[0], self.rect.center[1]))
            all_sprites.add(bomb)
            bombs.add(bomb)
        self.bomb_reload += 1

        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, SCREEN_HEIGHT)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)
