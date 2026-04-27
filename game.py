from raylib import *
from pyray import *
from anim import *
from player import *
from enemy import *
from weight import *
from blood import *

class Game:
    def __init__(self):
        self.player = Player()
        self.enemy = Enemy(Vector2(0,0))
        self.camera = Camera2D()
        self.weight = Weight(0,0)
        self.blood = Blood(0,0)

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
    
    def startup(self, level):
        self.camera.target = Vector2(self.player.position.x, self.player.position.y)
        self.camera.offset = Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0
        for row in range(TILE_ROWS):
            for col in range(TILE_COLS):
                tile_value = level[row][col]
                if tile_value == TILE_WEIGHT:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    self.weight.arr.append(Weight(int(x + 0.5 * TILE_SIZE), int(y + 0.5 * TILE_SIZE)))
                if tile_value == TILE_BLOOD:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    self.blood.arr.append(Blood(int(x + 5), int(y + 5)))


    def item_player_collision(self):
        for item in self.weight.arr:
            if check_collision_circle_rec(Vector2(item.position.x,item.position.y), item.radius, self.player.bounding_box):
                item.active = False
        for item in self.blood.arr:
            if check_collision_circle_rec(Vector2(item.position.x,item.position.y), item.radius, self.player.bounding_box):
                item.active = False
        

    def update(self):
        self.item_player_collision()
        self.player.update()
        self.update_camera()
        

    def update_camera(self):
        self.camera.target.x = self.player.position.x + PLAYER_SIZE/2
        self.camera.target.y = self.player.position.y + PLAYER_SIZE/2
        min_x = SCREEN_WIDTH / 2
        max_x = WORLD_WIDTH - SCREEN_WIDTH / 2
        
        if self.camera.target.x < min_x:
            self.camera.target.x = min_x
        if self.camera.target.x > max_x:
            self.camera.target.x = max_x

        min_y = SCREEN_HEIGHT / 2
        max_y = WORLD_HEIGHT - SCREEN_HEIGHT / 2
        
        if self.camera.target.y < min_y:
            self.camera.target.y = min_y
        if self.camera.target.y > max_y:
            self.camera.target.y = max_y
        
        self.camera.offset.x = SCREEN_WIDTH / 2
        self.camera.offset.y = SCREEN_HEIGHT / 2

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
        self.draw_level(LEVEL1)
        self.blood.draw()
        self.weight.draw()
