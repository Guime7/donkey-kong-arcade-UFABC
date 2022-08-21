"""
Imports
"""
import time
import arcade
import os
import random
from game import *
from main import *
import datetime

"""
Constantes
"""
# Physics
class GameOverView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.backMenuTimer = 0
        self.game_view = game_view
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite(
            "assets/playerFixo.png", 4,
        )
        # Starting position of the player
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = 350
        self.player_list.append(self.player_sprite)
    """ Class to manage the game over view """
    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the game over view """
        self.clear()
        arcade.draw_text("Game Over", SCREEN_WIDTH / 2,430,
                         arcade.color.WHITE, 30, anchor_x="center")

        arcade.draw_text("Bobeu dançou, um F você tirou ;/", SCREEN_WIDTH / 2, 250,
                         arcade.color.WHITE, 15, anchor_x="center")
        self.player_list.draw()

        arcade.draw_text("Pressione ENTER para tentar denovo.", SCREEN_WIDTH / 2, 150,
                         arcade.color.WHITE, 16, anchor_x="center")
        arcade.draw_text("Pressione ESC para voltar ao menu.", SCREEN_WIDTH / 2, 120,
                         arcade.color.WHITE, 16, anchor_x="center")
        self.player_list.draw()

    
        

    def on_key_press(self, key, modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        if key == arcade.key.ENTER:
            game_view = game.GameView()
            # game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
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