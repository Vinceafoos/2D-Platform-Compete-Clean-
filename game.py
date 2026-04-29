from raylib import *
from pyray import *
from anim import *
from player import *
from enemy import *
from weight import *
from blood import *

class GameStates:
    SPLASH = 1
    GAME = 2
    WIN = 3
    LOSE = 4
    INSTRUCTIONS = 5
    IN_BETWEEN = 6

class Game:
    def __init__(self):
        self.player = Player()
        self.enemy = Enemy(Vector2(0,0))
        self.camera = Camera2D()
        self.weight = Weight(0,0)
        self.blood = Blood(0,0)
        self.evidence = 0
        self.curr_time = 0
        self.start_time = 0
        self.debug = False
        self.win_tiles = []
        self.game_state = 6
        self.curr_level = -1

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
        self.start_time = get_time()
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
                    self.weight.arr.append(Weight(int(x), int(y)))
                if tile_value == TILE_BLOOD:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    self.blood.arr.append(Blood(int(x + 5), int(y + 5)))
                if tile_value == TILE_WIN:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    self.win_tiles.append(Rectangle(x,y,TILE_SIZE, TILE_SIZE))


    def item_player_collision(self):
        for item in self.weight.arr:
            if check_collision_circle_rec(Vector2(item.position.x + 14,item.position.y + 12), item.radius, self.player.bounding_box):
                if item.active: self.player.strength += 50
                item.active = False
        for item in self.blood.arr:
            if check_collision_circle_rec(Vector2(item.position.x + 14,item.position.y + 12), item.radius, self.player.bounding_box):
                if item.active: self.evidence += 1
                item.active = False
        
    def check_win(self):
        for rec in self.win_tiles:
            if check_collision_recs(self.player.bounding_box, rec):
                self.game_state = GameStates.IN_BETWEEN

    def update(self):
        match self.game_state:
            case GameStates.GAME:
                self.curr_time = get_time() - self.start_time
                self.item_player_collision()
                self.player.update(LEVELS[self.curr_level])
                self.update_camera()
                self.check_debug()
                self.weight.update()
                self.check_win()
            case GameStates.IN_BETWEEN:
                if is_key_pressed(KEY_SPACE):
                    self.curr_level += 1
                    self.weight.arr = []
                    self.blood.arr = []
                    self.win_tiles = []
                    self.startup(LEVELS[self.curr_level])
                    self.player.position = Vector2(SCREEN_WIDTH/4, SCREEN_HEIGHT)

                    self.game_state = GameStates.GAME
                
        
    def check_debug(self):
        if is_key_pressed(KEY_I):
            self.debug = not self.debug

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

    def draw_hud(self):
        draw_rectangle(0,0,TILE_COLS * TILE_SIZE,30, WHITE)
        draw_text(f"Evidence Collected: {self.evidence}", 5,5,20, BLACK)
        draw_text(f"Strength: {self.player.strength}", 280,5,20, BLACK)
        draw_text(f"Health: {self.player.health}", 470, 5, 20, BLACK)
        draw_text(f"Current Time: {self.curr_time:.2f}", 600,5,20, BLACK)

    def draw_debug(self):
        if self.debug:
            draw_text(f"Grounded: {self.player.grounded}", 200, 200, 20, PINK)
    
    def draw(self):
        match self.game_state:
            case GameStates.GAME:
                self.draw_level(LEVELS[self.curr_level])
                self.player.draw()
                self.blood.draw()
                self.weight.draw()
                self.draw_debug()
            case GameStates.IN_BETWEEN:
                draw_rectangle(0,0,SCREEN_WIDTH,SCREEN_HEIGHT, WHITE)
