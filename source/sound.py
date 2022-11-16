import pygame
from . import consatants as C
from . import setup

class Sound(object):
    def __init__(self, overhead_info):
        self.sfx_dict = setup.SFX
        self.music_dict = setup.MUSIC
        self.overhead_info = overhead_info
        self.game_info = overhead_info.game_info
        self.set_music_mixer()

    def set_music_mixer(self):
        if self.overhead_info.state == C.LEVEL:
            pygame.mixer.music.load(self.music_dict['main_theme'])
            pygame.mixer.music.play()
            self.state = C.NORMAL
        elif self.overhead_info.state == C.LAST:
            pygame.mixer.music.load(self.music_dict['game_over'])
            pygame.mixer.music.play()
            self.state = C.NORMAL
        elif self.overhead_info.state == C.GAME_OVER:
            pygame.mixer.music.load(self.music_dict['game_over'])
            pygame.mixer.music.play()
            self.state = C.GAME_OVER

    def update(self, game_info, mario):
        self.game_info = game_info
        self.mario = mario
        self.handle_state()

    def  handle_state(self):
        """Handles the state of the soundn objeCt"""
        if self.state == C.NORMAL:
            if self.mario.dead:
                self.play_music('death', C.MARIO_DEAD)


    def play_music(self, key, state):
        """Plays new music"""
        pygame.mixer.music.load(self.music_dict[key])
        pygame.mixer.music.play()
        self.state = state



    def stop_music(self):
        """Stops playback"""
        pygame.mixer.music.stop()