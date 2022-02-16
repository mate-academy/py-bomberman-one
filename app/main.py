import pygame
from pygame import KEYDOWN, K_ESCAPE, QUIT

from app.settings import (
    screen,
    clock,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    DEFAULT_OBJECT_SIZE,
    BACKGROUND_COLOR)
from app.player.player import Player
from app.walls.wall import Wall


class Bomberman:
    def __init__(self):
        self.walls = None
        self.bombs = None
        self.tmp_bombs = None
        self.all_sprites = None
        self.player = None
        self.pressed_keys = None
        self.running = True
        self.bomb = None
        self.preparation()

    def start_game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE:
                        self.bomb = self.player.plant_bomb()
                        if self.bomb:
                            self.tmp_bombs.add(self.bomb)
                            self.all_sprites.add(self.bomb)

                elif event.type == QUIT:
                    self.running = False

            self.pressed_keys = pygame.key.get_pressed()

            if self.bomb:
                if not pygame.sprite.spritecollideany(
                        self.player, self.tmp_bombs):
                    self.bombs.add(self.bomb)

            self.player.update()

            self.bombs.update()
            self.walls.update()

            screen.fill(BACKGROUND_COLOR)

            for sprite in self.all_sprites:
                screen.blit(sprite.surf, sprite.rect)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def preparation(self):
        self.player = Player(self)

        self.walls = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.tmp_bombs = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        for wall_center in Wall.create_centers_of_walls(
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                (DEFAULT_OBJECT_SIZE, DEFAULT_OBJECT_SIZE)
        ):
            wall = Wall(wall_center)
            self.walls.add(wall)
            self.all_sprites.add(wall)


if __name__ == "__main__":
    bomberman = Bomberman()
    bomberman.start_game()
