"""Imports"""
import arcade

"""Constantes"""
CHARACTER_SCALING = 1.5
UPDATES_PER_FRAME = 15
RIGHT_FACING = 0
LEFT_FACING = 1

"""Load a texture pair, with the second being a mirror image."""
def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class BarrilCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)

        # --- Load Textures ---
        # Images from Kenney.nl's Asset Pack 3
        main_path = "assets/images/barril"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_1.png")

        # Load textures for walking
        self.walk_textures = []

        for i in range(1,5):
            texture = load_texture_pair(f"{main_path}_{i}.png")
            self.walk_textures.append(texture)

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


        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 3 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]
