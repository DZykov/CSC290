import random
from pygame import *
import pygame
import math
import sys
import datetime


class Player(sprite.Sprite):
    """
    This is a Player Class which is a subclass of pygame.sprite.Sprite
    Player Class creates controllable object
    Attributes:
        x: An integer represents x coordinate
        y: An integer represents y coordinate
        size: An integer represents the size of the player
        image: An image which is loaded to the memory
        rect: The outline of the image; needed for detecting collisions
        screen_size: A Tuple(Integer, Integer) represents the screen size
        health: An integer represent the health of the player
    """

    def __init__(self, screen_size, size, color):
        """
        Inits Player class with given attributes
        """
        sprite.Sprite.__init__(self)
        self.x = screen_size[0] / 2
        self.y = screen_size[1] - size - 5
        self.size = size
        self.color = color + (255,)
        self.image = pygame.transform.scale((image.load("Objects/ship.png")),
                                            (size, size))
        self.image = pygame.transform.rotate(self.image, 135)

        pixels = PixelArray(self.image)
        pixels.replace(Color(255, 255, 255, 255), self.color)
        del pixels
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.screen_size = screen_size
        self.health = 10
        self.speedx = 5
        self.speedy = 5

    def move(self, x, y):
        """
        Moves Player by given x and y
        """
        self.x += x
        self.y += y
        self.rect = self.rect.move((x, y))

    def update(self):
        """
        Overrides and calls the update method for this specific sprite
        """
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_LEFT]:
            if 0 <= self.x - self.speedx <= self.screen_size[0]:
                self.move(-self.speedx, 0)
        if pressed_key[pygame.K_RIGHT]:
            if 0 <= self.x + self.speedx <= self.screen_size[0]:
                self.move(self.speedx, 0)


class Bullet(sprite.Sprite):
    """
    This is a Bullet Class which is a subclass of pygame.sprite.Sprite
    Bullet Class creates uncontrollable object with specific behaviour
    Attributes:
        x: An integer represents x coordinate
        y: An integer represents y coordinate
        image: An image which is loaded to the memory
        rect: The outline of the image; needed for detecting collisions
        screen_size: A Tuple(Integer, Integer) represents the screen size
        speedx: An integer represents the speed of Bullet on x-axis
        speedy: An integer represents the speed of Bullet on y-axis
    """

    def __init__(self, x, y, speedy, speedx, screen_size, color):
        """
        Inits Bullet class with given attributes
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 8))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.bottom, self.y = y, y
        self.rect.centerx, self.x = x, x
        self.speedy = speedy
        self.speedx = speedx
        self.screen_size = screen_size  # this part is undone

    def update(self):
        """
        Overrides and calls the update method for this specific sprite
        """
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        self.y += self.speedy
        self.x += self.speedx
        if self.y < 0 or self.y > self.screen_size[1] or \
                self.x < 0 or self.x > self.screen_size[0]:
            self.kill()


class Invader(sprite.Sprite):
    """
    This is an Invader Class which is a subclass of pygame.sprite.Sprite
    Invader Class creates uncontrollable object
    Attributes:
        x: An integer represents x coordinate
        y: An integer represents y coordinate
        size: An integer represents the size of the player
        image: An image which is loaded to the memory
        rect: The outline of the image; needed for detecting collisions
        screen_size: A Tuple(Integer, Integer) represents the screen size
        health: An integer represent the health of the player
    """

    def __init__(self, screen_size, size, string, x, y):
        """
        Inits Invader class with given attributes
        """
        sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.transform.scale((image.load(string)),
                                            (size, size))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.screen_size = screen_size
        self.health = 1

    def move(self, x, y, enemies_left):
        """
        Moves Invader by given x and y
        """
        if enemies_left > 14:
            if 0 <= self.x + x <= self.screen_size[0] and 0 <= self.y + y <= \
                    self.screen_size[1]:
                self.x += x
                self.y += y
                self.rect = self.rect.move((x, y))
        else:
            if 0 <= self.x + x <= self.screen_size[0] and 0 <= self.y + self.get_sin(self.x) <= \
                    self.screen_size[1]:
                self.x += x
                self.y += self.get_sin(self.x)
                self.rect = self.rect.move((x, self.get_sin(self.x)))
            elif 0 <= self.x + x <= self.screen_size[0] and self.y + self.get_sin(self.x) >= \
                    self.screen_size[1]:
                self.x += x
                self.y -= self.get_sin(self.x)
                self.rect = self.rect.move((x, -self.get_sin(self.x)))

    def get_sin(self, x) -> float:
        """
        Returns the value of sin(<X>) as relative to the screen.
        """
        y = -2*math.sin(x/10)
        return y


class InvadersGroup(sprite.Group):
    """
    This is an InvadersGroup Class which is a subclass of pygame.sprite.Group
    InvadersGroup Class is a collection of uncontrollable objects that
        subclasses of pygame.sprite.Sprite
    Attributes:
        screen_size: A Tuple(Integer, Integer) represents the size of a screen
        size: An integer represents the size of each member of InvadersGroup
        space: An integer represent the space between each member
        invaders: A list with every member of InvadersGroup Class
        de_way: A string "L" or "R" indicates the direction of movement
        died: An integer represents the number of members destroyed
    """

    def __init__(self, screen_size, size, space):
        """
        Init InvadersGroup with given attributes
        """
        sprite.Group.__init__(self)
        self.screen_size = screen_size
        self.size = size
        self.space = space
        self.invaders = []
        self.de_way = "R"
        self.died = 0

    def move(self, x, y, health):
        """
        Moves each member of InvadersGroup by given x and y
        """
        for invader in self.invaders:
            invader.move(x, y, len(self.invaders))

    def update(self, health):
        """
        Calls the update method of every member sprite
        Group.update(*args): return None
        Calls the update method of every member sprite. All arguments that
        were passed to this method are passed to the Sprite update function.
        """
        if len(self.invaders) == 0:
            pass
        elif self.de_way == "L":
            self.move(-1, 0, health)
            if self.invaders[0].x - self.invaders[-1].size <= 0:
                self.de_way = "R"
        elif self.de_way == "R":
            self.move(1, 0, health)
            if self.invaders[-1].x >= \
                    self.screen_size[0] - self.invaders[-1].size - self.space:
                self.de_way = "L"

    def add_internal(self, *sprites):
        """
        Adds new member to InvadersGroup
        """
        super(InvadersGroup, self).add_internal(*sprites)
        for s in sprites:
            self.invaders.append(s)

    def remove_internal(self, *sprites):
        """
        Removes and deletes all given sprite from InvadersGroup
        """
        super(InvadersGroup, self).remove_internal(*sprites)
        for s in sprites:
            self.kill(s)

    def kill(self, enemy):
        """
        Deletes given member of InvadersGroup and deletes given sprite itself
        """
        self.died = +1
        self.invaders.remove(enemy)
        del enemy

    def shooter(self):
        """
        Chooses random member of InvadersGroup and return its coordinates
        """
        if len(self.invaders) > 0:
            shoot = pygame.mixer.Sound('Sounds/laser_invader.ogg')
            shoot.play()
            a = random.choice(self.invaders)
            return a.x, a.y


class Barrier(sprite.Sprite):
    def __init__(self, screen_size, size, string1, string2, string3, x, y):
        sprite.Sprite.__init__(self)
        self.health = 10
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.transform.scale((image.load(string1)), (size * 3, size))
        self.image2 = pygame.transform.scale((image.load(string2)), (size * 3, size))
        self.image3 = pygame.transform.scale((image.load(string3)), (size * 3, size))
        self.rect = self.image.get_rect(center=(self.x * 5, self.y))
        self.screen_size = screen_size

    def move(self, x, y):
        if 0 <= self.x + x <= self.screen_size[0] and 0 <= self.y + y <= \
                self.screen_size[1]:
            self.x += x
            self.y += y
            self.rect = self.rect.move((x, y))

    def update(self):
        if 0 < self.health < 7:
            self.image = self.image2
        if 0 < self.health < 3:
            self.image = self.image3


class BarrierGroup(sprite.Group):
    def __init__(self, screen_size, size, space):
        sprite.Group.__init__(self)
        self.screen_size = screen_size
        self.size = size
        self.space = space
        self.barriers = []
        self.way = "R"

    def move(self, x, y):
        for barrier in self.barriers:
            barrier.move(x, y)

    def move(self, x, y):
        for barrier in self.barriers:
            barrier.move(x, y)

    def update(self):
        if len(self.barriers) == 0:
            pass
        elif self.way == "L":
            self.move(-1, 0)
            if self.barriers[0].x - self.barriers[-1].size <= 20:
                self.way = "R"
        elif self.way == "R":
            self.move(1, 0)
            if self.barriers[-1].x >= \
                    self.screen_size[0] - 2.5*self.space - self.barriers[-1].size :
                self.way = "L"

    def add_internal(self, *sprites):
        super(BarrierGroup, self).add_internal(*sprites)
        for x in sprites:
            self.barriers.append(x)

    def remove_internal(self, *sprites):
        """
        Removes and deletes all given sprite from InvadersGroup
        """
        super(BarrierGroup, self).remove_internal(*sprites)
        for x in sprites:
            self.barriers.remove(x)
            del x


class Environment(object):
    """
    Creates environment, all objects and 'physics'
    """

    def __init__(self, color):
        """
        Inits Environment class
        """
        pygame.init()

        pygame.mixer.music.load('Music/8_bit_song.ogg')
        pygame.mixer.music.play(-1)

        background = (0, 0, 0)

        self.screen_size = (800, 400)
        self.size = 30
        self.gap = 20
        self.color = color

        self.max_bullets = 3  # number of bullets allowed
        self.bullets = sprite.Group()
        self.enemy_bullets = sprite.Group()

        self.invaders = self.create_invaders()
        self.barriers = self.create_barriers()

        self.keys = key.get_pressed()
        self.screen = pygame.display.set_mode(
            (self.screen_size[0], self.screen_size[1]))
        self.play = True
        self.clock = pygame.time.Clock()

        self.player = Player(self.screen_size, self.size, self.color)

        self.all_sprites = sprite.Group()
        self.all_sprites.add(self.player)

        self.start_time = datetime.datetime.now()
        self.ship_hit = False
        self.dead = False

        pygame.font.init()
        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, 20)
        label_lost = font_renderer.render(str("YOU LOST!"), 1, (255, 255, 255))
        label_win = font_renderer.render(str("YOU WON!"), 1, (255, 255, 255))
        edge_crossed = False

        while self.play:
            self.clock.tick(60)
            self.screen.fill(background)

            self.check_control()
            self.check_collision()

            self.invaders_shoot()

            self.all_sprites.update()
            self.invaders.update(self.player.health)
            self.barriers.update()

            self.invaders.draw(self.screen)
            self.barriers.draw(self.screen)
            self.all_sprites.draw(self.screen)

            if self.dead:
                self.screen.blit(label_lost, (self.screen_size[0]/2, self.screen_size[1]/3))
                self.player.move(0, self.player.speedy)

            if len(self.invaders) == 0:
                self.screen.blit(label_win, (self.screen_size[0] / 2, self.screen_size[1] / 3))
                if self.player.y >= 0:
                    self.player.move(0, -self.player.speedy)
                else:
                    edge_crossed = True

            if edge_crossed:
                self.play = False
                main()

            pygame.display.flip()

    def check_control(self):
        """
        This method check for keyboard interaction which influences
        only Environment
        """
        self.keys = key.get_pressed()
        for e in event.get():
            if e.type == pygame.QUIT:
                self.play = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if len(self.bullets) < self.max_bullets:
                        shoot = pygame.mixer.Sound('Sounds/laser_ship.ogg')
                        shoot.play()
                        bullet = Bullet(self.player.x,
                                        self.player.y - self.player.size, -3, 0,
                                        self.screen_size, (255, 255, 0))
                        self.bullets.add(bullet)
                        self.all_sprites.add(self.bullets)

    def check_collision(self):
        """
        Preconditions: self.invaders, self.bullets, self.enemy_bullets and
                            self.player are initialized anf none empty
        Checks the collision for all objects in the Environment and proceeds
        with specific instructions
        """
        pygame.font.init()
        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, 14)

        hits = pygame.sprite.groupcollide(self.invaders, self.bullets, False,
                                          True)

        for hit in hits:
            hit.health = hit.health - 1
            if hit.health <= 0:
                shoot = pygame.mixer.Sound('Sounds/explosion_invader.ogg')
                shoot.play()
                self.invaders.remove_internal(hit)
        pygame.sprite.groupcollide(self.enemy_bullets, self.bullets, True, True)
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            self.ship_hit = True
            self.player.health = self.player.health - 1
            if self.player.health <= 0:
                self.dead = True
                shoot = pygame.mixer.Sound('Sounds/ship_explosion.wav')
                shoot.play()
                self.player.speedx = 0

        if self.ship_hit:
            label = font_renderer.render(
                str(self.player.health), 1, (255, 255, 255))
            self.screen.blit(label, (self.player.x + 15, self.player.y - 7))
            diff_sec = (datetime.datetime.now() - self.start_time).total_seconds()
            if diff_sec > 5:
                self.start_time = datetime.datetime.now()
                self.ship_hit = False
                if self.dead:
                    self.play = False
                    main()

        hit_barrier = pygame.sprite.groupcollide(self.barriers, self.enemy_bullets, False, True)
        for hit in hit_barrier:
            hit.health = hit.health - 1
            hit.update()
            if hit.health <= 0:
                shoot = pygame.mixer.Sound('Sounds/barrier_explosion.ogg')
                shoot.play()
                self.barriers.remove_internal(hit)

    def create_invaders(self):
        """
        Create all needed Invaders for Environment and returns them as
        InvadersGroup
        """
        invaders = InvadersGroup(self.screen_size, self.size, self.gap)
        n = int(
            self.screen_size[0] / 100 * 75 /
            (self.size + self.gap))
        break_p = self.size + self.gap
        for i in range(n):
            invader = Invader(self.screen_size, self.size, "Objects/invader1.png",
                              i * (self.gap + self.size), break_p)
            invaders.add(invader)
        for i in range(n):
            invader = Invader(self.screen_size, self.size, "Objects/invader2.png",
                              i * (self.gap + self.size), 2 * break_p)
            invaders.add(invader)
        for i in range(n):
            invader = Invader(self.screen_size, self.size, "Objects/invader3.png",
                              i * (self.gap + self.size), 3 * break_p)
            invaders.add(invader)
        return invaders

    def create_barriers(self):
        """
        This method create barriers as pygroup
        :return: pygroup
        """
        barriers = BarrierGroup(self.screen_size, self.size, self.gap * 10)
        n = 3
        h = 260
        for i in range(n):
            barrier = Barrier(self.screen_size, self.size, "Objects/asteroid 1.png", "Objects/asteroid 2.png", "Objects/asteroid 3.png",
                              i * (self.gap + self.size), h)
            barriers.add(barrier)
        return barriers

    def invaders_shoot(self):
        """
        Preconditions: self.invaders is initialized and none empty
        Makes randomly chosen Invader to shoot
        """
        if len(self.invaders) > 0:
            a = random.randint(0, 1000)
            if a <= 70:
                x, y = self.invaders.shooter()
                bullet = Bullet(x, y + self.size, 3, 0, self.screen_size, (255, 0, 0))
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(self.enemy_bullets)


class Menu(object):

    """
    This class creates a main meany at the start.
    """

    def __init__(self) -> bool:
        self.screen_size = (800, 400)
        background = (0, 0, 0)
        self.screen = pygame.display.set_mode((self.screen_size[0], self.screen_size[1]))
        pygame.display.set_caption('Space Invaders')
        self.run = True
        self.clock = pygame.time.Clock()

        while self.run:
            self.screen.fill(background)
            TS, TR = text_objects("SPACE INVADERS: The Next Frontier", 40)
            TS1, TR1 = text_objects("Press F to Start", 15)
            TR.center = (self.screen_size[0] // 2, 100)
            TR1.center = (self.screen_size[0] // 2, self.screen_size[1] // 2 + 85)
            self.screen.blit(TS, TR)
            self.screen.blit(TS1, TR1)
            pygame.display.update()
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[K_f]:
                    self.run = False
                if event.type == pygame.QUIT:
                    sys.exit(0)


class CharacterSelect(object):

    """
    This class does character selection menu.
    """

    def __init__(self):
        self.screen_size = (800, 400)
        background = (0, 0, 0)
        self.screen = pygame.display.set_mode((self.screen_size[0], self.screen_size[1]))
        self.run = True
        self.clock = pygame.time.Clock()
        self.ship_col = 0

        while self.run:
            self.screen.fill(background)
            position = draw_menu(self.screen, 150, 55, 0)
            TS, TR = text_objects("DOUBLE CLICK to select ship color", 30)
            TR.center = (self.screen_size[0] // 2, 20)
            self.screen.blit(TS, TR)
            pygame.display.update()
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i in range(len(position)):
                        if position[i][0] <= pos[0] <= position[i][0] + 150 and position[i][1] <= pos[1] \
                                <= position[i][1] + 100:
                            self.ship_col = i
                            self.run = False
                            break
                break


def text_objects(text, size):
    """
    Function returns <textSurface> and the rect surrounding the surface.
    """
    pygame.font.init()
    BASICFONT = pygame.font.SysFont('Arial', size)
    textSurface = BASICFONT.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()


def draw_menu(screen, x, y, row):
    """Draws the necessary menu layout on the screen"""
    colors = {0: (255, 6, 80), 1: (218, 165, 32), 2: (107, 142, 35),
              3: (64, 224, 208), 4: (153, 255, 204), 5: (111, 90, 255),
              6: (169, 169, 169), 7: (240, 230, 140), 8: (255, 64, 255)}
    position = []
    while row < 3:
        color = 0
        if row is 0:
            for i in range(3):
                position.append((x, y))
                pygame.draw.rect(screen, colors[color], (x, y, 150, 100))
                x += 165
                color += 1

        elif row is 1:
            y += 115
            color = 3
            for i in range(3):
                position.append((x, y))
                pygame.draw.rect(screen, colors[color], (x, y, 150, 100))
                x += 165
                color += 1
        else:
            y += 230
            color = 6
            for i in range(3):
                position.append((x, y))
                pygame.draw.rect(screen, colors[color], (x, y, 150, 100))
                x += 165
                color += 1

        x, y, = 150, 55
        row += 1

    return position


def main():
    Menu()
    CharacterSelect()
    color = CharacterSelect().ship_col
    colors = {0: (255, 6, 80), 1: (218, 165, 32), 2: (107, 142, 35),
              3: (64, 224, 208), 4: (153, 255, 204), 5: (111, 90, 255),
              6: (169, 169, 169), 7: (240, 230, 140), 8: (255, 64, 255)}
    Environment(colors[color])


if __name__ == '__main__':
    main()
