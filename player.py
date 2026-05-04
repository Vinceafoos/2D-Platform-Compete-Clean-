from pyray import *
from settings import *
from anim import *

class State:
    IDLE = 0
    RUNNING = 1
    JUMP = 2
    HEAL = 3
    CHARGE = 4

class Player():
    def __init__(self):
        self.position = Vector2(SCREEN_WIDTH/4, SCREEN_HEIGHT)
        self.velocity = Vector2(0, 0)
        self.grounded = True
        self.gravity = 2000
        self.jump_vel = -800
        self.state = Animation(
                    first=0, last=3, cur=0,
                    step=1, duration=0.1, duration_left=0.1,
                    anim_type=AnimationType.REPEATING,
                    row=0, sprites_in_row=4,)
        self.player_texture = load_texture(SHEET)
        self.player_frame = self.state.frame()
        self.player_direction = Direction.RIGHT
        self.bounding_box = Rectangle(self.position.x + PLAYER_HITBOX_X_OFFSET,
                                       self.position.y + PLAYER_HITBOX_Y_OFFSET,
                                         PLAYER_HITBOX_WIDTH, PLAYER_HITBOX_HEIGHT)
        self.strength = 0
        self.health = 3
        self.on_sand = False
        self.invincible_timer = 0.0
        self.player_dest_rec = Rectangle(0,0,PLAYER_BOUNDING_BOX_WIDTH, PLAYER_BOUNDING_BOX_HEIGHT)

    def get_rect(self):
        return (
            self.position.x + PLAYER_HITBOX_X_OFFSET,
            self.position.y + PLAYER_HITBOX_Y_OFFSET,
            PLAYER_HITBOX_WIDTH,
            PLAYER_HITBOX_HEIGHT,
        )

    def transition(self, state):
        if state == self.state.row:
            return
        self.state.cur = 0
        match state:
            case State.IDLE:
                self.state.row = State.IDLE
                self.state.sprites_in_row = 4
                self.state.type = AnimationType.REPEATING
                self.state.duration = 0.1
            case State.RUNNING:
                self.state.row = State.RUNNING
                self.state.sprites_in_row = 4
                self.state.type = AnimationType.REPEATING
                self.state.duration = 0.1
            case State.JUMP:
                self.state.row = State.JUMP
                self.state.sprites_in_row = 2
                self.state.type = AnimationType.ONESHOT
                self.state.duration = 0.1
            case State.HEAL:
                self.state.row = State.HEAL
                self.state.sprites_in_row = 5
                self.state.type = AnimationType.ONESHOT
                self.state.duration = 0.3
            case State.CHARGE:
                time_to_charge = ((((-self.jump_vel + self.strength) + self.jump_vel)/120)/2) / 4
                self.state.row = State.CHARGE
                self.state.sprites_in_row = 4
                self.state.type = AnimationType.ONESHOT
                self.state.duration = time_to_charge
                self.state.duration_left = time_to_charge
        self.state.last = self.state.sprites_in_row - 1

    def update(self, level):
        frame_time = get_frame_time()
        motion = 0

        if is_key_down(KeyboardKey.KEY_RIGHT):
            if self.grounded:
                self.transition(State.RUNNING)
            self.player_direction = Direction.RIGHT
            motion += 1
        elif is_key_down(KeyboardKey.KEY_LEFT):
            if self.grounded:
                self.transition(State.RUNNING)
            self.player_direction = Direction.LEFT
            motion -= 1
        else:
            if self.grounded and self.state.row != State.CHARGE:
                self.transition(State.IDLE)

        self.velocity.x = motion * MOVE_SPEED
        if self.on_sand:
            self.velocity.x /= 2
        self.position.x += self.velocity.x*frame_time
        self.bounding_box.x = self.position.x + PLAYER_HITBOX_X_OFFSET

        self.handle_tile_collision(level, 'X')

        if self.grounded and (is_key_pressed(KeyboardKey.KEY_UP) or is_key_pressed(KeyboardKey.KEY_SPACE)):
            self.transition(State.JUMP)
            self.velocity.y = self.jump_vel
            if self.on_sand:
                self.velocity.y /= 2
            self.grounded = False

        if (is_key_down(KEY_DOWN) or is_key_down(KeyboardKey.KEY_LEFT_SHIFT)) and self.grounded and not is_key_down(KEY_LEFT) and not is_key_down(
            KEY_RIGHT) and not self.on_sand and self.strength > 0:
            if self.state.row != State.CHARGE:
                self.transition(State.CHARGE)
            if self.jump_vel > -800 - self.strength:
                self.jump_vel -= 2
            else:
                print("jump maxed")

        if (is_key_released(KEY_DOWN) or is_key_released(KeyboardKey.KEY_LEFT_SHIFT)) and self.grounded and not is_key_down(KEY_LEFT) and not is_key_down(
            KEY_RIGHT) and not self.on_sand and self.strength > 0:
            self.transition(State.JUMP)
            self.grounded = False
            self.velocity.y = self.jump_vel
            self.jump_vel = JUMP_VELOCITY
        elif is_key_down(KEY_LEFT) or is_key_down(KEY_RIGHT):
            self.jump_vel = JUMP_VELOCITY

        if self.invincible_timer > 0:
            self.invincible_timer -= frame_time

        self.velocity.y += self.gravity * frame_time
        self.position.y += self.velocity.y * frame_time
        self.bounding_box.y = self.position.y + PLAYER_HITBOX_Y_OFFSET
        if(self.velocity.y > RESTING_VELOCTY):
            self.grounded = False

        self.handle_tile_collision(level, 'Y')

        bottom_bound = WORLD_HEIGHT - PLAYER_BOUNDING_BOX_HEIGHT
        if self.position.y >= bottom_bound:
            self.position.y = bottom_bound
            self.velocity.y = 0
            self.grounded = True
            if self.state.row not in (State.CHARGE, State.HEAL):
                if motion != 0:
                    self.transition(State.RUNNING)
                else:
                    self.transition(State.IDLE)

        self.state.update(frame_time)
        self.player_frame = self.state.frame()
        if (self.player_frame.width < 0 and self.player_direction > 0)or (self.player_frame.width
                                                                 > 0 and self.player_direction < 0):
            self.player_frame.width *= -1

        self.player_dest_rec.x = self.position.x
        self.player_dest_rec.y = self.position.y

    def handle_tile_collision(self, level, axis):
        player_rect = self.get_rect()
        px, py, pw, ph = player_rect
        
        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                
                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue
                
                if (level[row][col] >= 10 and level[row][col] != TILE_SPIKE and level[row][col] != TILE_THROWER) or level[row][col] == TILE_SOLID:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if check_collision_recs(player_rect, tile_rect):
                        
                        if axis == 'X':
                            if self.velocity.x > 0:
                                self.position.x = tile_rect[0] - PLAYER_HITBOX_X_OFFSET - PLAYER_HITBOX_WIDTH
                            elif self.velocity.x < 0:
                                self.position.x = tile_rect[0] + TILE_SIZE - PLAYER_HITBOX_X_OFFSET

                        elif axis == 'Y':
                            if self.velocity.y >= 0.0: # Falling (Hitting Ground)
                                self.position.y = tile_rect[1] - PLAYER_HITBOX_Y_OFFSET - PLAYER_HITBOX_HEIGHT
                                self.grounded = True 
                                self.velocity.y = 0.0 
                                if level[row][col] == TILE_SAND:
                                    self.on_sand = True
                                else:
                                    self.on_sand = False

                            elif self.velocity.y < 0.0: # Jumping (Hitting Ceiling)
                                self.position.y = tile_rect[1] + TILE_SIZE
                                self.velocity.y = 0.0 
                            
                        player_rect = self.get_rect() # Update rect after resolution

    def draw(self, debug):
        if self.invincible_timer <= 0 or int(self.invincible_timer * 10) % 2 == 0:
            draw_texture_pro(
                self.player_texture,
                self.player_frame,
                self.player_dest_rec,
                (0, 0), 0, WHITE,
            )
        if debug:
            draw_rectangle_lines(int(self.position.x + PLAYER_HITBOX_X_OFFSET),
                                  int(self.position.y + PLAYER_HITBOX_Y_OFFSET), PLAYER_HITBOX_WIDTH, PLAYER_HITBOX_HEIGHT, RED)
            draw_text(f"jump velo: {self.jump_vel}", int(self.position.x),
                       int(self.position.y-60), 20, RED)
            draw_text(f"anim: {self.state.cur}", int(self.position.x), int(self.position.y-30), 20, RED)

    def shutdown(self):
        unload_texture(self.player_texture)