from raylib import *
from pyray import *
from anim import *

class Weight():
    def __init__(self, x, y):
        self.position = Vector2(x,y)
        self.arr = []
        self.radius = 10
        self.active = True
        self.dest_rec = Rectangle(0,0,TILE_SIZE, TILE_SIZE)
        self.startup()

    def startup(self):
        self.texture = load_texture(SHEET)
        self.state = Animation(
            first =0,
            last = 3,
            cur = 0,
            step = 1,
            duration = .15,
            duration_left= .1,
            anim_type= AnimationType.REPEATING,
            row = 5,
            sprites_in_row= 4
        )
        self.frame = self.state.frame()

    def update(self,):
        dt = get_frame_time()
        self.state.update(dt)
        self.frame = self.state.frame()

    def draw(self):
        for item in self.arr:
            if item.active:
                self.dest_rec.x = item.position.x
                self.dest_rec.y = item.position.y
                draw_texture_pro(
                    self.texture,
                    self.frame,
                    self.dest_rec,
                    (0,0), 0.0, WHITE
                )
                #draw_circle(int(item.position.x + 14), int(item.position.y + 12), self.radius, GRAY)