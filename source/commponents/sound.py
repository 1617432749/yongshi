import pygame
from .. import setup
from .. import consatants as c

class Sound(object):
    """Handles all sound for the game"""
    def __init__(self, overhead_info):
        """Initialize the class"""
        self.sfx_dict = setup.SFX
        self.music_dict = setup.MUSIC
        self.overhead_info = overhead_info
        self.game_info = overhead_info.game_info
        self.set_music_mixer()



    def set_music_mixer(self):
        """Sets music for level"""
        if self.overhead_info.state == c.LEVEL:
            pygame.mixer.music.load(self.music_dict['main_theme'])
            pygame.mixer.music.play()
            self.state = c.NORMAL
        elif self.overhead_info.state == c.GAME_OVER:
            pygame.mixer.music.load(self.music_dict['game_over'])
            pygame.mixer.music.play()
            self.state = c.GAME_OVER


    def update(self, game_info, player):
        """Updates sound object with game info"""
        self.game_info = game_info
        self.mario = player
        self.handle_state()

    def  handle_state(self):
        """Handles the state of the soundn object"""
        if self.state == c.NORMAL:
            if self.mario.dead:
                self.play_music('death', c.MARIO_DEAD)



    def play_music(self, key, state):
        """Plays new music"""
        pygame.mixer.music.load(self.music_dict[key])
        pygame.mixer.music.play()
        self.state = state

    def stop_music(self):
        """Stops playback"""
        pygame.mixer.music.stop()



