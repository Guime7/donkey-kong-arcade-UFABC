"""
Imports
"""
import time
import arcade
import os
import random
from game import *
from main import *

"""
Constantes
"""
# Physics
class GameOverView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
    """ Class to manage the game over view """
    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the game over view """
        self.clear()
        arcade.draw_text("Game Over - press ESCAPE to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, 30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """ If user hits escape, go back to the main menu view """
        if key == arcade.key.ESCAPE:
            menu_view = MainView()
            self.window.show_view(menu_view)
        
class GameWinView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
    """ Class to manage the game over view """
    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.GREEN)

    def on_draw(self):
        """ Draw the game over view """
        self.clear()
        arcade.draw_text("Você Ganhou um Azão - press ESCAPE to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, 30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """ If user hits escape, go back to the main menu view """
        if key == arcade.key.ESCAPE:
            menu_view = MainView()
            self.window.show_view(menu_view)