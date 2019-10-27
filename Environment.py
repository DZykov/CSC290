from pygame import *
import pygame


class Player(sprite.Sprite):

    def __init__(self, screen, screen_size, size):
        sprite.Sprite.__init__(self)
        self.x = screen_size[0] / 2
        self.y = screen_size[1] - size - 5
        self.size = size
        self.image = pygame.transform.scale((image.load("ship.png")), (size, size))
        # crunch to rotate an image
        # image will be changed in ps
        self.image = pygame.transform.rotate(self.image, 135)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.screen = screen
        self.screen_size = screen_size
        self.prev_coord = (self.x, self.y)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def move(self, x, y):
        self.x += x
        self.y += y
        self.rect = self.rect.move((x, y))

    def control(self, pressed_key):
        self.prev_coord = (self.x, self.y)
        if pressed_key[pygame.K_LEFT]:
            if 0 <= self.x - 5 <= self.screen_size[0] - self.size:
                self.move(-5, 0)
        if pressed_key[pygame.K_RIGHT]:
            if 0 <= self.x + 5 <= self.screen_size[0] - self.size:
                self.move(5, 0)
        if pressed_key[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        bullet = Bullet(self.screen, self.screen_size, 3, (0, 255, 0),
                        self.x + self.size / 2,
                        self.screen_size[1] - self.size - 10)
        bullet.cycle()
        del bullet


class Invaders(sprite.Sprite):

    def __init__(self, screen, screen_size, size, pic, x, y):
        sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.im = pic
        self.pic = pygame.transform.scale((image.load(pic)), (size, size))
        self.rect = self.pic.get_rect(center=(self.x, self.y))
        self.screen = screen
        self.screen_size = screen_size

    def draw(self):
        self.screen.blit(self.pic, self.rect)

    def move(self, x, y):
        self.x += x
        self.y += y
        self.rect = self.rect.move((x, y))


class Group:

    def __init__(self, invader):
        self.enemy_size = invader.size
        self.space_between_enemies = 10
        self.enemy_number = int(
            invader.screen_size[0] / 100 * 75 /
            (self.enemy_size + self.space_between_enemies))
        invaders = []
        for x in range(self.enemy_number):
            a = Invaders(invader.screen, invader.screen_size, invader.size,
                         invader.im,
                         10 + x * (
                                 self.space_between_enemies + self.enemy_size),
                         invader.y)
            invaders.append(a)
        self.invaders = invaders
        self.de_way = "R"

    def draw(self):
        for invader in self.invaders:
            invader.draw()

    def cycle(self):
        if self.de_way == "L":
            self.move(-1, 0)
            if self.invaders[0].x <= 0:
                self.de_way = "R"
        if self.de_way == "R":
            self.move(1, 0)
            if self.invaders[-1].x + self.enemy_size >= \
                    self.invaders[-1].screen_size[0]:
                self.de_way = "L"

    def move(self, x, y):
        for invader in self.invaders:
            invader.move(x, y)


class Bullet:

    def __init__(self, screen, screen_size, length, colour, x, y):
        self.x = x
        self.y = y
        self.length = length
        self.width = 10
        self.colour = colour
        self.screen = screen
        self.screen_size = screen_size

    def draw(self):
        pygame.draw.rect(self.screen, self.colour,
                         pygame.Rect(self.x, self.y, self.length, self.width))

    def move(self, x, y):
        self.x += x
        self.y += y

    def cycle(self):
        self.draw()
        while self.y >= 0:
            self.move(0, -1)
            self.draw()


class Environment:

    pygame.init()
    screen_size = (800, 400)
    background = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    player_size = 30
    enemy_y_gap = 20

    screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
    play = True
    clock = pygame.time.Clock()

    player = Player(screen, screen_size, player_size)

    invader1 = Invaders(screen, screen_size, player_size, "invader1.png", 0,
                        player_size + enemy_y_gap)
    invader2 = Invaders(screen, screen_size, player_size, "invader2.png", 0,
                        2 * (player_size + enemy_y_gap))
    invader3 = Invaders(screen, screen_size, player_size, "invader3.png", 0,
                        3 * (player_size + enemy_y_gap))

    invaders1 = Group(invader1)
    invaders2 = Group(invader2)
    invaders3 = Group(invader3)

    while play:

        clock.tick(60)
        screen.fill(background)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

        invaders1.draw()
        invaders2.draw()
        invaders3.draw()

        invaders1.cycle()
        invaders2.cycle()
        invaders3.cycle()

        pressed_key = pygame.key.get_pressed()
        player.control(pressed_key)

        player.draw()

        pygame.display.flip()


if __name__ == '__main__':
    Environment()
