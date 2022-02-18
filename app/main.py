import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
)

from app.da_bomb import Bomb
from app.wall import Wall

pygame.init()
clock = pygame.time.Clock()


SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650
DEFAULT_OBJECT_SIZE = 50

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/player_right.png")
        self.rect = self.surf.get_rect()
        self.on_da_bomb = False
        self.da_bomb_countdown = 60

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.da_bomb_countdown -= 1
        if not pygame.sprite.spritecollideany(self, bombs):
            self.on_da_bomb = False
        if pressed_keys[K_UP]:
            self.surf = pygame.image.load("images/player_back.png")
            self.rect.move_ip(0, -5)
            self.collision_checker(0, 5)
        if pressed_keys[K_DOWN]:
            self.surf = pygame.image.load("images/player_front.png")
            self.rect.move_ip(0, 5)
            self.collision_checker(0, -5)
        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load("images/player_left.png")
            self.rect.move_ip(-5, 0)
            self.collision_checker(5, 0)
        if pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load("images/player_right.png")
            self.rect.move_ip(5, 0)
            self.collision_checker(-5, 0)
        if pressed_keys[K_SPACE]:
            self.the_bomb_has_been_planted()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def collision_checker(self, x_speed: int, y_speed: int):
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.move_ip(x_speed, y_speed)
        if pygame.sprite.spritecollideany(self, bombs)\
                and self.on_da_bomb is False:
            self.rect.move_ip(x_speed, y_speed)

    def the_bomb_has_been_planted(self):
        if self.da_bomb_countdown <= 0:
            x = (self.rect.centerx // DEFAULT_OBJECT_SIZE
                 * DEFAULT_OBJECT_SIZE) + DEFAULT_OBJECT_SIZE // 2
            y = (self.rect.centery // DEFAULT_OBJECT_SIZE
                 * DEFAULT_OBJECT_SIZE) + DEFAULT_OBJECT_SIZE // 2
            self.bomb = Bomb((x, y))
            bombs.add(self.bomb)
            all_sprites.add(self.bomb)
            self.on_da_bomb = True
            self.da_bomb_countdown = 60


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
