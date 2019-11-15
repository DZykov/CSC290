import random

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
        self.screen_size = screen_size  # this part is undone

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

    def __init__(self, screen_size, size, string, x, y):
        sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.transform.scale((image.load(string)),
                                            (size, size))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.screen_size = screen_size
        self.prev_coord = (self.x, self.y)

    def move(self, x, y):
        if 0 <= self.x + x <= self.screen_size[0] and 0 <= self.y + y <= \
                self.screen_size[1]:
            self.x += x
            self.y += y
            self.rect = self.rect.move((x, y))


class InvadersGroup(sprite.Group):
    def __init__(self, screen_size, size, space):
        sprite.Group.__init__(self)
        self.screen_size = screen_size
        self.size = size
        self.rows = int(
            screen_size[0] / 100 * 75 /
            (size + space))
        self.columns = 4
        self.invaders = []
        self.n = len(self.invaders)
        self.de_way = "R"
        self.died = 0

    def move(self, x, y):
        for invader in self.invaders:
            invader.move(x, y)

    def update(self):
        if self.de_way == "L":
            self.move(-1, 0)
            if self.invaders[0].x - self.invaders[-1].size <= 0:
                self.de_way = "R"
        if self.de_way == "R":
            self.move(1, 0)
            if self.invaders[-1].x >= \
                    self.screen_size[0] - self.invaders[-1].size:
                self.de_way = "L"

    def add_internal(self, *sprites):
        super(InvadersGroup, self).add_internal(*sprites)
        for s in sprites:
            self.invaders.append(s)

    def remove_internal(self, *sprites):
        super(InvadersGroup, self).remove_internal(*sprites)
        for s in sprites:
            self.kill(s)

    def kill(self, enemy):
        self.n = -1
        self.died = +1
        self.invaders.remove(enemy)
        del enemy

    def shoot(self):
        a = random.choice(self.invaders)
        return a.x, a.y


class Environment(object):
    def __init__(self):
        init()
        self.screen_size = (800, 400)
        background = (0, 0, 0)
        red = (255, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        self.size = 30
        self.gap = 20

        self.max_bullets = 3  # number of bullets allowed
        self.bullets = sprite.Group()
        self.enemy_bullets = sprite.Group()

        self.invaders = self.create_invaders()

        self.keys = key.get_pressed()
        self.screen = pygame.display.set_mode(
            (self.screen_size[0], self.screen_size[1]))
        self.play = True
        self.clock = pygame.time.Clock()

        self.player = Player(self.screen_size, self.size)

        self.all_sprites = sprite.Group()
        self.all_sprites.add(self.player)

        while self.play:
            self.clock.tick(60)
            self.screen.fill(background)

            self.check_control()
            self.check_collision()

            self.invaders_shoot()

            self.all_sprites.update()
            self.invaders.update()

            self.invaders.draw(self.screen)
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
                                        self.player.y - self.player.size, -3, 0,
                                        self.screen_size)
                        self.bullets.add(bullet)
                        self.all_sprites.add(self.bullets)

    def check_collision(self):
        # checks for single sprite ->
        # sprite.groupcollide(self.GroupEnemy, self.bullets,
        # True, True).keys():check for sprites
        pygame.sprite.groupcollide(self.invaders, self.bullets, True, True)
        pygame.sprite.groupcollide(self.enemy_bullets, self.bullets, True, True)
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            self.play = False

    def create_invaders(self):
        invaders = InvadersGroup(self.screen_size, self.size, self.gap)
        n = int(
            self.screen_size[0] / 100 * 75 /
            (self.size + self.gap))
        break_p = self.size + self.gap
        for i in range(n):
            invader = Invader(self.screen_size, self.size, "invader1.png", i*(self.gap+self.size), break_p)
            invaders.add(invader)
        for i in range(n):
            invader = Invader(self.screen_size, self.size, "invader2.png", i*(self.gap+self.size), 2*break_p)
            invaders.add(invader)
        for i in range(n):
            invader = Invader(self.screen_size, self.size, "invader3.png", i*(self.gap+self.size), 3*break_p)
            invaders.add(invader)
        return invaders

    def invaders_shoot(self):
        a = random.randint(0, 1000)
        if a <= 50:
            x, y = self.invaders.shoot()
            bullet = Bullet(x, y + self.size, 3, 0, self.screen_size)
            self.enemy_bullets.add(bullet)
            self.all_sprites.add(self.enemy_bullets)

    
class Menu(object):
    def __init__(self):
        self.screen_size = (800, 400)
        background = (0, 0, 0)
        self.screen = pygame.display.set_mode((self.screen_size[0], self.screen_size[1])) 
        self.run = True 
        self.clock = pygame.time.Clock()

        while self.run:            
            self.screen.fill(background)
            pygame.time.delay(5000)
            self.run = False        


if __name__ == '__main__':
    Menu()
    Environment()
