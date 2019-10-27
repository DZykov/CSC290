import pygame


class Player(object):

    def __init__(self, screen, screen_size, size, colour):
        self.x = screen_size[0] / 2
        self.y = screen_size[1] - size - 5
        self.size = size
        self.colour = colour
        self.screen = screen
        self.screen_size = screen_size
        self.prev_coord = (self.x, self.y)

    def draw(self):
        pygame.draw.rect(self.screen, self.colour,
                         pygame.Rect(self.x, self.y, self.size, self.size))

    def move(self, x, y):
        self.prev_coord = (self.x, self.y)
        self.x += x
        self.y += y

    def control(self, pressed_key):
        self.prev_coord = (self.x, self.y)
        # if pressed_key[pygame.K_UP]: self.y += -5
        # if pressed_key[pygame.K_DOWN]: self.y += 5
        if pressed_key[pygame.K_LEFT]: self.x += -5
        if pressed_key[pygame.K_RIGHT]: self.x += 5
        if self.x <= 0 or self.x >= self.screen_size[0] - self.size:
            self.x = self.prev_coord[0]
        if self.y <= 0 or self.y >= self.screen_size[1] - self.size:
            self.y = self.prev_coord[1]
        if pressed_key[pygame.K_SPACE]:
            bullet = Bullet(self.screen, self.screen_size, 3, (0,255,0), self.x+self.size/2,
                            self.screen_size[1]-self.size-10)
            print("WTF", bullet.x, "||", bullet.y)

class TestsNIC:
    def __init__(self):
        pass

class Laser:
    def __init__(self, colour, x, y, spd, dmg, file):
        self.x = x
        self.y = y
        self.spd = spd
        self.dmg = dmg
        self.colour = colour
        self.icon = pygame.image.load(file)
    def move(self):
        self.y += self.spd


class Barrier:
    def __init__(self, x, y, hp, file):

        self.x = x
        self.y = y
        self.hp = hp
        self.icon = pygame.image.load(file)
        self.screen = screen

    def remove(self,):
        pass
    def apperarence(self,file1,file2,file3):
        if self.hp == 100:

            self.icon = pygame.image.load(file1)

        elif self.hp >50 and self.hp<100:
            self.icon = pygame.image.load(file2)
        elif self. hp <= 50 and self.hp > 0:
            self.icon = pygame.image.load(file3)
        elif self.hp <= 0:
            pass




class Invaders:

    def __init__(self, screen, screen_size, size, colour, x, y):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.screen = screen
        self.screen_size = screen_size

    def draw(self):
        pygame.draw.rect(self.screen, self.colour,
                         pygame.Rect(self.x, self.y, self.size, self.size))

    def move(self, x, y):
        self.x += x
        self.y += y


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
                         invader.colour,
                         10 + x * (self.space_between_enemies + self.enemy_size), invader.y)
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
        self.move(0, -1)

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

player = Player(screen, screen_size, player_size, red)

invader = Invaders(screen, screen_size, player_size, blue, 0, 0)
invader1 = Invaders(screen, screen_size, player_size, green, 0,
                    player_size+enemy_y_gap)
invader2 = Invaders(screen, screen_size, player_size, blue, 0, 2*(player_size+enemy_y_gap))
invader3 = Invaders(screen, screen_size, player_size, green, 0, 3*(player_size+enemy_y_gap))

invaders = Group(invader)
invaders1 = Group(invader1)
invaders2 = Group(invader2)
invaders3 = Group(invader3)

barrier = Barrier(0,0,100,"C:/Users/Klaudius/Desktop/290 project/CSC290/wall-24.png")

while play:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    screen.fill(background)

    invaders.draw()
    invaders1.draw()
    invaders2.draw()
    invaders3.draw()
    invaders.cycle()
    invaders1.cycle()
    invaders2.cycle()
    invaders3.cycle()

    pressed_key = pygame.key.get_pressed()
    player.control(pressed_key)

    player.draw()

    pygame.display.flip()
    clock.tick(60)
