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
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.surf = pygame.Surface((20, 40))
        self.image_front = pygame.image.load(
            "images/player_front.png"
        ).convert_alpha()
        self.image_back = pygame.image.load(
            "images/player_back.png"
        ).convert_alpha()
        self.image_left = pygame.image.load(
            "images/player_left.png"
        ).convert_alpha()
        self.image_right = pygame.image.load(
            "images/player_right.png"
        ).convert_alpha()
        self.surf = self.image_front
        self.rect = self.surf.get_rect()
        self.placed_bomb_clock = 0
        self.is_on_bomb = False
        self.speed = 5

    def plant_bomb(self):
        if not self.placed_bomb_clock:
            bombs.add(Bomb(self.rect.center))
            all_sprites.add(bombs)
            self.is_on_bomb = True
            self.placed_bomb_clock = 60

    def update(self):
        if self.placed_bomb_clock:
            self.placed_bomb_clock -= 1

        if not pygame.sprite.spritecollideany(
                self, bombs
        ):
            self.is_on_bomb = False

        if pressed_keys[K_UP] and self.rect.top > self.screen_rect.top:
            self.rect.move_ip(0, -self.speed)
            self.move_collision_out(0, -self.speed)
            self.surf = self.image_back

        if pressed_keys[K_DOWN] and self.rect.bottom < self.screen_rect.bottom:
            self.rect.move_ip(0, self.speed)
            self.move_collision_out(0, self.speed)
            self.surf = self.image_front

        if pressed_keys[K_LEFT] and self.rect.left > self.screen_rect.left:
            self.rect.move_ip(-self.speed, 0)
            self.move_collision_out(-self.speed, 0)
            self.surf = self.image_left

        if pressed_keys[K_RIGHT] and self.rect.right < self.screen_rect.right:
            self.rect.move_ip(self.speed, 0)
            self.move_collision_out(self.speed, 0)
            self.surf = self.image_right

        if pressed_keys[K_SPACE]:
            self.plant_bomb()

    def move_collision_out(self, x_speed: int, y_speed: int):
        if (pygame.sprite.spritecollideany(
                self, walls
        ) or pygame.sprite.spritecollideany(
            self, bombs
        ) and not self.is_on_bomb):
            self.rect.move_ip(-x_speed, -y_speed)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, owner_center):
        super(Bomb, self).__init__()
        self.surf = pygame.image.load("images/bomb.png").convert_alpha()
        self.rect = self.surf.get_rect(center=owner_center)
        self.rect.center = self.get_self_center()

    def get_self_center(self):
        lines = self.get_line_bomb_placed()
        return (
            lines[0] * DEFAULT_OBJECT_SIZE + self.rect.width // 2,
            lines[1] * DEFAULT_OBJECT_SIZE + self.rect.height // 2,
        )

    def get_line_bomb_placed(self):
        width = self.rect.centerx // DEFAULT_OBJECT_SIZE
        height = self.rect.centery // DEFAULT_OBJECT_SIZE
        return width, height


class Wall(pygame.sprite.Sprite):
    def __init__(self, center_pos: tuple):
        super().__init__()
        self.width = DEFAULT_OBJECT_SIZE
        self.height = DEFAULT_OBJECT_SIZE
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))
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
bombs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

for wall_center in Wall.create_centers_of_walls(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        (DEFAULT_OBJECT_SIZE, DEFAULT_OBJECT_SIZE)
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

    bombs.update()

    walls.update()

    screen.fill((0, 0, 0))

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
