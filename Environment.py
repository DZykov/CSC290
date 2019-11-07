from pygame import *
import pygame


class Player(sprite.Sprite):

    def __init__(self, screen_size, size):
        sprite.Sprite.__init__(self)
        self.x = screen_size[0] / 2
        self.y = screen_size[1] - size - 5
        self.size = size
        self.image = pygame.transform.scale((image.load("ship.png")),
                                            (size, size))
        # crunch to rotate an image
        # image will be changed in ps
        self.image = pygame.transform.rotate(self.image, 135)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.screen_size = screen_size
        self.prev_coord = (self.x, self.y)

    def move(self, x, y):
        self.x += x
        self.y += y
        self.rect = self.rect.move((x, y))

    def update(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_LEFT]:
            if 0 <= self.x - 5 <= self.screen_size[0]:
                self.move(-5, 0)
        if pressed_key[pygame.K_RIGHT]:
            if 0 <= self.x + 5 <= self.screen_size[0]:
                self.move(5, 0)


class Bullet(sprite.Sprite):

    def __init__(self, x, y, speedy, speedx, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 8))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom, self.y = y, y
        self.rect.centerx, self.x = x, x
        self.speedy = speedy
        self.speedx = speedx
        self.screen_size = screen_size # this part is undone

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        self.y += self.speedy
        self.x += self.speedx
        # kill if it moves off the top of the screen
        # REDO it
        if self.y < 0 or self.y > self.screen_size[1] or \
                self.x < 0 or self.x > self.screen_size[0]:
            self.kill()


class Invader(sprite.Sprite):

    def __init__(self, screen_size, size, string):
        sprite.Sprite.__init__(self)
        self.x = 20
        self.y = 20
        self.size = size
        self.image = pygame.transform.scale((image.load(string)),
                                            (size, size))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.screen_size = screen_size
        self.prev_coord = (self.x, self.y)

    def move(self, x, y):
        if 0 <= self.x + x <= self.screen_size[0] and 0 <= self.y + y <= self.screen_size[1]:
            self.x += x
            self.y += y
            self.rect = self.rect.move((x, y))


class EnemiesGroup(sprite.Group):
    def __init__(self, screen_size, size):
        sprite.Group.__init__(self)

    def update(self):
        pass


class Environment(object):
    def __init__(self):
        init()
        self.screen_size = (800, 400)
        background = (0, 0, 0)
        red = (255, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        size = 30
        enemy_y_gap = 20

        self.max_bullets = 3  # number of bullets allowed
        self.bullets = sprite.Group()

        self.keys = key.get_pressed()
        self.screen = pygame.display.set_mode((self.screen_size[0], self.screen_size[1]))
        self.play = True
        self.clock = pygame.time.Clock()

        self.player = Player(self.screen_size, size)

        # demo line
        self.enemy = Invader(self.screen_size, size, "invader1.png")

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.enemy)
        self.all_sprites.add(self.player)

        while self.play:
            self.clock.tick(60)
            self.screen.fill(background)

            self.check_control()
            self.check_collision()

            self.all_sprites.update()
            self.all_sprites.draw(self.screen)

            pygame.display.flip()

    def check_control(self):
        self.keys = key.get_pressed()
        for e in event.get():
            if e.type == pygame.QUIT:
                self.play = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if len(self.bullets) < self.max_bullets:
                        bullet = Bullet(self.player.x,
                                        self.player.y - self.player.size, -3, 0, self.screen_size)
                        self.bullets.add(bullet)
                        self.all_sprites.add(self.bullets)

    def check_collision(self):
        # checks for single sprite ->
        # sprite.groupcollide(self.GroupEnemy, self.bullets,
        # True, True).keys():check for sprites
        hits = sprite.spritecollide(self.enemy, self.bullets, True)
        if hits:
            self.all_sprites.remove(self.enemy)
            self.enemy.x = -10
            self.enemy.y = -10
            self.enemy.kill()


if __name__ == '__main__':
    Environment()
