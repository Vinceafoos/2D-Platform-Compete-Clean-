from raylib import *
from pyray import *
from anim import *

class Blood():
    def __init__(self, x, y):
        self.position = Vector2(x,y)
        self.arr = []
        self.radius = 8
        self.active = True
        self.sprite = load_texture(BLOOD_SPRITE)
        self.src_rec = Rectangle(0,0,self.sprite.width,self.sprite.height)
        self.dest_rec = Rectangle(0,0,30, 30)

    def update(self):
        pass
    def draw(self):
        for item in self.arr:
            if item.active:
                self.dest_rec.x = item.position.x
                self.dest_rec.y = item.position.y
                draw_texture_pro(self.sprite, 
                                 self.src_rec, 
                                 self.dest_rec, 
                                 (0,0), 0, WHITE)
                #draw_circle(int(item.position.x + 14), int(item.position.y + 12), self.radius, RED)
