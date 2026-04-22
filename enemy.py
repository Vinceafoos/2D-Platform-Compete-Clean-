from raylib import *
from pyray import *
from anim import *
from settings import *

class Enemy:
    def __init__(self, position):
        self.position = Vector2(0,0)
        self.width = TILE_SIZE
        self.height = TILE_SIZE

    
    def update(self):
        pass


    def get_rect(self):
        """Returns the enemy's collision bounding box."""
        return (self.x, self.y, self.width, self.height)

    def draw(self):
        """Draws the enemy as a red rectangle with a directional indicator."""
        DrawRectangle(int(self.position.x), int(self.position.y), int(self.width), int(self.height), RED)
        DrawRectangleLines(int(self.x), int(self.y), int(self.width), int(self.height), BLACK)
        
        # Draw a small indicator for direction
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        indicator_size = self.width * 0.2
        
        if self.vx > 0: # Moving Right
            DrawTriangle(Vector2(center_x + indicator_size, center_y), 
                         Vector2(center_x - indicator_size, center_y - indicator_size), 
                         Vector2(center_x - indicator_size, center_y + indicator_size), WHITE)
        elif self.vx < 0: # Moving Left
            DrawTriangle(Vector2(center_x - indicator_size, center_y), 
                         Vector2(center_x + indicator_size, center_y - indicator_size), 
                         Vector2(center_x + indicator_size, center_y + indicator_size), WHITE)