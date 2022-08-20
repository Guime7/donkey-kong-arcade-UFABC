"""
Imports
"""
import time
import arcade
import os
import random
import game

"""
Constantes
"""
# Player
TILE_SCALING = 2
PLAYER_SCALING = 1

#Tela
SCREEN_WIDTH = 832
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Donkey-Arcade-UFABC"
# Physics
class MainView(arcade.View):
    """ Class that manages the 'menu' view. """

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """ Draw the menu """
        self.clear()
        arcade.draw_text("Menu Screen - click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        game_view = game.GameView()
        game_view.setup()
        self.window.show_view(game_view)

def main():
    """ Startup """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()