from ..commponents import info
import pygame
from ..import consatants as C
from ..import sound

class LoadScreen:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = C.LEVEL
        self.duration = 2000
        self.timer = 0
        self.info = info.Info(C.LOAD_SCREEN, self.game_info)

        info_state = self.set_overhead_info_state()

        self.overhead_info = info.Info(info_state, self.game_info)
        self.sound_manager = sound.Sound(self.overhead_info)

    def set_overhead_info_state(self):
        return C.LOAD_SCREEN

    def update(self, surface, keys):
        self.draw(surface)
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.duration:
            self.finished = True
            self.timer = 0


    def draw(self,surface):
        surface.fill((0, 0, 0))
        self.info.draw(surface)

class GameOver(LoadScreen):
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = C.MAIN_MENU
        self.duration = 4000
        self.timer = 0
        self.info = info.Info(C.GAME_OVER, self.game_info)

        info_state = self.set_overhead_info_state()
        self.overhead_info = info.Info(info_state, self.game_info)
        self.sound_manager = sound.Sound(self.overhead_info)

    def set_overhead_info_state(self):
        return C.GAME_OVER