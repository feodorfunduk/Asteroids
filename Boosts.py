import pygame


class boost(pygame.sprite.Sprite):
    def __init__(self, image, pos, xvel, yvel):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.scale = 25
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.xvel = xvel
        self.yvel = yvel

    def update(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel
