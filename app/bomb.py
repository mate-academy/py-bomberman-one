import pygame


DEFAULT_OBJECT_SIZE = 50


class Bomb(pygame.sprite.Sprite):
    def __init__(self, center_pos: tuple):
        super().__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.image.load("./images/bomb.png").convert_alpha()
        self.rect = self.surf.get_rect(center=center_pos)
