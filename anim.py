from raylib import *
from pyray import *
from settings import *

class AnimationType():
    REPEATING = 1
    ONESHOT = 2

class Direction():
    LEFT = -1
    RIGHT = 1
    NEITHER = 0

class Animation:
    def __init__(self, first, last, cur, step, duration, duration_left, anim_type, row, sprites_in_row):
        self.first = first
        self.last = last
        self.cur = cur
        self.step = step
        self.duration = duration
        self.duration_left = duration_left
        self.type = anim_type
        self.row = row
        self.sprites_in_row = sprites_in_row 
        self.done = False
        self.frame_rec = Rectangle(0,0,SPRITE_SHEET_TILE_SIZE, SPRITE_SHEET_TILE_SIZE)

    def update(self, dt):
        self.duration_left -= dt
        if (self.duration_left<=0):
            self.duration_left = self.duration
            self.cur += self.step
            if (self.cur > self.last):
                match(self.type):
                    case AnimationType.ONESHOT:
                        self.cur = self.last 
                        self.done = True
                    case AnimationType.REPEATING:
                        self.cur = self.first 

    def frame(self):
        self.frame_rec.x = (self.cur % self.sprites_in_row) * SPRITE_SHEET_TILE_SIZE
        self.frame_rec.y =  SPRITE_SHEET_TILE_SIZE * self.row
        return self.frame_rec

    def reset(self): 
        self.cur = self.first
        self.done = False
        self.type = AnimationType.REPEATING