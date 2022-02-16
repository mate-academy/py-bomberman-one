import pygame

from app.settings import DEFAULT_OBJECT_SIZE


class Bomb(pygame.sprite.Sprite):
    def __init__(self, center_pos: tuple):
        super().__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.Surface((self.width, self.height))
        self.surf = pygame.image.load("images/bomb.png").convert_alpha()
        self.rect = self.surf.get_rect(center=center_pos)

    @staticmethod
    def create_centers_of_bombs(player_pos: tuple):
        center_width = player_pos[0]
        center_height = player_pos[1]

        center_pos = (center_width, center_height)

        return center_pos
