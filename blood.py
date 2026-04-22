from raylib import *
from pyray import *
from anim import *

class Blood():
    def __init__(self, x, y):
        self.position = Vector2(x,y)
        self.arr = []
        self.radius = 10
        self.active = True

    def update(self):
        pass
    def draw(self):
        for item in self.arr:
            if item.active:
                draw_circle(int(item.position.x), int(item.position.y), self.radius, RED)
