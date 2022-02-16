import pygame

from app.settings import DEFAULT_OBJECT_SIZE


class Bomb(pygame.sprite.Sprite):
    def __init__(self, position: tuple):
        super().__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.image.load("images/bomb.png").convert_alpha()
        self.timer = 0
        self.rect = self.surf.get_rect(center=position)
