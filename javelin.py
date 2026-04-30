from raylib import *
from pyray import *
from anim import *
from settings import * 
from game import *
from enemy import *




class Javelin:
    def __init__(self, position):
        self.positon = position
        self.texture = load_texture(JAVELIN_SPRITE)

        
