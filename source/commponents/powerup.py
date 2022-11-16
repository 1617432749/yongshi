import pygame
from .. import setup, tools
from .. import consatants as C

def create_powerup(centerx, centery, type):
    return Mushroom(centerx, centery)

class Powerup(pygame.sprite.Sprite):
    def __init__(self, centerx, centery, frame_rects):
        pygame.sprite.Sprite.__init__(self)

        self.frames = []
        self.frame_index = 0
        for frame_rects in frame_rects:
            self.frames.append(tools.get_image(setup.GRAPHICS['item_objects'], *frame_rects, (0, 0, 0), 2.5))
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.origin_y = centery - self.rect.height/2

        self.direction = 1
        self.gravity = 1

    def update_position(self, level):
        self.check_x_collisions(level)
        self.check_y_collisions(level)

    def check_x_collisions(self, level):
        sprite = pygame.sprite.spritecollideany(self, level.ground_items_group)
        if sprite:
            if self.direction:
                self.direction = 0
                self.rect.right = sprite.rect.left
            else:
                self.direction = 1
                self.rect.left = sprite.rect.right


    def check_y_collisions(self, level):
        check_group = pygame.sprite.Group(level.ground_items_group, level.box_group, level.brick_group)
        sprite = pygame.sprite.spritecollideany(self, check_group)
        if sprite:
            if self.rect.top < sprite.rect.top:
                self.rect.bottom = sprite.rect.top
                self.state = 'walk'

        level.check_will_fall(self)

class Mushroom(Powerup):
    def __init__(self, centerx, centery):
        Powerup.__init__(self, centerx, centery, [(0, 0, 16, 16)])
        self.x_vel = 2
        self.state = 'grow'
        self.name = 'mushroom'

