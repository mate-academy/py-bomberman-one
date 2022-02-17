import sys
import pygame
from player import Player
from wall import Wall
from bomb import Bomb

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


class Bomberman:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()

        self.SCREEN_WIDTH = 650
        self.SCREEN_HEIGHT = 650
        self.DEFAULT_OBJECT_SIZE = 50

        self.screen = pygame.display.set_mode(
            [self.SCREEN_WIDTH, self.SCREEN_HEIGHT]
        )

        self.player = Player(self)
        self.walls = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.current_bombs = []

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.timer = 60

        for wall_center in Wall.create_centers_of_walls(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            (self.DEFAULT_OBJECT_SIZE, self.DEFAULT_OBJECT_SIZE)
        ):
            wall = Wall(wall_center)
            self.walls.add(wall)
            self.all_sprites.add(wall)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_SPACE] and self.timer <= 0:
                temp_x = self.player.rect.center[0] // 50
                temp_y = self.player.rect.center[1] // 50
                bomb = Bomb((temp_x * 50 + 25, temp_y * 50 + 25))
                self.current_bombs.append(bomb)
                self.all_sprites.add(bomb)
                self.timer = 60

            self.player.update(pressed_keys)
            self._check_player_collision(self.walls, pressed_keys)
            self._check_player_collision(self.bombs, pressed_keys)
            self._check_is_on_bomb()

            # walls.update()

            self.screen.fill((0, 0, 0))

            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, sprite.rect)

            pygame.display.flip()

            self.clock.tick(60)
            self.timer -= 1

    def _check_player_collision(self, objects, pressed_keys):
        collision = pygame.sprite.spritecollideany(self.player, objects)

        if collision:
            if pressed_keys[K_UP]:
                self.player.rect.top = collision.rect.bottom
            if pressed_keys[K_DOWN]:
                self.player.rect.bottom = collision.rect.top
            if pressed_keys[K_LEFT]:
                self.player.rect.left = collision.rect.right
            if pressed_keys[K_RIGHT]:
                self.player.rect.right = collision.rect.left

    def _check_is_on_bomb(self):
        for bomb in self.current_bombs:
            if not pygame.sprite.collide_rect(self.player, bomb):
                self.bombs.add(bomb)
                self.current_bombs.remove(bomb)


if __name__ == '__main__':
    bomberman = Bomberman()
    bomberman.run_game()
