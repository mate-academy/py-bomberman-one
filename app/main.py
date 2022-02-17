import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

pygame.init()
clock = pygame.time.Clock()


SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650
DEFAULT_OBJECT_SIZE = 50

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.get_driver()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/player_front.png").convert()
        self.rect = self.surf.get_rect()
        self.counter = 0

    def update(self):
        self.counter += 1
        key_press = pygame.key.get_pressed()
        if key_press[K_LEFT]:
            self.surf = pygame.image.load("images/player_left.png").convert()
            self.rect.move_ip(-2, 0)
            if pygame.sprite.spritecollideany(self, group=walls):
                self.rect.move_ip(2, 0)
        elif key_press[K_RIGHT]:
            self.surf = \
                pygame.image.load("images/player_right.png").convert()
            self.rect.move_ip(2, 0)
            if pygame.sprite.spritecollideany(self, group=walls):
                self.rect.move_ip(-2, 0)
        elif key_press[K_UP]:
            self.surf = \
                pygame.image.load("images/player_back.png").convert()
            self.rect.move_ip(0, -2)
            if pygame.sprite.spritecollideany(self, group=walls):
                self.rect.move_ip(0, 2)
        elif key_press[K_DOWN]:
            self.surf = \
                pygame.image.load("images/player_front.png").convert()
            self.rect.move_ip(0, 2)
            if pygame.sprite.spritecollideany(self, group=walls):
                self.rect.move_ip(0, -2)
        elif key_press[K_SPACE]:
            if self.counter >= 60:
                bomb = Bomb((self.rect.x, self.rect.y))
                all_sprites.add(bomb)
                bombs.add(bomb)
                self.counter = 0

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Bomb(pygame.sprite.Sprite):
    def __init__(self, center: tuple):
        super().__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.image.load("images/bomb.png").convert_alpha()
        self.rect = self.surf.get_rect(center=self.get_centr(center))

    def get_centr(self, center):
        wight = (center[0] - center[0] % DEFAULT_OBJECT_SIZE
                 + self.surf.get_width() // 2)
        height = (center[1] - center[1] % DEFAULT_OBJECT_SIZE
                  + self.surf.get_height() // 2)
        return wight, height


class Wall(pygame.sprite.Sprite):
    def __init__(self, center_pos: tuple):
        super().__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.image.load("images/wall.png").convert()
        self.rect = self.surf.get_rect(center=center_pos)

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


player = Player()

bombs = pygame.sprite.Group()
walls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

for wall_center in Wall.create_centers_of_walls(
    (SCREEN_WIDTH, SCREEN_HEIGHT), (DEFAULT_OBJECT_SIZE, DEFAULT_OBJECT_SIZE)
):
    wall = Wall(wall_center)
    walls.add(wall)
    all_sprites.add(wall)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    player.update()

    walls.update()

    screen.fill((0, 0, 0))

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
