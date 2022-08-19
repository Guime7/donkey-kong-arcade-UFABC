"""
Imports
"""
import time
import arcade
import os
import random

"""
Constantes
"""
# Player
TILE_SCALING = 2
PLAYER_SCALING = 0.2

#Tela
SCREEN_WIDTH = 832
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Donkey-Arcade-UFABC"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 15
GRAVITY = 1.1

class MyGame(arcade.Window):
    """Main application class."""
    def __init__(self):
        """
        Initializer
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Tilemap Object
        self.tile_map = None

        # Sprite lists
        self.player_list = None
        self.wall_list = None

        # Set up the player
        self.score = 0
        self.player_sprite = None

        self.physics_engine = None
        self.game_over = False
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None

        self.background = None

    def setup(self):
        """Set up the game and initialize the variables."""
        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png",
            PLAYER_SCALING,
        )
        # Starting position of the player
        self.player_sprite.center_x = 180
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)
   
        # Estrutura das plataformas
        map_name = "assets/map.json"
        layer_options = {
            "caminho": {"use_spatial_hash": True}
        }
        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(
            map_name, layer_options=layer_options, scaling=TILE_SCALING
        )    
        # Set wall and coin SpriteLists
        self.wall_list = self.tile_map.sprite_lists["caminho"]

        # --- Other stuff
        # Set the background color    
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        
        self.background = arcade.load_texture("assets/background.png")

        # Keep player from running through the wall_list layer
        walls = [self.wall_list, ]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls, gravity_constant=GRAVITY
        )

        self.game_over = False

    def on_draw(self):
        """
        Render the screen.
        """
        # self.camera.use()
        self.clear()

        # render background
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # Start counting frames
        self.frame_count += 1

        # Draw all the sprites.
        self.player_list.draw()
        # esconder as plataformas que dão fisica
        # self.wall_list.draw()

        # Calculate FPS if conditions are met
        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"

        # Draw FPS text
        if self.fps_message:
            arcade.draw_text(
                self.fps_message,
                10,
                40,
                arcade.color.BLACK,
                14
            )

        # Get time for every 60 frames
        if self.frame_count % 60 == 0:
            self.last_time = time.time()

        # Enable to draw hit boxes
        # self.wall_list.draw_hit_boxes()
        # self.wall_list_objects.draw_hit_boxes()

        # Get distance and draw text
        distance = self.player_sprite.right
        output = f"Distance: {distance}"
        arcade.draw_text(
            output, 10, 20, arcade.color.BLACK, 14
        )

        # Draw game over text if condition met
        if self.game_over:
            arcade.draw_text(
                "Game Over",
                200,
                200,
                arcade.color.BLACK,
                30,
            )

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        # if self.player_sprite.right >= self.end_of_map:
        #     self.game_over = True

        # # Call update on all sprites
        # if not self.game_over:
        #     self.physics_engine.update()
        self.physics_engine.update()

        # coins_hit = arcade.check_for_collision_with_list(
        #     self.player_sprite, self.coin_list
        # )
        # for coin in coins_hit:
        #     coin.remove_from_sprite_lists()
        #     self.score += 1

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()