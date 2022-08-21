"""
Imports
"""
import time
import arcade
import arcade.gui
import os
import random
import game

"""
Constantes
"""
#Tela
SCREEN_WIDTH = 832
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Donkey-Arcade-UFABC"
# Physics
class MainView(arcade.View):
    """ Class that manages the 'menu' view. """

    def on_show_view(self):
        """ Called when switching to this view"""
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.background = arcade.load_texture("assets/background.png")
        arcade.set_background_color(arcade.color.BLACK)

        # Set background color
        # arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
      

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create a text label
        ui_text_label = arcade.gui.UITextArea(text=SCREEN_TITLE,
                                              width=500,
                                              height=80,
                                              font_size=24,
                                              font_name="Kenney Future",
                                              text_color=arcade.color.WHITE)
        self.v_box.add(ui_text_label.with_space_around(bottom=0))

        text = "ESSA NÃO! Mais um quadrimestre começou e você caiu com mais um professor Cavaleiro :( "          
        ui_text_label = arcade.gui.UITextArea(text=text,
                                              width=700,
                                              height=35,
                                              font_size=12,
                                              font_name="arial")
        self.v_box.add(ui_text_label.with_space_around(bottom=0))

        text2 = "Agora é tudo ou nada. Fuja dos \"Fs\" e alcance o tão suado \"A\" "

        ui_text_label = arcade.gui.UITextArea(text=text2,
                                              width=500,
                                              height=35,
                                              font_size=12,
                                              font_name="arial")
        self.v_box.add(ui_text_label.with_space_around(bottom=0))

        text3 = "ps: fugir para chorar nas escadas sempre será uma opção ;/ "
        ui_text_label = arcade.gui.UITextArea(text=text3,
                                              width=500,
                                              height=60,
                                              font_size=12,
                                              font_name="arial")
        self.v_box.add(ui_text_label.with_space_around(bottom=0))


        default_style = {
            "font_name": ("Kenney Future", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.BUD_GREEN,

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.BLACK,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }
        quit_style = {
            "font_name": ("Kenney Future", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.UP_FOREST_GREEN,

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.BLACK,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }
        # Create a UIFlatButton
        flatbutton_onePlayer = arcade.gui.UIFlatButton(text="1 jogador Pressione ENTER", width=270, height=60, style=default_style)
        self.v_box.add(flatbutton_onePlayer.with_space_around(bottom=20))

        flatbutton_twoPlayer = arcade.gui.UIFlatButton(text="2 jogadores pressione SPACE", width=270,height=60, style=default_style)
        self.v_box.add(flatbutton_twoPlayer.with_space_around(bottom=20))

        # Handle Clicks
        @flatbutton_onePlayer.event("on_click")
        def on_click_flatbutton(event):
            game_view = game.GameView()
            # game_view.setup()
            self.window.show_view(game_view)

        @flatbutton_twoPlayer.event("on_click")
        def on_click_flatbutton(event):
            print("UIFlatButton2 pressed")

        # Create a UITextureButton
        # texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/play.png")
        # ui_texture_button = arcade.gui.UITextureButton(texture=texture)

        flatbutton_quit = arcade.gui.UIFlatButton(text="Quit", width=200, style=quit_style)
        self.v_box.add(flatbutton_quit.with_space_around(bottom=20))

        @flatbutton_quit.event("on_click")
        def on_click_flatbutton(event):
            arcade.exit()

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background, alpha=80)
        self.manager.draw()

       
    def on_key_press(self, key, modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        if key == arcade.key.ENTER:
            game_view = game.GameView()
            # game_view.setup()
            self.window.show_view(game_view)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = game.GameView()
        # game_view.setup()
        self.window.show_view(game_view)


def main():
    """ Startup """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()