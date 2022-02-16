import pygame

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from app.const import SCREEN_WIDTH, SCREEN_HEIGHT
from app.player import Player
from app.wall import Wall

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

player = Player()

bombs = pygame.sprite.Group()
walls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

Wall.create_walls(walls=walls, all_sprites=all_sprites)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys=pressed_keys,
                  walls=walls,
                  bombs_group=bombs,
                  all_sprites_group=all_sprites)

    walls.update()

    screen.fill((0, 0, 0))

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
