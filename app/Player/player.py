import pygame.image

from app.settings import *
from app.Bomb.bomb import Bomb
from app.music import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(".\\images\\player_front.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.frames = 0

        self.set_bomb = pygame.mixer.Sound(".\\music\\Effects\\Bomberman SFX (1).wav")

    def update(self, pressed_keys, walls, bombs, all_sprites):
        self.frames += 1

        if pressed_keys[K_UP]:
            self.surf = pygame.image.load(".\\images\\player_back.png").convert_alpha()
            self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, 5)

        if pressed_keys[K_DOWN]:
            self.surf = pygame.image.load(".\\images\\player_front.png").convert_alpha()
            self.rect.move_ip(0, 5)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, -5)

        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load(".\\images\\player_left.png").convert_alpha()
            self.rect.move_ip(-5, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(5, 0)

        if pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load(".\\images\\player_right.png").convert_alpha()
            self.rect.move_ip(5, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(-5, 0)

        if pressed_keys[K_SPACE]:
            if self.frames > 60:
                self.set_bomb.play()
                bomb = Bomb((self.rect.x, self.rect.y))

                bombs.add(bomb)
                all_sprites.add(bomb)
                bombs.update()

                self.frames = 0

        self.keep_on_screen()

    def keep_on_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def keep_out_the_bomb(self):
        pass
        # TODO function that keep out from a bombs
