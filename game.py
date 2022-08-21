"""
Imports
"""
import time
import arcade
from gameOver import *

"""
Constantes
"""
# Player
TILE_SCALING = 2

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 13.5
GRAVITY = 1

class GameView(arcade.View):
    """Main application class."""
    def __init__(self):
        """
        Initializer
        """
        super().__init__()

        # Tilemap Object
        self.tile_map = None
        self.walls = None
        self.wall_list = None
        self.escada = None
        self.escada_list = None

        # Sprite lists
        self.player_list = None
        self.enemy_list = None
        self.cavaleiro_list = None
        self.vitoria_list = None

        # Physics lists
        self.physics_engine_enemy_list = None
        self.physics_engine_enemy = None
        self.physics_engine = None
        self.physics_engine_vitoria = None

        # Set up the player
        self.player_sprite = None
        self.cavaleiro_sprite = None
        self.enemy_sprite = None
        self.vitoria_sprite = None


        self.score = 0
        self.game_over = False
        self.game_win = False
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None

        self.background = None

    def setup(self):
        """Set up the game and initialize the variables."""
        self.game_over = False

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.vitoria_list = arcade.SpriteList()
        self.cavaleiro_list = arcade.SpriteList()
        self.physics_engine_enemy_list = []

        # Set up the player
        self.player_sprite = arcade.Sprite(
            "assets/playerFixo.png", 0.9,
        )
        # Starting position of the player
        self.player_sprite.center_x = 180
        self.player_sprite.center_y = 50
        self.player_sprite.boundary_bottom = -550
        self.player_list.append(self.player_sprite)
   
        # Set up the cavaleiro
        self.cavaleiro_sprite = arcade.Sprite(
            "assets/cavaleiroFixo.png", 1,
        )

        # Starting position of the player
        self.cavaleiro_sprite.center_x = 180
        self.cavaleiro_sprite.center_y = 485
        self.cavaleiro_list.append(self.cavaleiro_sprite)

         # Set up the vitoria
        self.vitoria_sprite = arcade.Sprite(
            "assets/barrilAVitoria.png", 1.5,
        )

        # Starting position of the player
        self.vitoria_sprite.center_x = 375
        self.vitoria_sprite.center_y = 600
        self.vitoria_list.append(self.vitoria_sprite)
        

        # Estrutura das plataformas
        map_name = "assets/map.json"
        layer_options = {
            "caminho": {"use_spatial_hash": True},
            "escada": {"use_spatial_hash": True}
        }
        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(
            map_name, layer_options=layer_options, scaling=TILE_SCALING
        )    
        # Set wall and coin SpriteLists
        self.wall_list = self.tile_map.sprite_lists["caminho"]
        self.escada_list = self.tile_map.sprite_lists["escada"]

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
        self.escada = [self.escada_list]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.walls, gravity_constant=GRAVITY,
            ladders= self.escada,
        )

        self.physics_engine_vitoria = arcade.PhysicsEnginePlatformer(
            self.vitoria_sprite, self.walls, gravity_constant=GRAVITY,           
        )
        

    def on_draw(self):
        """
        Render the screen.
        """
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
        self.cavaleiro_list.draw()
        self.vitoria_list.draw()
        # esconder as plataformas que dão fisica
        # self.wall_list.draw()
        # self.escada_list.draw()

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

        # Draw game over text if condition met
        # if self.game_over:
        #     arcade.draw_text(
        #         "Game Over",
        #         SCREEN_WIDTH/2,
        #         SCREEN_HEIGHT/2,
        #         arcade.color.BLACK,
        #         30,
        #     )

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        # if key == arcade.key.UP:
        #     if self.physics_engine.can_jump():
        #         self.player_sprite.change_y = JUMP_SPEED
        if key == arcade.key.UP:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = MOVEMENT_SPEED
            elif self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
                # arcade.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED


        # gerar ininigo
        if key == arcade.key.SPACE and len(self.enemy_list) < 6:          
            self.enemy_sprite = arcade.Sprite("assets/barrilFixo.png", 1.5)

            self.enemy_sprite.center_x = 180
            self.enemy_sprite.center_y = 510

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

    def gameWin(self):
        """ Use a mouse press to advance to the 'game' view. """
        game_win_view = GameWinView(self)
        self.window.show_view(game_win_view)

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.UP:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


    def on_update(self, delta_time):
        """Movement and game logic"""

        # Loop through each bullet
        if not self.game_over and not self.game_win:

            # Generate a list of all sprites that collided with the player.
            hit_list_vitoria = arcade.check_for_collision_with_list(self.player_sprite, self.vitoria_list)

            # Loop through each colliding sprite, remove it, and add to the score.
            for win in hit_list_vitoria:
                self.game_win = True


            if self.player_sprite.bottom < self.player_sprite.boundary_bottom:
                self.game_over = True
            # Check each enemy
            for enemy in self.enemy_list:
                # If the enemy hit a wall, reverse
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

                # If the bullet flies off-screen, remove it.
                if enemy.bottom < enemy.boundary_bottom:
                    enemy.remove_from_sprite_lists()

            self.physics_engine.update()
            self.physics_engine_vitoria.update()
            for i in self.physics_engine_enemy_list:
                i.update()

        # em caso de gameOver        
        elif self.game_win:
            self.gameWin()

        else:
            self.gameOver()
