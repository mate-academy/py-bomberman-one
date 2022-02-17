import pygame


class Bomb(pygame.sprite.Sprite):

    def __init__(self, position: tuple, default_obj_size: int):
        super(Bomb, self).__init__()
        self.surf = pygame.image.load("images/bomb.png").convert_alpha()
        self.rect = self.surf.get_rect(center=position)
        self.default_obj_size = default_obj_size
        self.rect.center = self.get_self_center()

    def get_self_center(self):
        return (
            (self.rect.centerx // self.default_obj_size) * self.default_obj_size + self.rect.width // 2,
            (self.rect.centery // self.default_obj_size) * self.default_obj_size + self.rect.height // 2,
        )
