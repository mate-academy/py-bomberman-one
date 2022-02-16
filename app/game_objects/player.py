from pygame import sprite, Surface
from collections import namedtuple

Border = namedtuple(
    'Border',
    'left right top bottom',
)

class Player(sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = Surface((20, 40))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect()

    def move(self, direction_vector):

        self.rect.move_ip(direction_vector[0], direction_vector[1])

    @property
    def borders(self) -> namedtuple:
        return Border(
            self.rect.midleft[0],
            self.rect.right,
            self.rect.top,
            self.rect.bottom,
        )
