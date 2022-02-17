import os

import pygame
from pygame.locals import RLEACCEL


DEFAULT_OBJECT_SIZE = 50


class Bomb(pygame.sprite.Sprite):
    def __init__(self, center_pos: tuple):
        super().__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.Surface((self.width, self.height))
        self.surf = pygame.image.load(
            os.path.join("images", "bomb.png")).convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=center_pos)
