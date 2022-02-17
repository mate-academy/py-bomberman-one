import pygame

from wall import Wall
from bomb import Bomb

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

# Import and initialize the pygame library
pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650
DEFAULT_OBJECT_SIZE = 50
# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.timer = 0
        self.surf = \
            pygame.image.load("images/player_right.png").convert_alpha()
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses
    def update(self):

        self.timer += 1

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            self.surf = \
                pygame.image.load("images/player_back.png").convert_alpha()
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, 5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            self.surf = \
                pygame.image.load("images/player_front.png").convert_alpha()
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, -5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.surf = \
                pygame.image.load("images/player_left.png").convert_alpha()
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.surf = \
                pygame.image.load("images/player_right.png").convert_alpha()
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(-5, 0)

        if pressed_keys[K_SPACE]:
            if self.timer >= 60:
                bomb = Bomb((self.rect.x, self.rect.y))
                all_sprites.add(bomb)
                bombs.add(bomb)
                self.timer = 0

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


player = Player()

bombs = pygame.sprite.Group()
walls = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

for wall_center in Wall.create_centers_of_walls(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        (DEFAULT_OBJECT_SIZE, DEFAULT_OBJECT_SIZE)
):
    wall = Wall(wall_center)
    walls.add(wall)
    all_sprites.add(wall)

# Run until the user asks to quit
running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    player.update()

    walls.update()

    bombs.update()

    # Fill the background
    screen.fill((0, 0, 0))

    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
