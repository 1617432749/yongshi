import pygame, os
from . import consatants as C
from . import tools

pygame.init()
SCREEN = pygame.display.set_mode((C.SCREEN_W, C.SCREEN_H))

GRAPHICS = tools.load_graphics('resources/graphics')
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX = tools.load_all_sfx(os.path.join("resources", "sound"))