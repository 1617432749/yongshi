import pygame
from .. import setup
from .. import tools
from .. import consatants as C
from .. commponents import info


class Xuanze:
    def start(self, game_info):
        self.game_info = game_info
        self.setup_cursor()
        self.info = info.Info(C.XUANZE, self.game_info)
        self.finished = False


    def setup_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = tools.get_image(setup.GRAPHICS['item_objects'], 24, 160, 8, 8, (0, 0, 0), C.PLAYER_MULTI)
        rect = self.cursor.image.get_rect()
        rect.x, rect.y = (180, 160)
        self.cursor.rect = rect
        self.cursor.state = '打开宝库'

    def update_cursor(self, keys):
        if keys[pygame.K_UP]:
            self.cursor.state = '打开宝库'
            self.cursor.rect.y = 160
        elif keys[pygame.K_DOWN]:
            self.cursor.state = '离开'
            self.cursor.rect.y = 300
        elif keys[pygame.K_RETURN]:
            if self.cursor.state == '打开宝库':
                self.finished = True
                self.next = 'jieju1'
            elif self.cursor.state == '离开':
                self.finished = True
                self.next = 'jieju2'

    def update(self, surface, keys):
        self.update_cursor(keys)
        surface.fill((0, 0, 0))
        surface.blit(self.cursor.image, self.cursor.rect)

        self.info.draw(surface)
