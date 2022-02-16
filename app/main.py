import pygame
from config import (
    BACKGROUND_COLOR,
    DEFAULT_OBJECT_SIZE,
    FPS,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from player.player import Player
from wall.wall import Wall

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
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
        if (
                event.type == KEYDOWN
                and event.key == K_ESCAPE
                or event.type != KEYDOWN
                and event.type == QUIT
        ):
            running = False

    player.update(walls, bombs, all_sprites)

    walls.update()

    screen.fill(BACKGROUND_COLOR)
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
