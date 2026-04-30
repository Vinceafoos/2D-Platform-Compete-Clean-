from raylib import *
from pyray import *
from anim import *
from settings import * 
from game import *
from enemy import *

class Thrower(Enemy):

    def __init__(self, position):
        self.position = position
        self.size = Vector2(PLAYER_BOUNDING_BOX_WIDTH, PLAYER_BOUNDING_BOX_HEIGHT)
        self.alive = True
        self.can_shoot = True
        self.texture = load_texture(SHEET)
        


        self.startup()

    def startup(self):
        self.texture = load_texture(SHEET)
        self.player_direction = Direction.RIGHT

        self.animation_throw = Animation(
            first = 0, 
            last = 2,
            cur = 0,
            step = 1,
            duration = 0.3,
            duration_left = 0.3

        )
        
