from pygame import sprite, Surface


class Bomb(sprite.Sprite):
    def __init__(self):
        super(Bomb, self).__init__()
        self.surf = Surface((10, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()

    def _move_bomb(self, position):
        self.rect.move_ip(position[0], position[1])

    @classmethod
    def create_bomb(cls, player_borders):
        new_bomb = Bomb()
        new_bomb._move_bomb((player_borders.left, player_borders.top))
        return new_bomb
