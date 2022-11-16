import pygame
from .. import setup
from .. import tools
from .. import consatants as C
from .. commponents import info

class Jieshu:
    def start(self, game_info):
        self.game_info = game_info
        self.info = info.Info('jieshu', self.game_info)
        self.finished = False
        self.next = C.MAIN_MENU
        self.timer = 0
        self.dector = 3000


    def update_cursor(self, keys):
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.dector:
            self.finished = True
            self.timer = 0

    def update(self, surface, keys):
        self.update_cursor(keys)
        surface.fill((0,0,0))
        self.info.draw(surface)