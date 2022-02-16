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

from app.bomb.bomb import Bomb
from app.wall.wall import Wall

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650
DEFAULT_OBJECT_SIZE = 50


class Player(pygame.sprite.Sprite):
    DIFFERENCE_BETWEEN_OBJECT = 35

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/player_front.png").convert()
        self.rect = self.surf.get_rect()
        self.counter = 60
        self.position_bomb = (0, 0)
        self.get_bomb = None

    def update(self, pressed_keys):
        self.counter += 1

        current_position = (self.rect.top,
                            self.rect.left,
                            self.rect.bottom,
                            self.rect.right)

        if pressed_keys[K_UP]:
            self.surf = pygame.image.load("images/player_back.png").convert()
            self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(player, walls) or \
                    pygame.sprite.spritecollideany(player, bombs):
                self.rect.top = current_position[0]
                self.rect.bottom = current_position[2]

        if pressed_keys[K_DOWN]:
            self.surf = pygame.image.load("images/player_front.png").convert()
            self.rect.move_ip(0, 5)
            if pygame.sprite.spritecollideany(player, walls) or \
                    pygame.sprite.spritecollideany(player, bombs):
                self.rect.top = current_position[0]
                self.rect.bottom = current_position[2]

        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load("images/player_left.png").convert()
            self.rect.move_ip(-5, 0)
            if pygame.sprite.spritecollideany(player, walls) or \
                    pygame.sprite.spritecollideany(player, bombs):
                self.rect.left = current_position[1]
                self.rect.right = current_position[3]

        if pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load("images/player_right.png").convert()
            self.rect.move_ip(5, 0)
            if pygame.sprite.spritecollideany(player, walls) or \
                    pygame.sprite.spritecollideany(player, bombs):
                self.rect.left = current_position[1]
                self.rect.right = current_position[3]

        if pressed_keys[K_SPACE]:
            if self.counter >= 60:
                boom = Bomb(self.rect.center)
                all_sprites.add(boom)
                self.get_bomb = boom
                self.position_bomb = boom.rect.center
                self.counter = 0

        position_player = self.rect.center
        if (self.position_bomb[1] - Player.DIFFERENCE_BETWEEN_OBJECT > position_player[1] or
            self.position_bomb[1] + Player.DIFFERENCE_BETWEEN_OBJECT < position_player[1]) or (
                self.position_bomb[0] - Player.DIFFERENCE_BETWEEN_OBJECT > position_player[0] or
                self.position_bomb[0] + Player.DIFFERENCE_BETWEEN_OBJECT < position_player[0]):

            if self.get_bomb is not None:
                bombs.add(self.get_bomb)
                self.get_bomb = None
                self.position_bomb = (0, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

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

        player.update(pressed_keys)

        walls.update()

        screen.fill((0, 0, 0))

        for sprite in all_sprites:
            screen.blit(sprite.surf, sprite.rect)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
