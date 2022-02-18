import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, center_position: tuple):
        super(Wall, self).__init__()

        self.image = pygame.image.load("images/wall.png").convert_alpha()
        self.rect = self.image.get_rect(center=center_position)

    @staticmethod
    def create_centers_of_wall(field_size: tuple, wall_size: tuple):
        center_width = wall_size[0] + wall_size[0] // 2
        center_height = wall_size[1] + wall_size[1] // 2
        centers = []

        while center_height < field_size[1] - wall_size[1]:
            while center_width < field_size[0] - wall_size[0]:
                centers.append((center_width, center_height))
                center_width += wall_size[0] * 2
            center_height += wall_size[1] * 2
            center_width = wall_size[0] + wall_size[0] // 2

        return centers
