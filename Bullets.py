import pygame
import random
from Asteroids import Ast

bullet = pygame.image.load("bullet.jpg")
colorkey = bullet.get_at((0, 0))
bullet.set_colorkey(colorkey)
sprite_list = pygame.sprite.Group()
razbit = 0


class Bullet(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet
        self.scale = 15
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.xvel = 0
        self.yvel = -10

    def update(self):
        global razbit
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        if self.rect.y <= 0:
            self.kill()
        for s in sprite_list:
            if s.rect.height >= 75 and s.rect.height < 88:
                if self.rect.colliderect(s.rect):
                    self.kill()
                    razbit += 1
                    sprite_list.add(
                        Ast(s.rect.center, s.rect.height // 2, random.randrange(5, 8), random.randrange(5, 8)))
                    sprite_list.add(
                        Ast(s.rect.center, s.rect.height // 2, random.randrange(5, 8) * -1, random.randrange(5, 8)))
                    sprite_list.remove(s)
                    pass

            if s.rect.height >= 88 and s.rect.height <= 99:
                if self.rect.colliderect(s.rect):
                    self.kill()
                    razbit += 1
                    sprite_list.add(
                        Ast(s.rect.center, s.rect.height // 3, random.randrange(5, 8), random.randrange(5, 8)))
                    sprite_list.add(
                        Ast(s.rect.center, s.rect.height // 3, random.randrange(5, 8) * -1, random.randrange(5, 8)))
                    sprite_list.add(Ast(s.rect.center, s.rect.height // 3, 0, random.randrange(5, 8)))
                    sprite_list.remove(s)
                    pass

            if s.rect.height >= 99:
                if self.rect.colliderect(s.rect):
                    self.kill()
                    razbit += 1
                    sprite_list.add(
                        Ast(s.rect.center, s.rect.height // 4, random.randrange(5, 8), random.randrange(5, 8)))
                    sprite_list.add(
                        Ast(s.rect.center, s.rect.height // 4, random.randrange(5, 8) * -1, random.randrange(5, 8)))
                    sprite_list.add(Ast(s.rect.center, s.rect.height // 4, 0, random.randrange(5, 8)))
                    sprite_list.add(
                        Ast(s.rect.center, s.rect.height // 4, random.randrange(2, 4), random.randrange(5, 8)))
                    sprite_list.remove(s)
                    pass

            if s.rect.height < 75:
                if self.rect.colliderect(s.rect):
                    self.kill()
                    sprite_list.remove(s)
                    razbit += 1
                    pass


def razbito():
    return razbit
