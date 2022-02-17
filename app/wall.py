import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, center_pos: tuple):
        super(Wall, self).__init__()

        # self.DEFAULT_OBJECT_SIZE = 50
        # self.width = self.DEFAULT_OBJECT_SIZE
        # self.height = self.DEFAULT_OBJECT_SIZE
        self.image = pygame.image.load("images/wall.png").convert_alpha()
        # self.surf.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=center_pos)

    @staticmethod
    def create_centers_of_walls(field_size: tuple, wall_size: tuple):
        center_width = wall_size[0] + wall_size[0] // 2
        center_height = wall_size[1] + wall_size[1] // 2
        centers = []

        while center_height < field_size[1] - wall_size[1]:
            while center_width < field_size[0] - wall_size[0]:
                centers.append((center_width, center_height))
                center_width += 2 * wall_size[0]
            center_height += 2 * wall_size[1]
            center_width = wall_size[0] + wall_size[0] // 2

        return centers
