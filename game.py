from raylib import *
from pyray import *
from anim import *

class Player:
    def __init__(self):
        self.position = Vector2(0,0)
class Enemy:
    def __init__(self):
        self.position = Vector2(0,0)

class Game:
    def __init__(self):
        self.player = Player()
        self.enemy = Enemy()

