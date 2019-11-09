import random
import sys
from pygame import *
import pygame


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

    def __init__(self, screen_size, size):
        """
        Inits Player class with given attributes
        """
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
        self.health = 10

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
            if 0 <= self.x - 5 <= self.screen_size[0]:
                self.move(-5, 0)
        if pressed_key[pygame.K_RIGHT]:
            if 0 <= self.x + 5 <= self.screen_size[0]:
                self.move(5, 0)


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

    def __init__(self, x, y, speedy, speedx, screen_size):
        """
        Inits Bullet class with given attributes
        """
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
        """
        Overrides and calls the update method for this specific sprite
        """
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

    def move(self, x, y):
        """
        Moves Invader by given x and y
        """
        if 0 <= self.x + x <= self.screen_size[0] and 0 <= self.y + y <= \
                self.screen_size[1]:
            self.x += x
            self.y += y
            self.rect = self.rect.move((x, y))


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

    def move(self, x, y):
        """
        Moves each member of InvadersGroup by given x and y
        """
        for invader in self.invaders:
            invader.move(x, y)

    def update(self):
        """
        Calls the update method of every member sprite
        Group.update(*args): return None

        Calls the update method of every member sprite. All arguments that
        were passed to this method are passed to the Sprite update function.
        """
        if len(self.invaders) == 0:
            print("U WON!!!")
            sys.exit()
        if self.de_way == "L":
            self.move(-1, 0)
            if self.invaders[0].x - self.invaders[-1].size <= 0:
                self.de_way = "R"
        if self.de_way == "R":
            self.move(1, 0)
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

    def shoot(self):
        """
        Chooses random member of InvadersGroup and return its coordinates
        """
        a = random.choice(self.invaders)
        return a.x, a.y


class Environment(object):
    """
    Documentation needed ###TO-DO
    """
    def __init__(self):
        """
        Inits Environment class
        """
        init()

        background = (0, 0, 0)

        self.screen_size = (800, 400)
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
        """
        This method check for keyboard interaction which influences
        only Environment
        """
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
        """
        Checks the collision for all objects in the Environment and proceeds
        with specific instructions
        """
        hits = pygame.sprite.groupcollide(self.invaders, self.bullets, False, True)
        for hit in hits:
            hit.health = hit.health - 1
            if hit.health <= 0:
                self.invaders.remove_internal(hit)
        pygame.sprite.groupcollide(self.enemy_bullets, self.bullets, True, True)
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            print("You have", self.player.health, "hp")
            self.player.health = self.player.health - 1
            if self.player.health <= 0:
                self.play = False

    def create_invaders(self):
        """
        Create all needed Invaders for Environment and adds them to
        InvadersGroup
        """
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
        """
        Makes randomly chosen Invader to shoot
        """
        a = random.randint(0, 1000)
        if a <= 50:
            x, y = self.invaders.shoot()
            bullet = Bullet(x, y + self.size, 3, 0, self.screen_size)
            self.enemy_bullets.add(bullet)
            self.all_sprites.add(self.enemy_bullets)


if __name__ == '__main__':
    Environment()
