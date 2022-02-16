import pygame
from constants import BOMB


class Bomb(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.surf = pygame.image.load(BOMB)
        self.player = player
        self.rect = player.rect.center
