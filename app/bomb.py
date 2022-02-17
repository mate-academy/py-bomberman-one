import pygame
from constants import BOMB, DEFAULT_OBJECT_SIZE


class Bomb(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.surf = pygame.image.load(BOMB)
        self.player = player
        self.rect = self.surf.get_rect(center=player)
        self.rect.center = self.get_self_center()

    def get_lines(self):
        width = self.rect.centerx // DEFAULT_OBJECT_SIZE
        height = self.rect.centery // DEFAULT_OBJECT_SIZE
        return width, height

    def get_self_center(self):
        lines = self.get_lines()
        return (
            lines[0] * DEFAULT_OBJECT_SIZE + self.rect.width // 2,
            lines[1] * DEFAULT_OBJECT_SIZE + self.rect.height // 2,
        )

