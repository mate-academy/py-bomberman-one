import pygame

from pygame.locals import (
    RLEACCEL,
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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("./images/player_front.png").convert()
        self.surf.set_colorkey((0, 255, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.timer = 0

    def update(self, stepback=0):
        self.timer += 1
        if stepback != 0:
            self.rect.move_ip(-stepback, 0)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(stepback, 0)
                self.rect.move_ip(0, stepback)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -3)
            self.surf = pygame.image.load("./images/player_back.png").convert()
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(0, 3)
            # if pygame.sprite.spritecollideany(player, bombs):
            #     self.rect.move_ip(0, 2)

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 3)
            self.surf = pygame.image.load("./images/player_front.png").convert()
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(0, -3)
            # if pygame.sprite.spritecollideany(player, bombs):
            #     self.rect.move_ip(0, -3)

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-3, 0)
            self.surf = pygame.image.load("./images/player_left.png").convert()
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(3, 0)
            # if pygame.sprite.spritecollideany(player, bombs):
            #     self.rect.move_ip(2, 0)

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(3, 0)
            self.surf = pygame.image.load("./images/player_right.png").convert()
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(-3, 0)
            # if pygame.sprite.spritecollideany(player, bombs):
            #     self.rect.move_ip(-2, 0)

        if pressed_keys[K_SPACE]:
            if self.timer >= 60:
                bomb = Bomb((self.rect.x, self.rect.y))
                bombs.add(bomb)
                all_sprites.add(bomb)
                self.timer = 0
                self.update(3)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


bombs = pygame.sprite.Group()


class Bomb(pygame.sprite.Sprite):

    def __init__(self, center_pos: tuple):
        super().__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.image.load("./images/bomb.png").convert_alpha()
        self.surf.set_colorkey((105, 105, 105), RLEACCEL)
        self.rect = self.surf.get_rect(center=center_pos)


class Wall(pygame.sprite.Sprite):
    def __init__(self, center_pos: tuple):
        super().__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.image.load("./images/wall.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
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
