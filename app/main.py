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
        self.surf = pygame.image.load("images/player_front.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.plant_bomb_waiting = 0

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, 5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, -5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(-5, 0)
        if self.plant_bomb_waiting:
            self.plant_bomb_waiting -= 1
        if pressed_keys[K_SPACE]:
            if not self.plant_bomb_waiting:
                bomb = self.put_bomb()
                bombs.add(bomb)
                all_sprites.add(bomb)
            if not pygame.sprite.spritecollideany(self, bombs):
                walls.add(bomb)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def put_bomb(self):
        bomb = Bomb(self.rect.center)
        self.plant_bomb_waiting = 60

        return bomb


class Wall(pygame.sprite.Sprite):
    def __init__(self, center_pos: tuple):
        super().__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.image.load("images/wall.png").convert_alpha()
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


class Bomb(pygame.sprite.Sprite):
    def __init__(self, player_coord):
        super(Bomb, self).__init__()
        self.surf = pygame.image.load("images/bomb.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(
                self.get_coord(player_coord)
            ))

    def get_coord(self, player_coord):
        width = player_coord[0] - player_coord[0] % DEFAULT_OBJECT_SIZE + self.surf.get_width() // 2
        height = player_coord[1] - player_coord[1] % DEFAULT_OBJECT_SIZE + self.surf.get_height() // 2

        return width, height


player = Player()

walls = pygame.sprite.Group()
bombs = pygame.sprite.Group()
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

    pressed_keys_list = pygame.key.get_pressed()

    player.update(pressed_keys_list)
    walls.update()
    bombs.update()

    screen.fill((0, 0, 0))

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
