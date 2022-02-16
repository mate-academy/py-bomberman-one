from app.settings import *


class Bomb(pygame.sprite.Sprite):
    def __init__(self, coordinates):
        super(Bomb, self).__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.image.load(".\\images\\bomb.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(0, 0))
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
