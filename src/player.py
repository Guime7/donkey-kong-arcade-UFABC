"""Imports"""
import arcade
import src.game as game

"""Constantes"""
CHARACTER_SCALING = 0.9
UPDATES_PER_FRAME = 20
RIGHT_FACING = 0
LEFT_FACING = 1

"""Load a texture pair, with the second being a mirror image."""
def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class PlayerCharacter(arcade.Sprite):
    def __init__(self, jogador):

        # Set up parent class
        super().__init__()
        self.moveSpeed = game.MOVEMENT_SPEED

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.ladder_cur_texture = 0
        self.scale = CHARACTER_SCALING
        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)

        # --- Load Textures ---
        # Images from Kenney.nl's Asset Pack 3


        if(jogador == 1):
            # Load textures for idle standing
            main_path = "assets/images/player"
            self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

            # Load textures for walking
            self.walk_textures = []
            self.ladder_textures = []

            #quando tiver andando normal
            for i in range(1,5):
                texture = load_texture_pair(f"{main_path}_{i}.png")
                self.walk_textures.append(texture)

            #para quando for subir escada
            for i in range(1,3):
                texture = load_texture_pair(f"{main_path}_escada_{i}.png")
                self.ladder_textures.append(texture)
        else:
            main_path = "assets/images/P2"
            # Load textures for idle standing
            self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

            # Load textures for walking
            self.walk_textures = []
            self.ladder_textures = []

            #quando tiver andando normal
            for i in range(1,5):
                texture = load_texture_pair(f"{main_path}_{i}.png")
                self.walk_textures.append(texture)

            #para quando for subir escada
            for i in range(1,3):
                texture = load_texture_pair(f"{main_path}_escada_{i}.png")
                self.ladder_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        #animação na escada
        if self.change_y == self.moveSpeed:
            self.cur_texture = 0
            self.ladder_cur_texture += 1

            if self.ladder_cur_texture > 2 * UPDATES_PER_FRAME:
                self.ladder_cur_texture = 0

            frame = self.ladder_cur_texture // UPDATES_PER_FRAME

            if self.moveSpeed > 0:
                self.texture = self.ladder_textures[frame][1]
            else:
                self.texture = self.ladder_textures[frame][0]

        # Walking animation
        else:
            self.ladder_cur_texture = 0
            self.cur_texture += 1

            if self.cur_texture > 3 * UPDATES_PER_FRAME:
                self.cur_texture = 0

            frame = self.cur_texture // UPDATES_PER_FRAME

            direction = self.character_face_direction
            self.texture = self.walk_textures[frame][direction]
