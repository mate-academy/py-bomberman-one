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
    def create_centers_of_bombs(field_size: tuple, wall_size: tuple):
        center_width = wall_size[0] // 2  # 75
        center_height = wall_size[1] // 2  # 75
        centers = []

        while center_height < field_size[1]:
            while center_width < field_size[0]:
                centers.append((center_width, center_height))
                center_width += 2 * wall_size[0] // 2
            center_height += 2 * wall_size[1] // 2
            center_width = wall_size[0] // 2
        return centers
