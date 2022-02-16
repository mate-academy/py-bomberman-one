import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
clock = pygame.time.Clock()


SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650
DEFAULT_OBJECT_SIZE = 50

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/player_right.png").convert()
        self.rect = self.surf.get_rect()

    def update(self, pressed_key):
        if pressed_key[K_UP]:
            self.surf = pygame.image.load("images/player_back.png").convert()
            self.rect.move_ip(0, -4)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(0, 4)
        if pressed_key[K_DOWN]:
            self.surf = pygame.image.load("images/player_front.png").convert()
            self.rect.move_ip(0, 4)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(0, -4)
        if pressed_key[K_LEFT]:
            self.surf = pygame.image.load("images/player_left.png").convert()
            self.rect.move_ip(-4, 0)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(4, 0)
        if pressed_key[K_RIGHT]:
            self.surf = pygame.image.load("images/player_right.png").convert()
            self.rect.move_ip(4, 0)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(-4, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("images/bomb.png").convert()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.rect = player.rect.copy()

    def update(self, pressed_key):
        if pressed_key[K_SPACE]:
            bombs.add(bomb)
            all_sprites.add(bomb)


class Wall(pygame.sprite.Sprite):
    def __init__(self, center_pos: tuple):
        super().__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.Surface((self.width, self.height))
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
bomb = Bomb()
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

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    bomb.update(pressed_keys)

    walls.update()

    screen.fill((0, 0, 0))

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
