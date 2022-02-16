from app.settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((20, 40))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect()

        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, pressed_keys, walls):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, 5)

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, -5)

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(5, 0)

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(-5, 0)

        self.keep_on_screen()
        # self.cannot_walk_over_the_walls(walls)

    def keep_on_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def cannot_walk_over_the_walls(self, walls):
        pass
            # print("TRUE")
            # self.rect.move_ip(-1, -1)
