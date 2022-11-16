import pygame

from source import tools, setup
from source.states import main_menu, load_screen, level, juqing, last, juqing2, juqing3, xuanze, jieju1, jieju2, gushijieshu
from source import consatants as C

def main():
    state_dict = {
        C.MAIN_MENU:main_menu.MainMenu(),
        C.LOAD_SCREEN:load_screen.LoadScreen(),
        C.LEVEL:level.Level(),
        C.GAME_OVER: load_screen.GameOver(),
        'juqing': juqing.Juqing(),
        'juqing2': juqing2.Juqing(),
        'juqing3': juqing3.Juqing(),
        C.LAST:last.Last(),
        C.XUANZE:xuanze.Xuanze(),
        'jieju1': jieju1.Jieju1(),
        'jieju2': jieju2.Jieju2(),
        'jieshu':gushijieshu.Jieshu()
    }
    game = tools.Game(state_dict, C.MAIN_MENU)
    game.run()


if __name__ == '__main__':
    main()