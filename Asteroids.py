import pygame

ochi = 0
asteroids = pygame.image.load("aster2.jpg")
colorkey = asteroids.get_at((0, 0))
asteroids.set_colorkey(colorkey)
scr = pygame.display.set_mode()
W, H = scr.get_width(), scr.get_height()


class Ast(pygame.sprite.Sprite):

    def __init__(self, pos, scale, xvel, yvel):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroids
        self.scale = scale
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.xvel = xvel
        self.yvel = yvel

    def update(self):
        global ochi
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        if self.rect.y >= H:
            ochi += 1
            self.kill()


def och():
    return ochi
