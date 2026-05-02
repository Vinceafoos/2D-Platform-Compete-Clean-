from raylib import *
from pyray import *
from anim import *
from settings import *
from game import *
from enemy import *
import math




class Javelin:
    def __init__(self, position, speed_x=-200, speed_y=-60):
        self.position = position
        self.texture = load_texture(JAVELIN_SPRITE)
        self.velocity = Vector2(speed_x, speed_y)
        self.active = True
        self.stuck_angle = None
        self.tip_radius = 4

    def update(self):
        if not self.active:
            return
        dt = get_frame_time()
        self.velocity.y += GRAVITY * 0.10 * dt
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt


    def tip(self):
        
        if self.stuck_angle is not None:
            angle_rad = math.radians(self.stuck_angle)
        else:
            angle_rad = math.atan2(self.velocity.y, self.velocity.x)
        half_len = self.texture.width / 2
        return Vector2(
            self.position.x + math.cos(angle_rad) * half_len,
            self.position.y + math.sin(angle_rad) * half_len,
        )

    def stick(self):
        self.stuck_angle = math.degrees(math.atan2(self.velocity.y, self.velocity.x))
        self.velocity.x = 0
        self.velocity.y = 0
        self.active = False

    def draw(self, debug=False):
        if self.stuck_angle != None:
            angle = self.stuck_angle 
        else:
            angle = math.degrees(math.atan2(self.velocity.y, self.velocity.x))
        w = self.texture.width
        h = self.texture.height
        draw_texture_pro(
            self.texture,
            Rectangle(0, 0, w, h),
            Rectangle(self.position.x, self.position.y, w, h),
            Vector2(w / 2, h / 2),
            angle,
            WHITE
        )
        if debug:
            t = self.tip()
            draw_circle_lines(int(t.x), int(t.y), self.tip_radius, RED)
