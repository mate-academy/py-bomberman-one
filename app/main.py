from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_OBJECT_SIZE
from groups import walls, all_sprites
import pygame
from app.player import player
from app.walls import Wall
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


def game():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
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
        player.update(pressed_keys)
        walls.update()

        screen.fill((0, 255, 0))

        for sprite in all_sprites:
            screen.blit(sprite.surf, sprite.rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game()
