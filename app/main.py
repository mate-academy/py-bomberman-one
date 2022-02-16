import pygame

from app.game_objects.walls import Wall
from app.game_objects.player import Player
from app.game_objects.bombs import Bomb


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    QUIT,
)


class PossibleDirections:
    LEFT = (-5, 0)
    DOWN = (0, 5)
    RIGHT = (5, 0)
    UP = (0, -5)
    STAY = (0, 0)


class BomberGame:
    SCREEN_WIDTH = 650
    SCREEN_HEIGHT = 650
    DEFAULT_OBJECT_SIZE = 50
    TIME_BEFORE_BOMBS = 1000

    def __init__(self):
        self._init_pygame()
        self._init_game_constants()
        self._init_game_objects()

    def _init_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

    def _init_game_objects(self):
        self._player = Player()

        self.walls = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self._player)

        self._bombs = pygame.sprite.Group()

        for wall_center in Wall.create_centers_of_walls(
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), (self.DEFAULT_OBJECT_SIZE, self.DEFAULT_OBJECT_SIZE)
        ):
            wall = Wall(
                wall_center,
                self.DEFAULT_OBJECT_SIZE,
                self.DEFAULT_OBJECT_SIZE
            )
            self.walls.add(wall)
            self.all_sprites.add(wall)

    def _init_game_constants(self):
        self.player_direction = PossibleDirections.STAY
        self.player_opposite_direction = PossibleDirections.STAY
        self.running = None
        self._planting_time = None

    def _process_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.running = False
            if event.key == K_UP:
                self.player_direction = PossibleDirections.UP
                self.player_opposite_direction = PossibleDirections.DOWN
            if event.key == K_DOWN:
                self.player_direction = PossibleDirections.DOWN
                self.player_opposite_direction = PossibleDirections.UP
            if event.key == K_LEFT:
                self.player_direction = PossibleDirections.LEFT
                self.player_opposite_direction = PossibleDirections.RIGHT
            if event.key == K_RIGHT:
                self.player_direction = PossibleDirections.RIGHT
                self.player_opposite_direction = PossibleDirections.LEFT

            if event.key == K_SPACE:
                print('Space pressed')
                self._plant_bomb()

        elif event.type == KEYUP:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                self.player_direction = PossibleDirections.STAY

        elif event.type == QUIT:
            self.running = False

    def _validate_player_position(self):
        player_borders = self._player.borders
        return (
            player_borders.left >= 0
            and player_borders.right <= self.SCREEN_WIDTH
            and player_borders.top >= 0
            and player_borders.bottom <= self.SCREEN_HEIGHT
        )

    def _move_player(self):
        self._player.move(self.player_direction)
        if not self._validate_player_position() or pygame.sprite.spritecollideany(self._player, self.walls):
            self._player.move(self.player_opposite_direction)

    def _plant_bomb(self):
        if (self._planting_time is None
                or pygame.time.get_ticks() - self._planting_time >= self.TIME_BEFORE_BOMBS):
            self._planting_time = pygame.time.get_ticks()
            planted_bomb = Bomb.create_bomb(self._player.borders)
            self._bombs.add(planted_bomb)
            self.all_sprites.add(planted_bomb)

    def play_game(self):

        self.running = True

        while self.running:

            for event in pygame.event.get():
                self._process_event(event)

            self._move_player()

            self.walls.update()
            self.screen.fill((0, 0, 0))
            for sprite in self.all_sprites:
                self.screen.blit(sprite.surf, sprite.rect)

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == '__main__':
    game = BomberGame()
    game.play_game()
