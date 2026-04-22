from raylib import *
from pyray import *
from anim import *
from settings import * 
from game import *
from enemy import *

class Thrower(Enemy):

    def __init__(self, position):
        self.position = position
        
