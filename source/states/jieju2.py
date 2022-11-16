import pygame
from .. import setup
from .. import tools
from .. import consatants as C
from .. commponents import info

class Jieju2:
    def start(self, game_info):
        self.game_info = game_info
        self.setup_background()
        self.info = info.Info('jieju2', self.game_info)
        self.finished = False
        self.next = 'jieshu'
        self.timer = 0
        self.dector = 3000

    def setup_background(self):
        self.background = setup.GRAPHICS['结局2']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 2.1),
                                                                   int(self.background_rect.height * 2.8)))
        self.viewport = setup.SCREEN.get_rect()

    def update_cursor(self, keys):
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.dector:
            self.finished = True
            self.timer = 0

    def update(self, surface, keys):
        self.update_cursor(keys)
        surface.blit(self.background, self.viewport)


        self.info.draw(surface)