import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE
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
        self.surf = pygame.image.load("images/player_front.png").convert()
        self.rect = self.surf.get_rect()
        self.plant_bomb_cooldown = 0
        self.is_on_bomb = False

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.plant_bomb_cooldown != 0:
            self.plant_bomb_cooldown -= 1

        if pressed_keys[K_SPACE]:
            if self.plant_bomb_cooldown == 0:
                self.plant_bomb()

        if not pygame.sprite.spritecollideany(self, bombs):
            self.is_on_bomb = False

        if pressed_keys[K_UP]:
            self.surf = pygame.image.load("images/player_back.png").convert()
            self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, 5)
            if pygame.sprite.spritecollideany(self, bombs) \
                    and not self.is_on_bomb:
                self.rect.move_ip(0, 5)
        if pressed_keys[K_DOWN]:
            self.surf = pygame.image.load("images/player_front.png").convert()
            self.rect.move_ip(0, 5)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(self, bombs) \
                    and not self.is_on_bomb:
                self.rect.move_ip(0, -5)
        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load("images/player_left.png").convert()
            self.rect.move_ip(-5, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(5, 0)
            if pygame.sprite.spritecollideany(self, bombs) \
                    and not self.is_on_bomb:
                self.rect.move_ip(5, 0)
        if pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load("images/player_right.png").convert()
            self.rect.move_ip(5, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(-5, 0)
            if pygame.sprite.spritecollideany(self, bombs) \
                    and not self.is_on_bomb:
                self.rect.move_ip(-5, 0)

            self.clash_wall()

    def clash_wall(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def plant_bomb(self):
        Bomb(self.rect.center)
        self.is_on_bomb = True
        self.plant_bomb_cooldown = 60


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


class Bomb(pygame.sprite.Sprite):
    def __init__(self, owner_center):
        super(Bomb, self).__init__()
        self.surf = pygame.image.load("images/bomb.png").convert()
        self.rect = self.surf.get_rect(center=self.get_lines(owner_center))
        bombs.add(self)
        all_sprites.add(self)

    def get_lines(self, owner_center):
        width = owner_center[0] - owner_center[0] % DEFAULT_OBJECT_SIZE + \
            self.surf.get_width() // 2
        height = owner_center[1] - owner_center[1] % DEFAULT_OBJECT_SIZE + \
            self.surf.get_height() // 2
        return width, height


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

    pressed_keys = pygame.key.get_pressed()

    player.update()

    walls.update()

    screen.fill((0, 0, 0))

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
