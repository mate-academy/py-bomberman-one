import pygame


class Bomb(pygame.sprite.Sprite):
    def __init__(self, center_pos: tuple):
        super().__init__()
        self.surf = pygame.image.load("./images/bomb.png")
        self.rect = self.surf.get_rect(center=center_pos)
