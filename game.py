from raylib import *
from pyray import *
from anim import *
from player import *
from enemy import *

class Game:
    def __init__(self):
        self.player = Player()
        self.enemy = Enemy()
        self.camera = Camera2D()

    """
    def parse_level(level):
        
        # Create a deep copy of the level to modify the tiles, leaving the original map intact
        new_level = [row[:] for row in level] 
        
        for r in range(TILE_ROWS):
            for c in range(TILE_COLS):
                x = c * TILE_SIZE
                y = r * TILE_SIZE

                if new_level[r][c] == TILE_COIN:
                    # Coin position is center
                    coins.append((x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                    new_level[r][c] = TILE_AIR 
                
                elif new_level[r][c] == TILE_ENEMY:
                    # Enemy position is top-left
                    enemies.append(Enemy(x, y))
                    new_level[r][c] = TILE_AIR 
                    
        return new_level
        """
    def update(self):
        self.player.update()

        self.camera.target.x = self.player.position.x + PLAYER_SIZE/2
        self.camera.target.y = self.player.position.y + PLAYER_SIZE/2


    def draw_level(self, level):
        """Draws the solid tiles of the level map."""
        for row in range(TILE_ROWS):
            for col in range(TILE_COLS):
                tile_value = level[row][col]
                if tile_value == TILE_SOLID:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    
                    draw_rectangle(x, y, TILE_SIZE, TILE_SIZE, DARKGRAY)
                    draw_rectangle_lines(x, y, TILE_SIZE, TILE_SIZE, BLACK)
    
    def draw(self):
        self.player.draw()
