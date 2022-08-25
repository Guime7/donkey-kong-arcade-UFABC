"""Imports"""
import time
import arcade
import random
import src.barril as barril
import src.player as player
import src.main as main
import src.gameOver as gameOver

"""Constantes"""
# Player
TILE_SCALING = 2

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 13.5
GRAVITY = 1

class GameView(arcade.View):
    """Construtor"""
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
        self.player_list2 = None
        self.enemy_list = None
        self.cavaleiro_list = None
        self.vitoria_list = None

        # Physics lists
        self.physics_engine_enemy_list = None
        self.physics_engine_enemy = None
        self.physics_engine = None
        self.physics_engine2 = None
        self.physics_engine_vitoria = None

        # Sprites
        self.player_sprite = None
        self.player_sprite2 = None
        self.cavaleiro_sprite = None
        self.enemy_sprite = None
        self.vitoria_sprite = None

        #Configs
        self.game_over = False
        self.game_win = False
   
        #background
        self.background = None

        # Sons
        self.jump_sound = arcade.load_sound(":resources:sounds/jump3.wav")

        # chamar setup
        self.setup()

    """Configuraçõs iniciais gerais"""
    def setup(self):
        """Set up the game and initialize the variables."""
        self.game_over = False

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.player_list2 = arcade.SpriteList()
    
        # Player sprite
        self.player_sprite = player.PlayerCharacter()
        self.player_sprite2 = player.PlayerCharacter()

        # Starting position of the player1
        self.player_sprite.center_x = 180
        self.player_sprite.center_y = 50
        self.player_sprite.boundary_bottom = -550
        self.player_list.append(self.player_sprite)

        # Starting position of the player2
        self.player_sprite2.center_x = 170
        self.player_sprite2.center_y = 50
        self.player_sprite2.boundary_bottom = -550
        self.player_list2.append(self.player_sprite2)
   
        # Set up the barril
        self.enemy_list = arcade.SpriteList()
        self.physics_engine_enemy_list = []

        # Set up the cavaleiro
        self.cavaleiro_list = arcade.SpriteList()
        self.cavaleiro_sprite = arcade.Sprite(
            "assets/images/cavaleiro_3.png", 1.2,
        )

        # Starting position of the cavaleiro
        self.cavaleiro_sprite.center_x = 180
        self.cavaleiro_sprite.center_y = 490
        self.cavaleiro_list.append(self.cavaleiro_sprite)

         # Set up the vitoria
        self.vitoria_list = arcade.SpriteList()
        self.vitoria_sprite = arcade.Sprite(
            "assets/images/barrilAVitoria.png", 1.5,
        )
        # Starting position of the vitoria
        self.vitoria_sprite.center_x = 375
        self.vitoria_sprite.center_y = 600
        self.vitoria_list.append(self.vitoria_sprite)
        
        # Estrutura das plataformas
        map_name = "assets/map/map.json"
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

        # Set the background color    
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color) 
        self.background = arcade.load_texture("assets/images/background.png")     
      
        #Set up fisica de objetos
        self.walls = [self.wall_list]
        self.escada = [self.escada_list]

        #fisica player 1
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.walls, gravity_constant=GRAVITY,
            ladders= self.escada,
        )
        #fisica player 2
        self.physics_engine2 = arcade.PhysicsEnginePlatformer(
            self.player_sprite2, self.walls, gravity_constant=GRAVITY,
            ladders= self.escada,
        )

        #fisica vitoria
        self.physics_engine_vitoria = arcade.PhysicsEnginePlatformer(
            self.vitoria_sprite, self.walls, gravity_constant=GRAVITY,           
        )
        
    """Render the screen."""
    def on_draw(self):
        
        self.clear()
        arcade.start_render()
        # render background
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            main.SCREEN_WIDTH, main.SCREEN_HEIGHT,
                                            self.background)

        # esconder as plataformas que dão fisica
        # self.wall_list.draw()
        # self.escada_list.draw()

        # Draw all the sprites.
        self.player_list.draw()
        self.player_list2.draw()
        self.enemy_list.draw()
        self.cavaleiro_list.draw()
        self.vitoria_list.draw()

    """Called whenever a key is pressed."""
    def on_key_press(self, key, modifiers):
       
       #controle do player 1
        if key == arcade.key.UP:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = MOVEMENT_SPEED
            elif self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
                arcade.play_sound(self.jump_sound)

        elif key == arcade.key.DOWN:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -MOVEMENT_SPEED

        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

        #controle do player 2
        if key == arcade.key.W:
            if self.physics_engine2.is_on_ladder():
                self.player_sprite2.change_y = MOVEMENT_SPEED
            elif self.physics_engine2.can_jump():
                self.player_sprite2.change_y = JUMP_SPEED
                arcade.play_sound(self.jump_sound)
      
        elif key == arcade.key.S:
            if self.physics_engine2.is_on_ladder():
                self.player_sprite2.change_y = -MOVEMENT_SPEED

        elif key == arcade.key.A:
            self.player_sprite2.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.D:
            self.player_sprite2.change_x = MOVEMENT_SPEED
        
    """Called when the user presses a mouse button."""
    def on_key_release(self, key, modifiers):

        #controle player 1
        if key == arcade.key.UP:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0

        elif key == arcade.key.DOWN:
            if self.physics_engine.is_on_ladder():

                self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        
        #controle player 2
        if key == arcade.key.W:
            if self.physics_engine2.is_on_ladder():
                self.player_sprite2.change_y = 0

        elif key == arcade.key.S:
            if self.physics_engine2.is_on_ladder():
                self.player_sprite2.change_y = 0

        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite2.change_x = 0  

    """Direcionar para gameOver"""
    def gameOver(self):
        time.sleep(1)
        game_over_view = gameOver.GameOverView(self)
        self.window.show_view(game_over_view)

    """Direcionar para Vitoria"""
    def gameWin(self):
        time.sleep(1)
        game_win_view = gameOver.GameWinView(self)
        self.window.show_view(game_win_view)

    """Gerar os inimigos (barril) aleatoriamente"""
    def spawnBarril(self):
        # gerar ininigo
        
        self.enemy_sprite = barril.BarrilCharacter()

        # Set enemy initial position
        self.enemy_sprite.center_x = 195
        self.enemy_sprite.center_y = 505

        # Set enemy initial speed
        self.enemy_sprite.change_x = 5

        # Set boundaries on the left/right the enemy can't cross (limites)
        self.enemy_sprite.boundary_right = 680
        self.enemy_sprite.boundary_left = 140  
        self.enemy_sprite.boundary_bottom = -350
        self.physics_engine_enemy = arcade.PhysicsEnginePlatformer(
            self.enemy_sprite, self.walls, gravity_constant=GRAVITY
        )
        
        # Set enemy physics
        self.physics_engine_enemy_list.append(self.physics_engine_enemy)

        self.enemy_list.append(self.enemy_sprite)

    """Movement and game logic"""
    def on_update(self, delta_time):

        if not self.game_over and not self.game_win:

            #Spawn aleatorio do barril
            # Have a random 1 in 200 change of shooting each 1/60th of a second
            odds = 100
            # Adjust odds based on delta-time
            adj_odds = int(odds * (1 / 60) / delta_time)
            if random.randrange(adj_odds) == 0 and len(self.enemy_list) < 7:
                # self.cavaleiro_list.update_animation()
                self.spawnBarril()

            # Update the players animation
            self.player_list.update_animation()
            self.player_list2.update_animation()
            self.enemy_list.update_animation()
            
            # Generate a list of all sprites that collided with the player.
            hit_list_vitoria = arcade.check_for_collision_with_list(self.player_sprite, self.vitoria_list)
            hit_list_vitoria2 = arcade.check_for_collision_with_list(self.player_sprite2, self.vitoria_list)

            # Loop through each colliding sprite, remove it, and add to the score.
            for win in hit_list_vitoria:
                self.game_win = True

            for win in hit_list_vitoria2:
                self.game_win = True

            if self.player_sprite.bottom < self.player_sprite.boundary_bottom or self.player_sprite2.bottom < self.player_sprite2.boundary_bottom :
                self.game_over = True

            # Movimentação do barril
            for enemy in self.enemy_list:
                # If the enemy hit a wall, reverse
                # If the enemy hit the left boundary, reverse
                if enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                    enemy.change_x *= -1
                # If the enemy hit the right boundary, reverse
                elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1

                # Check this enemy to see if it hit a coin
                hit_list = arcade.check_for_collision_with_list(enemy, self.player_list)
                hit_list2 = arcade.check_for_collision_with_list(enemy, self.player_list2)

                # If it did, get rid of the enemy
                if len(hit_list) > 0 or len(hit_list2) > 0:

                    #mostrar a imagem de morto do player       
                    temp_x = self.player_list2[0].center_x 
                    temp_y = self.player_list2[0].center_y 
                    self.player_list2[0] = arcade.Sprite("assets/images/player_death.png", 0.9)
                    self.player_list2[0].center_x = temp_x
                    self.player_list2[0].center_y = temp_y

                    temp_x = self.player_list[0].center_x 
                    temp_y = self.player_list[0].center_y 
                    self.player_list[0] = arcade.Sprite("assets/images/player_death.png", 0.9)
                    self.player_list[0].center_x = temp_x
                    self.player_list[0].center_y = temp_y

                    self.game_over = True

                # If the enemy flies off-screen, remove it.
                if enemy.bottom < enemy.boundary_bottom:
                    enemy.remove_from_sprite_lists()

            #atualizar as fisicas
            self.physics_engine.update()
            self.physics_engine2.update()
            self.physics_engine_vitoria.update()
            for i in self.physics_engine_enemy_list:
                i.update()

        # em caso de Vitoria       
        elif self.game_win:
            self.gameWin()

        # em caso de gameOver 
        else:
            self.gameOver()
