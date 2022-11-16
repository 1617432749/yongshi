import pygame

from source import tools, setup
from source.states import main_menu, load_screen, level, juqing, last
from source import consatants as C


def main():
    state_dict = {
        C.LAST: last.Last()
    }
    game = tools.Game(state_dict, C.LAST)
    game.run()


if __name__ == '__main__':
    main()