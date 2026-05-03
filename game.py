from raylib import *
from pyray import *
from anim import *
from player import *
from enemy import *
from weight import *
from blood import *
from javelin import *
from thrower import *
import random

class GameStates:
    SPLASH = 1
    GAME = 2
    WIN = 3
    LOSE = 4
    INSTRUCTIONS = 5
    IN_BETWEEN = 6
    CALCULATING = 7
    DEFEAT = 8


class Game:
    def __init__(self):
        self.player = Player()
        self.enemy = Enemy(Vector2(0,0))
        self.camera = Camera2D()
        self.weight = Weight(0,0)
        self.blood = Blood(0,0)
        self.curr_evidence = 0
        self.total_evidence = 0
        self.curr_time = 0
        self.start_time = 0
        self.debug = False
        self.win_tiles = []
        self.game_state = GameStates.SPLASH
        self.curr_level = 0
        self.javelins = []
        self.enemies = []
        self.spike_rects = []
        self.total_time = 0
        self.splash = load_texture(SPLASH)
        self.splash_src = Rectangle(0,0,self.splash.width,self.splash.height)
        self.screen_size = Rectangle(0,0,SCREEN_WIDTH, SCREEN_HEIGHT)
        self.level_complete = load_texture(LEVEL_COMPLETE)
        self.num_evidence = 0
        self.win = False
        self.calculating = load_texture(CALCULATING)
        self.loading_bar = Rectangle(215,400,0,30)
        self.caught = load_texture(CAUGHT)
        self.escaped = load_texture(ESCAPED)
        self.defeat = load_texture(DEFEAT)


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
                    if random.random() < 0.8:
                        self.blood.arr.append(Blood(int(x + 5), int(y + 5)))
                        self.num_evidence += 1
                if tile_value == TILE_WIN:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    self.win_tiles.append(Rectangle(x,y,TILE_SIZE, TILE_SIZE))
                if tile_value == TILE_THROWER:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    self.enemies.append(Thrower(Vector2(x,y)))
                if tile_value == TILE_SPIKE:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    self.spike_rects.append(Rectangle(x, y, TILE_SIZE, SPIKE_TIP_HEIGHT))


        self.track_texture = load_texture(TRACK_GROUND)
        self.stone_texture = load_texture(STONE_GROUND)
        self.sand_texture = load_texture(SAND_GROUND)
        self.dirt_texture = load_texture(DIRT_GROUND)
        self.spike_texture = load_texture(SPIKES)
        self.background_texture = load_texture(BACKGROUND)


    def item_player_collision(self):
        for item in self.weight.arr:
            if check_collision_circle_rec(Vector2(item.position.x + 14,item.position.y + 12), item.radius, self.player.bounding_box):
                if item.active: self.player.strength += 100
                item.active = False
        for item in self.blood.arr:
            if check_collision_circle_rec(Vector2(item.position.x + 14,item.position.y + 12), item.radius, self.player.bounding_box):
                if item.active: self.curr_evidence += 1
                item.active = False
        hit_javelin = None
        for javelin in self.javelins:
            if check_collision_circle_rec(javelin.tip(), javelin.tip_radius, self.player.bounding_box):
                if javelin.active and self.player.invincible_timer <= 0:
                    self.player.health -= 1
                    self.player.invincible_timer = 1.5
                    hit_javelin = javelin
                    break
        if hit_javelin:
            self.javelins.remove(hit_javelin)
        if self.player.invincible_timer <= 0:
            for spike_rect in self.spike_rects:
                if check_collision_recs(self.player.bounding_box, spike_rect):
                    self.player.health -= 1
                    self.player.invincible_timer = 1.5
                    break

    def check_win(self):
        for rec in self.win_tiles:
            if check_collision_recs(self.player.bounding_box, rec):
                self.game_state = GameStates.IN_BETWEEN
                self.enemies.clear()
                self.javelins.clear()
        if self.debug:
            if is_key_pressed(KeyboardKey.KEY_N):
                self.game_state = GameStates.IN_BETWEEN


    def hits_solid(self, jav, level):
            col = int(jav.position.x // TILE_SIZE)
            row = int(jav.position.y // TILE_SIZE)
            return level[row][col] == TILE_SOLID or level[row][col] >= 10

    def out_of_bounds(self, jav):
            col = int(jav.position.x // TILE_SIZE)
            row = int(jav.position.y // TILE_SIZE)
            return row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS
    
    def jav_world_collisions(self, level):
        to_remove = []
        for jav in self.javelins:
            if not jav.active:
                continue
            if self.out_of_bounds(jav):
                to_remove.append(jav)
            elif self.hits_solid(jav, level):
                jav.stick()
        self.javelins = [j for j in self.javelins if j not in to_remove]

    def calculate_win(self):
        percent = self.total_evidence / self.num_evidence
        if random.random() < percent:
            self.win = True

    def restart_level(self):
        self.curr_evidence = 0
        self.weight.arr = []
        self.blood.arr = []
        self.win_tiles = []
        self.enemies = []
        self.javelins = []
        self.spike_rects = []
        self.player.strength = 0
        self.player.health = 3
        self.player.position = Vector2(SCREEN_WIDTH/4, SCREEN_HEIGHT)

    
    def next_level(self):
        self.total_evidence += self.curr_evidence
        self.curr_evidence = 0
        self.curr_level += 1
        self.weight.arr = []
        self.blood.arr = []
        self.win_tiles = []
        self.spike_rects = []
        self.player.strength = 0
        self.player.health = 3
        self.total_time += self.curr_time

    def reset(self):
        self.next_level()
        self.total_time = 0
        self.total_evidence = 0
        self.num_evidence = 0
        self.win = False
        self.curr_level = 0
        self.player.health = 3
        self.game_state = GameStates.SPLASH


    def update(self):
        match self.game_state:
            case GameStates.GAME:
                self.curr_time = get_time() - self.start_time
                self.item_player_collision()
                self.player.update(LEVELS[self.curr_level])
                for enemy in self.enemies:
                    javelin = enemy.update()
                    if javelin != None:
                        self.javelins.append(javelin)
                for javelin in self.javelins:
                    javelin.update()
                self.jav_world_collisions(LEVELS[self.curr_level])
                self.update_camera()
                self.check_debug()
                self.weight.update()
                self.check_win()
                if self.player.health < 1:
                    self.game_state = GameStates.DEFEAT
            case GameStates.IN_BETWEEN:
                if is_key_pressed(KEY_SPACE):
                    self.next_level()
                    if self.curr_level > 2:
                        self.calculate_win()
                        self.game_state = GameStates.CALCULATING
                    else:
                        self.startup(LEVELS[self.curr_level])
                        self.player.position = Vector2(SCREEN_WIDTH/4, SCREEN_HEIGHT)
                        self.game_state = GameStates.GAME
            case GameStates.SPLASH:
                if is_key_pressed(KEY_SPACE):
                    self.startup(LEVELS[self.curr_level])
                    self.game_state = GameStates.GAME
            case GameStates.CALCULATING:
                self.loading_bar.width += 1
                if self.loading_bar.width > 370:
                    if self.win:
                        self.game_state = GameStates.WIN
                    else:
                        self.game_state = GameStates.LOSE
            case GameStates.WIN | GameStates.LOSE:
                if is_key_pressed(KeyboardKey.KEY_SPACE):
                    self.reset()
            case GameStates.DEFEAT:
                if is_key_pressed(KeyboardKey.KEY_SPACE):
                    self.restart_level()
                    self.startup(LEVELS[self.curr_level])
                    self.game_state = GameStates.GAME
                if is_key_pressed(KeyboardKey.KEY_ENTER):
                    self.next_level()
                    self.reset()
                    self.game_state = GameStates.SPLASH


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
                if tile_value >= 10 or tile_value == TILE_SOLID:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    match tile_value:
                        case 10:
                            draw_texture(self.track_texture,x,y, WHITE)
                        case 11:
                            draw_texture(self.stone_texture,x,y, WHITE)
                        case 12:
                            draw_texture(self.sand_texture,x,y, WHITE)
                        case 13:
                            draw_texture(self.dirt_texture,x,y, WHITE)
                        case 1:
                            draw_texture(self.dirt_texture, x, y, WHITE)
                        case 14:
                            draw_texture(self.spike_texture,x,y, WHITE)

    def draw_hud(self):
        draw_texture(self.background_texture, 0, 0, LIGHTGRAY)
        draw_rectangle(0,0,TILE_COLS * TILE_SIZE,30, WHITE)
        draw_text(f"Evidence Collected: {self.curr_evidence}", 5,5,20, BLACK)
        draw_text(f"Strength: {self.player.strength}", 280,5,20, BLACK)
        draw_text(f"Health: {self.player.health}", 470, 5, 20, BLACK)
        draw_text(f"Current Time: {self.curr_time:.2f}", 600,5,20, BLACK)

    def draw_debug(self):
        if self.debug:
            draw_text(f"Grounded: {self.player.grounded}", int(self.player.position.x), int(self.player.position.y - 100), 20, PINK)
    
    def draw_screens(self):
        match self.game_state:
            case GameStates.SPLASH:
                draw_texture_pro(self.splash, self.splash_src, self.screen_size, (0,0), 0, WHITE)
            case GameStates.IN_BETWEEN:
                draw_texture_pro(self.level_complete, self.splash_src, self.screen_size, (0,0), 0, WHITE)
                draw_text(f"{self.curr_evidence} Blood Bags", 265, 280, 40, RED)
                draw_text(f"{self.curr_time:.2f} Seconds", 265, 415, 40, WHITE)
            case GameStates.CALCULATING:
                draw_texture_pro(self.calculating, self.splash_src, self.screen_size, (0,0), 0, WHITE)
                draw_rectangle_rec(self.loading_bar, GREEN)
            case GameStates.WIN:
                draw_texture_pro(self.caught, self.splash_src, self.screen_size, (0,0), 0, WHITE)
                draw_text(f"{self.total_evidence} Blood Bags", 265, 255, 40, RED)
                draw_text(f"{self.total_time:.2f} Seconds", 265, 355, 40, WHITE)
            case GameStates.LOSE:
                draw_texture_pro(self.escaped, self.splash_src, self.screen_size, (0,0), 0, WHITE)
                draw_text(f"{self.total_evidence} Blood Bags", 265, 255, 40, RED)
                draw_text(f"{self.total_time:.2f} Seconds", 265, 355, 40, WHITE)
            case GameStates.DEFEAT:
                draw_texture_pro(self.defeat, self.splash_src, self.screen_size, (0,0), 0, WHITE)



    def draw(self):
        match self.game_state:
            case GameStates.GAME:
                self.draw_level(LEVELS[self.curr_level])
                self.player.draw(self.debug)
                for enemy in self.enemies:
                    enemy.draw()
                for javelin in self.javelins:
                    javelin.draw(self.debug)
                self.blood.draw()
                self.weight.draw()
                self.draw_debug()
            
    def shutdown(self):
        self.player.shutdown()
        for enemy in self.enemies:
            enemy.shutdown()
        for javelin in self.javelins:
            javelin.shutdown()
        unload_texture(TRACK_GROUND)
        unload_texture(STONE_GROUND)
        unload_texture(SAND_GROUND)
        unload_texture(DIRT_GROUND)
        unload_texture(SPIKES)
