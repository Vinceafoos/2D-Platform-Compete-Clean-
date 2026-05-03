from raylib import *
from pyray import *
from anim import *
from settings import * 
from game import *
from enemy import *
from javelin import *


class State:
    IDLE = 6
    THROW = 7

class Thrower(Enemy):

    def __init__(self, position):
        self.position = position
        self.size = Vector2(PLAYER_BOUNDING_BOX_WIDTH, PLAYER_BOUNDING_BOX_HEIGHT)
        self.alive = True
        self.can_shoot = True
        self.texture = load_texture(SHEET)
        self.total_time = 0
        self.state = State.IDLE
        self.player_direction = Direction.LEFT


        self.startup()

    def startup(self):
        self.texture = load_texture(SHEET)
        self.direction = Direction.LEFT


        self.animation = Animation(
            first = 0, 
            last = 0,
            cur = 0,
            step = 1,
            duration = 0.5,
            duration_left = 0.5,
            anim_type=AnimationType.REPEATING,
            row = 6,
            sprites_in_row=1
        )
        self.frame = self.animation.frame()
        self.frame.width *= self.direction

    def update(self):
        dt = get_frame_time()
        #every 3 seconds throw
        self.total_time +=1
        if self.total_time %120 ==0:
            print(f"ticks:{self.total_time}, current:{self.animation.cur}")
        if self.total_time % 360 == 0:
            self.transition(State.THROW)
        
        if self.state == State.THROW and self.animation.cur == 2: 
            self.transition(State.IDLE)
            return Javelin(Vector2(self.position.x,self.position.y))
        
        self.animation.update(dt)
        self.frame = self.animation.frame()
        return None
        
    def transition(self, state):
        if state == self.animation.row:
            return
        self.animation.cur = 0
        self.state = state
        match state:
            case State.IDLE:
                self.animation.row = State.IDLE
                self.animation.sprites_in_row = 4
                self.animation.last = 0
                self.animation.type = AnimationType.REPEATING
                self.animation.duration = 0.5
            case State.THROW:
                self.animation.row = State.THROW
                self.animation.sprites_in_row = 4
                self.animation.last = 2
                self.animation.type = AnimationType.ONESHOT
                self.animation.duration_left = 2.0
                self.animation.duration = 2.0
    
    def draw(self):
        
        draw_texture_pro(
            self.texture,
            self.frame,
            Rectangle(self.position.x, self.position.y, TILE_SIZE, TILE_SIZE),
            (0,0), 0.0, WHITE
        )
        

    def shutdown(self):
        unload_texture(self.texture)
