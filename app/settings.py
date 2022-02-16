import pygame

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650
DEFAULT_OBJECT_SIZE = 50

# Colors
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CRIMSON = (220, 20, 60)

# Media images
grass_img = pygame.image.load('.\\images\\grass.png')
grass_img = pygame.transform.scale(grass_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND = pygame.image.load(".\\images\\background2.png")

# Media images Player
player_front = pygame.image.load(".\\images\\player_front.png")
player_back = pygame.image.load(".\\images\\player_back.png")
player_left = pygame.image.load(".\\images\\player_left.png")
player_right = pygame.image.load(".\\images\\player_right.png")

# Media sounds
