import pygame
from .. import consatants as C
from . import coin
from .. import setup, tools
pygame.font.init()


class Info:
    def __init__(self, state, game_info):
        self.state = state
        self.game_info = game_info
        self.create_state_labels()
        self.create_info_labels()

    def create_state_labels(self):
        self.state_labels = []
        if self.state == C.MAIN_MENU:
            self.state_labels.append((self.create_label('故事开始'), (272, 360)))
        elif self.state == C.LOAD_SCREEN:
            self.state_labels.append((self.create_label('X    {}'.format(self.game_info['lives'])), (380, 280)))
            self.player_image = tools.get_image(setup.GRAPHICS['mario_bros'],157, 58, 62, 61, (0, 0, 0), 1)
        elif self.state == C.GAME_OVER:
            self.state_labels.append((self.create_label('GAME OVER'), (300, 300)))
        elif self.state == C.XUANZE:
            self.state_labels.append((self.create_label('打开宝库'), (272, 160)))
            self.state_labels.append((self.create_label('离开'), (272, 300)))
        elif self.state == 'jieshu':
            self.state_labels.append((self.create_label('故事结束'), (290, 250)))


    def create_info_labels(self):
        self.info_labels = []

    def create_label(self, label, size=40, width_scale=1.25, height_scale=1):
        font = pygame.font.SysFont(C.FONT, size)
        label_image = font.render(label, 1, (255, 255, 255))
        rect = label_image.get_rect()
        label_image = pygame.transform.scale(label_image, (int(rect.width*width_scale),
                                                           int(rect.height*height_scale)))
        return label_image

    def draw(self, suface):
         for lable in self.state_labels:
             suface.blit(lable[0], lable[1])
         if self.state != 'juqing':
             for lable_l in self.info_labels:
                suface.blit(lable_l[0], lable_l[1])
         if self.state == C.LOAD_SCREEN:
             suface.blit(self.player_image, (300, 250))
             pygame.display.update()