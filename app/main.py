import pygame
from app.Player.player import Player
from app.Wall.wall import Wall
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from app.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    DEFAULT_OBJECT_SIZE,
    grass_img,
)

if __name__ == "__main__":
    # Setup for sounds
    pygame.mixer.init()

    # Initialize program
    pygame.init()
    clock = pygame.time.Clock()

    # Background music
    pygame.mixer.music.load(".\\music\\main_melody.mp3")
    pygame.mixer.music.play(loops=-1)

    # Set screen size
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
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

        # Get all currently pressed
        pressed_keys = pygame.key.get_pressed()
        # Update the player sprite based on user key presses
        player.update(pressed_keys, walls, bombs, all_sprites)
        walls.update()

        # Background
        screen.blit(grass_img, (0, 0))

        for sprite in all_sprites:
            screen.blit(sprite.surf, sprite.rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()
