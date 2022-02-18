import pygame


class Bomb(pygame.sprite.Sprite):
    def __init__(self, center_position: tuple):
        super(Bomb, self).__init__()

        self.image = pygame.image.load("images/bomb.png").convert_alpha()
        self.rect = self.image.get_rect(center=center_position)