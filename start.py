"""
Imports
"""

import arcade
import arcade.gui
from src.main import *
"""
Constantes
"""
#Tela
SCREEN_WIDTH = 832
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Donkey-Arcade-UFABC"

def main():
    """ Startup """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()