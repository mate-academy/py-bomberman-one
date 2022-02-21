"""
Issues:
- walls do not stop fire
- route of spiders is weird
- score indicator
"""


import random
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
        self.dropped_bombs = []
        self.health = 100000

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.surf = pygame.image.load("images/player_back.png").convert_alpha()
            self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs):
                self.rect.move_ip(0, 5)
        if pressed_keys[K_DOWN]:
            self.surf = pygame.image.load("images/player_front.png").convert_alpha()
            self.rect.move_ip(0, 5)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs):
                self.rect.move_ip(0, -5)
        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load("images/player_left.png").convert_alpha()
            self.rect.move_ip(-5, 0)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs):
                self.rect.move_ip(5, 0)
        if pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load("images/player_right.png").convert_alpha()
            self.rect.move_ip(5, 0)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs):
                self.rect.move_ip(-5, 0)
        if self.plant_bomb_waiting:
            self.plant_bomb_waiting -= 1
        if pressed_keys[K_SPACE]:
            if not self.plant_bomb_waiting:
                bomb = self.put_bomb()
                self.dropped_bombs.append(bomb)
                all_sprites.add(bomb)
        if self.dropped_bombs:
            if not pygame.sprite.collide_rect(self, self.dropped_bombs[-1]):
                bombs.add(self.dropped_bombs[-1])
                del self.dropped_bombs[-1]

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if self.health <= 0:
            self.kill()

    def put_bomb(self):
        self.plant_bomb_waiting = 60
        return Bomb(self.rect.center)


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
        self.time_to_blow = 180

    def get_coord(self, player_coord):
        width = player_coord[0] - player_coord[0] % DEFAULT_OBJECT_SIZE + self.surf.get_width() // 2
        height = player_coord[1] - player_coord[1] % DEFAULT_OBJECT_SIZE + self.surf.get_height() // 2

        return width, height

    def update(self):
        self.time_to_blow -= 1
        if not self.time_to_blow:
            self.kill()
            current_coord = self.rect.center
            fire_center = Fire(current_coord)
            fires.add(fire_center)
            all_sprites.add(fire_center)
            for step in range(1, 6):
                fire_top = Fire((current_coord[0], current_coord[1] + DEFAULT_OBJECT_SIZE * step))
                fires.add(fire_top)
                all_sprites.add(fire_top)
                fire_bottom = Fire((current_coord[0], current_coord[1] - DEFAULT_OBJECT_SIZE * step))
                fires.add(fire_bottom)
                all_sprites.add(fire_bottom)
                fire_left = Fire((current_coord[0] - DEFAULT_OBJECT_SIZE * step, current_coord[1]))
                fires.add(fire_left)
                all_sprites.add(fire_left)
                fire_right = Fire((current_coord[0] + DEFAULT_OBJECT_SIZE * step, current_coord[1]))
                fires.add(fire_right)
                all_sprites.add(fire_right)


class Fire(pygame.sprite.Sprite):
    def __init__(self, bomb_coord):
        super(Fire, self).__init__()
        self.surf = pygame.image.load("images/explosion_1.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=bomb_coord)
        self.time_to_blow = 30

    def update(self):
        self.time_to_blow -= 1
        if self.time_to_blow == 20:
            self.surf = pygame.image.load("images/explosion_2.png").convert_alpha()
        elif self.time_to_blow == 10:
            self.surf = pygame.image.load("images/explosion_3.png").convert_alpha()
        elif not self.time_to_blow:
            self.kill()


class Spider(pygame.sprite.Sprite):
    def __init__(self):
        super(Spider, self).__init__()
        self.surf = pygame.image.load("images/spider_front.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self):
        if self.rect.center[1] > (player.rect.center[1]):
            self.surf = pygame.image.load("images/spider_back.png").convert_alpha()
            self.rect.move_ip(0, -2)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs) or \
                    pygame.sprite.spritecollideany(self, rocks):
                self.rect.move_ip(0, 2)
        if self.rect.center[1] < (player.rect.center[1]):
            self.surf = pygame.image.load("images/spider_front.png").convert_alpha()
            self.rect.move_ip(0, 2)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs) or \
                    pygame.sprite.spritecollideany(self, rocks):
                self.rect.move_ip(0, -2)
        if self.rect.center[0] > (player.rect.center[0]):
            self.surf = pygame.image.load("images/spider_left.png").convert_alpha()
            self.rect.move_ip(-2, 0)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs) or \
                    pygame.sprite.spritecollideany(self, rocks):
                self.rect.move_ip(2, 0)
        if self.rect.center[0] < (player.rect.center[0]):
            self.surf = pygame.image.load("images/spider_right.png").convert_alpha()
            self.rect.move_ip(2, 0)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs) or \
                    pygame.sprite.spritecollideany(self, rocks):
                self.rect.move_ip(-2, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if pygame.sprite.spritecollideany(self, fires):
            self.kill()
        if pygame.sprite.collide_rect(self, player):
            player.health -= 10
            self.kill()


class Boar(pygame.sprite.Sprite):
    def __init__(self):
        super(Boar, self).__init__()
        self.surf = pygame.image.load("images/boar_front.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH, 0))
        self.dropped_rocks = []
        self.time_to_drop_rock = 300

    def update(self):
        if self.rect.center[1] > (player.rect.center[1]):
            self.surf = pygame.image.load("images/boar_back.png").convert_alpha()
            self.rect.move_ip(0, -2)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs) or \
                    pygame.sprite.spritecollideany(self, rocks):
                self.rect.move_ip(0, 2)
        if self.rect.center[1] < (player.rect.center[1]):
            self.surf = pygame.image.load("images/boar_front.png").convert_alpha()
            self.rect.move_ip(0, 2)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs) or \
                    pygame.sprite.spritecollideany(self, rocks):
                self.rect.move_ip(0, -2)
        if self.rect.center[0] > (player.rect.center[0]):
            self.surf = pygame.image.load("images/boar_left.png").convert_alpha()
            self.rect.move_ip(-2, 0)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs) or \
                    pygame.sprite.spritecollideany(self, rocks):
                self.rect.move_ip(2, 0)
        if self.rect.center[0] < (player.rect.center[0]):
            self.surf = pygame.image.load("images/boar_right.png").convert_alpha()
            self.rect.move_ip(2, 0)
            if pygame.sprite.spritecollideany(self, walls) or \
                    pygame.sprite.spritecollideany(self, bombs) or \
                    pygame.sprite.spritecollideany(self, rocks):
                self.rect.move_ip(-2, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if pygame.sprite.spritecollideany(self, fires):
            self.kill()
        if pygame.sprite.collide_rect(self, player):
            player.health -= 10
            self.kill()

        self.time_to_drop_rock -= 1
        if not self.time_to_drop_rock:
            rock = self.put_rock()
            self.dropped_rocks.append(rock)
            all_sprites.add(rock)
        if self.dropped_rocks:
            if not pygame.sprite.collide_rect(self, self.dropped_rocks[-1]):
                rocks.add(self.dropped_rocks[-1])
                del self.dropped_rocks[-1]

    def put_rock(self):
        return Rock(self.rect.center)


class Rock(pygame.sprite.Sprite):
    def __init__(self, boar_coord):
        super(Rock, self).__init__()
        self.surf = pygame.image.load("images/rock.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=boar_coord)

    def update(self):
        if pygame.sprite.spritecollideany(self, fires):
            self.kill()


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super(Bird, self).__init__()
        self.surf = pygame.image.load("images/bird_left.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.choice(
                    [(
                        random.randint(0, SCREEN_WIDTH),
                        0,
                    ),
                    (
                        0,
                        random.randint(0, SCREEN_HEIGHT),
                    )]
                )
            )
        )
        self.dropped_bombs = []
        self.plant_bomb_waiting = 240

    def update(self):
        self.plant_bomb_waiting -= 1
        self.rect.move_ip(-1, 1)
        if not pygame.sprite.spritecollideany(self, walls):
            if not self.plant_bomb_waiting:
                bomb = self.put_bomb()
                self.dropped_bombs.append(bomb)
                all_sprites.add(bomb)
        if self.dropped_bombs:
            if not pygame.sprite.collide_rect(self, self.dropped_bombs[-1]):
                bombs.add(self.dropped_bombs[-1])
                del self.dropped_bombs[-1]
        if self.rect.right < 0:
            self.kill()

    def put_bomb(self):
        self.plant_bomb_waiting = 240
        return Bomb(self.rect.center)


ADDSPIDER = pygame.USEREVENT + 1
pygame.time.set_timer(ADDSPIDER, 1000)
ADDBOAR = pygame.USEREVENT + 2
pygame.time.set_timer(ADDBOAR, 3000)
ADDBIRD = pygame.USEREVENT + 3
pygame.time.set_timer(ADDBIRD, 2000)

player = Player()

walls = pygame.sprite.Group()
bombs = pygame.sprite.Group()
fires = pygame.sprite.Group()
enemies = pygame.sprite.Group()
rocks = pygame.sprite.Group()
birds = pygame.sprite.Group()
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
        elif event.type == ADDSPIDER:
            new_spider = Spider()
            enemies.add(new_spider)
            all_sprites.add(new_spider)
        elif event.type == ADDBOAR:
            new_boar = Boar()
            enemies.add(new_boar)
            all_sprites.add(new_boar)
        elif event.type == ADDBIRD:
            new_bird = Bird()
            enemies.add(new_bird)
            all_sprites.add(new_bird)
        elif event.type == QUIT:
            running = False

    pressed_keys_list = pygame.key.get_pressed()

    player.update(pressed_keys_list)
    walls.update()
    bombs.update()
    fires.update()
    enemies.update()
    rocks.update()
    birds.update()

    screen.fill((0, 0, 0))

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    if pygame.sprite.spritecollideany(player, fires) or \
            player.health <= 0:
        player.kill()
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
