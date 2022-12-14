"""Imports"""
import arcade
import arcade.gui
import src.game as game

"""Constantes"""
SCREEN_WIDTH = 832
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Donkey-Arcade-UFABC"

class MainView(arcade.View):
    """ Class that manages the 'menu' view. """

    def on_show_view(self):
        """ Called when switching to this view"""

        #interface
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.background = arcade.load_texture("assets/images/background.png")
        arcade.set_background_color(arcade.color.BLACK)

        #musica
        self.songs = "assets/sounds/intro.mp3"
        self.my_music = arcade.load_sound(self.songs)
        self.media_player = self.my_music.play()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        #titulo
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

        #botaao
        default_style = {
            "font_name": ("Kenney Future", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.BUD_GREEN,
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
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.BLACK,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }

        # botao de incio
        flatbutton_onePlayer = arcade.gui.UIFlatButton(text="Trabalho em grupo :(", width=270, height=60, style=default_style)
        self.v_box.add(flatbutton_onePlayer.with_space_around(bottom=20))
        @flatbutton_onePlayer.event("on_click")
        def on_click_flatbutton(event):
            game_view = game.GameView()
            self.window.show_view(game_view)
            self.media_player.pause()

        #botao de sair
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

       
    #para iniciar o jogo ao clicar na tela
    def on_key_press(self, key, modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        if key == arcade.key.ENTER:
            game_view = game.GameView()
            # game_view.setup()
            self.window.show_view(game_view)
            self.media_player.pause()