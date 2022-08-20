"""
Imports
"""
import time
import arcade
import os
import random
from gameOverScreen import *

"""
Constantes
"""
# Player
TILE_SCALING = 2
PLAYER_SCALING = 1

#Tela
SCREEN_WIDTH = 832
SCREEN_HEIGHT = 640
# SCREEN_TITLE = "Donkey-Arcade-UFABC"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

SPRITE_SCALING_ENEMY = 0.2
SPRITE_NATIVE_SIZE = 64
SPRITE_SIZE_ENEMY = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING_ENEMY)

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 15
GRAVITY = 1.1

class GameView(arcade.View):
    """Main application class."""
    def __init__(self):
        """
        Initializer
        """
        super().__init__()
        # super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Tilemap Object
        self.tile_map = None

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.enemy_list = None
        self.physics_engine_enemy_list = None

        # Set up the player
        self.score = 0
        self.player_sprite = None
        self.enemy_sprite = None
        self.view_left = 0
        self.view_bottom = 0

        self.physics_engine = None
        self.physics_engine_enemy = None
        self.game_over = False
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None

        self.background = None

        self.walls = None

    def setup(self):
        """Set up the game and initialize the variables."""
        self.game_over = False

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.physics_engine_enemy_list = []
        # Set up the player
        self.player_sprite = arcade.Sprite(
            "assets/playerFixo.png",
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

        # -- Draw an enemy on the ground
        # self.enemy_sprite = arcade.AnimatedTimeBasedSprite()
        # self.enemy_sprite.textures = []

        # for i in range(7):
        # self.enemy_sprite.textures.append(arcade.load_texture("assets/barril.png", x=0,y=0,width=28,height=20))
        # self.enemy_sprite = arcade.Sprite(
        #     "assets/barrilFixo.png",
        #     PLAYER_SCALING,
        # )
        
      
         # Keep player from running through the wall_list layer
        self.walls = [self.wall_list]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.walls, gravity_constant=GRAVITY
        )

       
   

    def on_draw(self):
        """
        Render the screen.
        """
        # self.camera.use()
        self.clear()
        arcade.start_render()
        # render background
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # Start counting frames
        self.frame_count += 1

        # Draw all the sprites.
        self.player_list.draw()
        self.enemy_list.draw()
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

        # Draw game over text if condition met
        if self.game_over:
            arcade.draw_text(
                "Game Over",
                SCREEN_WIDTH/2,
                SCREEN_HEIGHT/2,
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


        if key == arcade.key.SPACE and len(self.enemy_list) < 6:          
            self.enemy_sprite = arcade.Sprite("assets/barrilFixo.png", 1.5)

            self.enemy_sprite.center_x = 180
            self.enemy_sprite.center_y = 500

            # Set enemy initial speed
            self.enemy_sprite.change_x = 5
            # Set boundaries on the left/right the enemy can't cross
            self.enemy_sprite.boundary_right = 680
            self.enemy_sprite.boundary_left = 140  
            self.enemy_sprite.boundary_bottom = -350
            self.physics_engine_enemy = arcade.PhysicsEnginePlatformer(
                self.enemy_sprite, self.walls, gravity_constant=GRAVITY
            )
            
            self.physics_engine_enemy_list.append(self.physics_engine_enemy)
            self.enemy_list.append(self.enemy_sprite)
           

    def gameOver(self):
        """ Use a mouse press to advance to the 'game' view. """
        game_over_view = GameOverView(self)
        self.window.show_view(game_over_view)

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


    def on_update(self, delta_time):
        """Movement and game logic"""

        # Loop through each bullet
        if not self.game_over:
            # Check each enemy
            for enemy in self.enemy_list:
                # If the enemy hit a wall, reverse
                # if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                #     enemy.change_x *= -1
                # If the enemy hit the left boundary, reverse
                if enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                    enemy.change_x *= -1
                # If the enemy hit the right boundary, reverse
                elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1

                # Check this bullet to see if it hit a coin
                hit_list = arcade.check_for_collision_with_list(enemy, self.player_list)

                # If it did, get rid of the bullet
                if len(hit_list) > 0:
                    enemy.remove_from_sprite_lists()
                    self.game_over = True


                # For every coin we hit, add to the score and remove the coin
                # for barril in hit_list:
                #     enemy.remove_from_sprite_lists()
                    # self.score += 1

                    # Hit Sound
                    # arcade.play_sound(self.hit_sound)

                # If the bullet flies off-screen, remove it.
                if enemy.bottom < enemy.boundary_bottom:
                    enemy.remove_from_sprite_lists()


            # if self.player_sprite.right >= self.end_of_map:
            #     self.game_over = True

            # # Call update on all sprites
            # if not self.game_over:
            self.physics_engine.update()
            for i in self.physics_engine_enemy_list:
                i.update()

            # coins_hit = arcade.check_for_collision_with_list(
            #     self.player_sprite, self.coin_list
            # )
            # for coin in coins_hit:
            #     coin.remove_from_sprite_lists()
            #     self.score += 1
        else:
            self.gameOver()
            
# def main():
#     window = MyGame()
#     window.setup()
#     arcade.run()


# if __name__ == "__main__":
#     main()