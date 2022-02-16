import pygame


class Bomb(pygame.sprite.Sprite):

    def __init__(self, position: tuple):
        super(Bomb, self).__init__()
        self.surf = pygame.image.load("images/bomb.png").convert_alpha()
        self.rect = self.surf.get_rect(center=position)
