from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_OBJECT_SIZE,\
    PLAYER_FRONT, PLAYER_BACK, PLAYER_LEFT, PLAYER_RIGHT
from app.bomb import Bomb
from app.walls import Wall
import pygame
import time


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class Player(pygame.sprite.Sprite):
    timeout = 0

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(PLAYER_FRONT)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if time.time() - Player.timeout >= 1 and pressed_keys[K_SPACE]:
            self.plant_bomb()

        if pressed_keys[K_UP]:
            self.surf = pygame.image.load(PLAYER_BACK)
            self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(0, 5)

        if pressed_keys[K_DOWN]:
            self.surf = pygame.image.load(PLAYER_FRONT)
            self.rect.move_ip(0, 5)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(0, -5)

        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load(PLAYER_LEFT)
            self.rect.move_ip(-5, 0)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(5, 0)

        if pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load(PLAYER_RIGHT)
            self.rect.move_ip(5, 0)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(-5, 0)

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def plant_bomb(self):
        bomb = Bomb(self)
        bombs.add(bomb)
        all_sprites.add(bomb)
        Player.timeout = time.time()


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
    player.update(pressed_keys)

    walls.update()

    screen.fill((0, 100, 100))

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
