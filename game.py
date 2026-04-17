from raylib import *
from pyray import *
from anim import *
from player import *
from enemy import *

class Game:
    def __init__(self):
        self.player = Player()
        self.enemy = Enemy()
    