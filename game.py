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
        self.cum_evidence = 0
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
        self.curr_level_evidence = 0
        self.total_evidence = 0
        self.win = False
        self.calculating = load_texture(CALCULATING)
        self.loading_bar = Rectangle(215,400,0,30)
        self.caught = load_texture(CAUGHT)
        self.escaped = load_texture(ESCAPED)
        self.defeat = load_texture(DEFEAT)
        self.flag = load_texture(FLAG)
        self.pause_white = Color(255, 255, 255, 127)
        self.pause = False
        self.pause_seconds = 0
        self.paused_at = 0
        self.unpaused_at = 0
        self.instructions = load_texture(INSTRUCTIONS)
        self.cloud_textures = [load_texture(p) for p in CLOUD_SPRITES]
        self.cloud_sizes = [(t.width, t.height) for t in self.cloud_textures]
        self.clouds = []
        self.cloud_spawn_timer = 0.0
        self.cloud_spawn_interval = 4.0
        for x_start in [SCREEN_WIDTH * 0.1, SCREEN_WIDTH * 0.35,
                        SCREEN_WIDTH * 0.6, SCREEN_WIDTH * 0.85]:
            self._try_spawn_cloud(x_override=x_start)
        hud_icon_size = 25
        heart_img = load_image(HEART_SPRITE)
        image_resize(heart_img, hud_icon_size, hud_icon_size)
        self.hud_heart = load_texture_from_image(heart_img)
        unload_image(heart_img)
        blood_img = load_image(BLOOD_BAG_HUD)
        image_resize(blood_img, hud_icon_size, hud_icon_size)
        self.hud_blood = load_texture_from_image(blood_img)
        unload_image(blood_img)
        self.hud_icon_size = hud_icon_size
        self.level_name = ""
        self.level_name_timer = 0.0
        self.popups = []
        self.shake_timer = 0.0
        self.evidence_flash_timer = 0.0
        self.weight_sound = load_sound(WEIGHT_SOUND)
        self.blood_sound = load_sound(BLOOD_SOUND)
        self.track_texture = load_texture(TRACK_GROUND)
        self.stone_texture = load_texture(STONE_GROUND)
        self.sand_texture = load_texture(SAND_GROUND)
        self.dirt_texture = load_texture(DIRT_GROUND)
        self.spike_texture = load_texture(SPIKES)
        self.background_texture = load_texture(BACKGROUND)


    def startup(self, level):
        self.start_time = get_time()
        names = ["Level 1", "Level 2", "Level 3"]
        self.level_name = names[self.curr_level] if self.curr_level < len(names) else f"Level {self.curr_level + 1}"
        self.level_name_timer = 2.0
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
                        self.curr_level_evidence += 1
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
                    spike_x_pad = 4
                    self.spike_rects.append(Rectangle(x + spike_x_pad, y + TILE_SIZE - SPIKE_TIP_HEIGHT, TILE_SIZE - spike_x_pad * 2, SPIKE_TIP_HEIGHT))


    def item_player_collision(self):
        for item in self.weight.arr:
            if check_collision_circle_rec((item.position.x + 14,item.position.y + 12),
                                           item.radius, self.player.bounding_box):
                if item.active:
                    self.player.strength += 100
                    play_sound(self.weight_sound)
                    self.popups.append({'x': item.position.x + 14, 'y': item.position.y, 'timer': 1.2, 'text': '+100', 'color': (255, 255, 255)})
                item.active = False
        for item in self.blood.arr:
            if check_collision_circle_rec((item.position.x + 14,item.position.y + 12),
                                           item.radius, self.player.bounding_box):
                if item.active:
                    self.curr_evidence += 1
                    play_sound(self.blood_sound)
                    self.popups.append({'x': item.position.x + 14, 'y': item.position.y, 'timer': 1.2, 'text': '+1', 'color': (255, 80, 80)})
                    self.evidence_flash_timer = 0.3
                item.active = False
        hit_javelin = None
        for javelin in self.javelins:
            if check_collision_circle_rec(javelin.tip(), javelin.tip_radius, self.player.bounding_box):
                if javelin.active and self.player.invincible_timer <= 0:
                    self.player.health -= 1
                    self.player.invincible_timer = 1.5
                    self._on_damage()
                    hit_javelin = javelin
                    break
        if hit_javelin:
            hit_javelin.shutdown()
            self.javelins.remove(hit_javelin)
        if self.player.invincible_timer <= 0:
            for spike_rect in self.spike_rects:
                if check_collision_recs(self.player.bounding_box, spike_rect):
                    self.player.health -= 1
                    self.player.invincible_timer = 1.5
                    self._on_damage()
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
                to_remove.append(jav)
        for jav in to_remove:
            jav.shutdown()
        self.javelins = [j for j in self.javelins if j not in to_remove]

    def calculate_win(self):
        percent = self.cum_evidence / self.total_evidence
        print(self.cum_evidence)
        print(self.total_evidence)
        print(percent)
        x = random.random()
        print(x)
        if x < percent:
            self.win = True

    def restart_level(self):
        self.curr_evidence = 0
        self.curr_level_evidence = 0
        self.pause_seconds = 0
        self.weight.arr = []
        self.blood.arr = []
        self.win_tiles = []
        self.enemies = []
        self.javelins = []
        self.spike_rects = []
        self.player.strength = 0
        self.player.health = 3
        self.player.position = Vector2(SCREEN_WIDTH/4, SCREEN_HEIGHT)
        self.shake_timer = 0.0
        self.evidence_flash_timer = 0.0
        self.popups = []

    
    def next_level(self):
        self.cum_evidence += self.curr_evidence
        self.total_evidence += self.curr_level_evidence
        self.curr_level_evidence = 0
        self.pause_seconds = 0
        self.curr_evidence = 0
        self.curr_level += 1
        self.weight.arr = []
        self.blood.arr = []
        self.enemies = []
        self.javelins = []
        self.win_tiles = []
        self.spike_rects = []
        self.player.strength = 0
        self.player.health = 3
        self.total_time += self.curr_time

    def reset(self):
        self.next_level()
        self.total_time = 0
        self.cum_evidence = 0
        self.total_evidence = 0
        self.win = False
        self.curr_level = 0
        self.game_state = GameStates.SPLASH
        self.player.position = Vector2(SCREEN_WIDTH/4, SCREEN_HEIGHT)

    def resume_timer(self):
        self.unpaused_at = get_time()
        self.pause_seconds += self.unpaused_at - self.paused_at

    def handle_pausing(self):
        if not self.pause:
            self.paused_at = get_time()
        else:
            self.resume_timer()
        self.pause = not self.pause

    def update(self):
        match self.game_state:
            case GameStates.GAME:
                if(is_key_pressed(KeyboardKey.KEY_P)):
                    self.handle_pausing()
                if not self.pause:
                    self.curr_time = get_time() - self.start_time - self.pause_seconds
                    self.item_player_collision()
                    self.player.update(LEVELS[self.curr_level])
                    for enemy in self.enemies:
                        javelin = enemy.update()
                        if javelin != None:
                            self.javelins.append(javelin)
                    for javelin in self.javelins:
                        javelin.update()
                    self.jav_world_collisions(LEVELS[self.curr_level])
                    self.update_clouds()
                    self.update_camera()
                    dt = get_frame_time()
                    self.level_name_timer = max(0.0, self.level_name_timer - dt)
                    self.shake_timer = max(0.0, self.shake_timer - dt)
                    self.evidence_flash_timer = max(0.0, self.evidence_flash_timer - dt)
                    for p in self.popups:
                        p['y'] -= 50 * dt
                        p['timer'] -= dt
                    self.popups = [p for p in self.popups if p['timer'] > 0]
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
                    self.game_state = GameStates.INSTRUCTIONS
            case GameStates.INSTRUCTIONS:
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
                    self.loading_bar.width = 0
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
        if self.shake_timer > 0:
            self.camera.offset.x += random.randint(-5, 5)
            self.camera.offset.y += random.randint(-5, 5)

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

    def _on_damage(self):
        self.shake_timer = 0.3
        self.popups.append({'x': self.player.position.x, 'y': self.player.position.y - 10,
                            'timer': 1.2, 'text': '-1', 'color': (255, 30, 30)})

    def _cloud_x(self, c):
        return c['start_x'] + c['speed'] * (get_time() - c['start_time'])

    def _try_spawn_cloud(self, x_override=None):
        if len(self.clouds) >= 5:
            return
        idx = random.randrange(len(self.cloud_textures))
        w, h = self.cloud_sizes[idx]
        x = float(x_override) if x_override is not None else -float(w)
        y = random.uniform(35, 300)
        for c in self.clouds:
            cx = self._cloud_x(c)
            if (x < cx + c['w'] + 15 and x + w + 15 > cx and
                    y < c['y'] + c['h'] + 10 and y + h + 10 > c['y']):
                return
        self.clouds.append({'start_x': x, 'start_time': get_time(),
                            'y': y, 'idx': idx, 'w': w, 'h': h,
                            'speed': random.uniform(8, 15)})

    def update_clouds(self):
        t = get_time()
        self.clouds = [c for c in self.clouds
                       if c['start_x'] + c['speed'] * (t - c['start_time']) < SCREEN_WIDTH + 10]
        self.cloud_spawn_timer += get_frame_time()
        if self.cloud_spawn_timer >= self.cloud_spawn_interval:
            self._try_spawn_cloud()
            self.cloud_spawn_timer = 0.0
            self.cloud_spawn_interval = random.uniform(3.5, 5.0)

    def draw_clouds(self):
        for c in self.clouds:
            draw_texture_v(self.cloud_textures[c['idx']], Vector2(self._cloud_x(c), c['y']), WHITE)

    def shadow(self, text, x, y, size, color):
        draw_text(text, x+2, y+2, size, Color(0,0,0,170))
        draw_text(text, x, y, size, color)
        
    def draw_hud(self):
        s = self.hud_icon_size
        y = 6
        fs = 18
        for i in range(self.player.health):
            draw_texture(self.hud_heart, 270 + i * (s + 4), y, WHITE)

        blood_tint = Color(255, 255, 100, 255) if self.evidence_flash_timer > 0 else WHITE
        draw_texture(self.hud_blood, 360, y, blood_tint)
        self.shadow(f"x{self.curr_evidence}", 386, y + 3, fs, WHITE)
        self.shadow(f"STR: {self.player.strength}", 442, y + 3, fs, WHITE)
        self.shadow(f"{self.curr_time:.2f}s", SCREEN_WIDTH - 80, y + 3, fs, WHITE)

        if self.level_name_timer > 0:
            fade = int(min(255, self.level_name_timer * 200))
            fs_big = 48
            tw = measure_text(self.level_name, fs_big)
            draw_text(self.level_name, (SCREEN_WIDTH - tw) // 2 + 2, SCREEN_HEIGHT // 2 - 22, fs_big, Color(0, 0, 0, fade))
            draw_text(self.level_name, (SCREEN_WIDTH - tw) // 2,     SCREEN_HEIGHT // 2 - 24, fs_big, Color(255, 255, 255, fade))

    def draw_debug(self):
        if self.debug:
            draw_text(f"Grounded: {self.player.grounded}", int(self.player.position.x), int(self.player.position.y - 100), 20, PINK)
            for rect in self.spike_rects:
                draw_rectangle_lines(int(rect.x), int(rect.y), int(rect.width), int(rect.height), RED)
    
    def draw_screens(self):
        match self.game_state:
            case GameStates.SPLASH:
                draw_texture_pro(self.splash, self.splash_src, self.screen_size, (0,0), 0, WHITE)
            case GameStates.INSTRUCTIONS:
                draw_texture_pro(self.instructions, self.splash_src, self.screen_size, (0,0), 0, WHITE)
            case GameStates.IN_BETWEEN:
                draw_texture_pro(self.level_complete, self.splash_src, self.screen_size, (0,0), 0, WHITE)
                draw_text(f"{self.curr_evidence} Blood Bags", 265, 280, 40, RED)
                draw_text(f"{self.curr_time:.2f} Seconds", 265, 415, 40, WHITE)
            case GameStates.CALCULATING:
                draw_texture_pro(self.calculating, self.splash_src, self.screen_size, (0,0), 0, WHITE)
                draw_rectangle_rec(self.loading_bar, GREEN)
            case GameStates.WIN:
                draw_texture_pro(self.caught, self.splash_src, self.screen_size, (0,0), 0, WHITE)
                draw_text(f"{self.cum_evidence} Blood Bags", 265, 255, 40, RED)
                draw_text(f"{self.total_time:.2f} Seconds", 265, 355, 40, WHITE)
            case GameStates.LOSE:
                draw_texture_pro(self.escaped, self.splash_src, self.screen_size, (0,0), 0, WHITE)
                draw_text(f"{self.cum_evidence} Blood Bags", 265, 255, 40, RED)
                draw_text(f"{self.total_time:.2f} Seconds", 265, 355, 40, WHITE)
            case GameStates.DEFEAT:
                draw_texture_pro(self.defeat, self.splash_src, self.screen_size, (0,0), 0, WHITE)

    def draw(self):
        match self.game_state:
            case GameStates.GAME:
                self.draw_level(LEVELS[self.curr_level])
                draw_texture_pro(self.flag, Rectangle(0,0,self.flag.width,self.flag.height)
                                 ,Rectangle(WORLD_WIDTH-130,WORLD_HEIGHT-123,100,100),(0,0),0,WHITE)
                self.player.draw(self.debug)
                for enemy in self.enemies:
                    enemy.draw()
                for javelin in self.javelins:
                    javelin.draw(self.debug)
                self.blood.draw()
                self.weight.draw()
                self.draw_debug()
                for p in self.popups:
                    fade = int((p['timer'] / 1.2) * 255)
                    r, g, b = p['color']
                    draw_text(p['text'], int(p['x']), int(p['y']), 20, Color(r, g, b, fade))
                if self.pause:
                    draw_rectangle(int(self.camera.target.x - self.camera.offset.x),
                                    int(self.camera.target.y - self.camera.offset.y),
                                    SCREEN_WIDTH,SCREEN_HEIGHT,self.pause_white)
                    draw_text(f"GAME PAUSED", int(self.camera.target.x) - 250, int(self.camera.target.y), 70, RED)

            
    def shutdown(self):
        self.player.shutdown()
        for enemy in self.enemies:
            enemy.shutdown()
        for javelin in self.javelins:
            javelin.shutdown()
        unload_texture(self.track_texture)
        unload_texture(self.stone_texture)
        unload_texture(self.sand_texture)
        unload_texture(self.dirt_texture)
        unload_texture(self.spike_texture)
        unload_texture(self.splash)
        unload_texture(self.calculating)
        unload_texture(self.caught)
        unload_texture(self.escaped)
        unload_texture(self.defeat)
        unload_texture(self.flag)
        unload_texture(self.instructions)
        unload_sound(self.weight_sound)
        unload_sound(self.blood_sound)
