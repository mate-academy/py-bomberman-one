import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, bm_game):
        super(Player, self).__init__()

        self.screen = bm_game.screen
        self.screen_rect = self.screen.get_rect()

        image = "images/player_front.png"
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, pressed_keys):
        if sum(pressed_keys) == 1:
            if pressed_keys[K_UP]:
                image = "images/player_back.png"
                self.image = pygame.image.load(image).convert_alpha()
                self.rect.move_ip(0, -3)
            if pressed_keys[K_DOWN]:
                image = "images/player_front.png"
                self.image = pygame.image.load(image).convert_alpha()
                self.rect.move_ip(0, 3)
            if pressed_keys[K_LEFT]:
                image = "images/player_left.png"
                self.image = pygame.image.load(image).convert_alpha()
                self.rect.move_ip(-3, 0)
            if pressed_keys[K_RIGHT]:
                image = "images/player_right.png"
                self.image = pygame.image.load(image).convert_alpha()
                self.rect.move_ip(3, 0)

        self._check_edges()

    def _check_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_rect.right:
            self.rect.right = self.screen_rect.right
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_rect.bottom:
            self.rect.bottom = self.screen_rect.bottom
