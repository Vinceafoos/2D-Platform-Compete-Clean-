from pyray import *
from settings import *
from anim import *

class State:
    IDLE = 5
    RUNNING = 1
    JUMP = 9

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
                    row=5, sprites_in_row=4,)
        self.player_texture = load_texture(SHEET)
        self.player_frame = self.state.frame()
        self.player_direction = Direction.RIGHT
        self.bounding_box = Rectangle(self.position.x,self.position.y, PLAYER_SIZE, PLAYER_SIZE)

    def get_rect(self):
        """Returns the player's collision bounding box (top-left, width, height)."""
        return (self.position.x, self.position.y, PLAYER_SIZE, PLAYER_SIZE)

    def transition(self, state):
        if state == self.state.row:
            return
        self.state.cur = 0
        match state:
            case State.IDLE:
                self.state.row = State.IDLE
                self.state.sprites_in_row = 4
            case State.RUNNING:
                self.state.row = State.RUNNING
                self.state.sprites_in_row = 6
            case State.JUMP:
                self.state.row = State.JUMP
                self.state.sprites_in_row = 3
        self.state.last = self.state.sprites_in_row - 1

    def update(self):
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
            if self.grounded:
                self.transition(State.IDLE)

        self.velocity.x = motion * MOVE_SPEED
        self.position.x += self.velocity.x*frame_time
        self.bounding_box.x = self.position.x

        self.handle_tile_collision(LEVEL1, 'X')


        if self.grounded and is_key_pressed(KeyboardKey.KEY_UP):
            self.transition(State.JUMP)
            self.velocity.y = self.jump_vel
            self.grounded = False

        if is_key_down(KEY_DOWN) and self.grounded:
            if self.jump_vel > -1000:
                self.jump_vel -= 2
            else:
                print("jump maxed")

    #for tuesday mini presentation:
    #something you can share that would be useful to others
    #one struggle you are having

        if is_key_released(KEY_DOWN) and self.grounded:
            self.transition(State.JUMP)
            self.grounded = False
            self.velocity.y = self.jump_vel
            self.jump_vel = JUMP_VELOCITY

        self.velocity.y += self.gravity * frame_time
        self.position.y += self.velocity.y * frame_time
        self.bounding_box.y = self.position.y

        self.handle_tile_collision(LEVEL1, 'Y')

        bottom_bound = SCREEN_HEIGHT - PLAYER_SIZE
        if self.position.y >= bottom_bound:
            self.position.y = bottom_bound
            self.velocity.y = 0
            self.grounded = True
            if motion != 0:
                self.transition(State.RUNNING)
            else:
                self.transition(State.IDLE)
        """
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > WINDOW_WIDTH - PLAYER_SIZE:
            self.pos.x = WINDOW_WIDTH - PLAYER_SIZE
        """

        self.state.update(frame_time)
        self.player_frame = self.state.frame()
        if (self.player_frame.width < 0 and self.player_direction > 0) or (self.player_frame.width > 0 and self.player_direction < 0):
            self.player_frame.width *= -1


    def handle_tile_collision(self, level, axis):
        """Enemy collision: reverses direction on horizontal wall contact, respects vertical floor contact."""
        enemy_rect = self.get_rect()
        px, py, pw, ph = enemy_rect
        
        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                
                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue
                
                if level[row][col] == TILE_SOLID:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if check_collision_recs(enemy_rect, tile_rect):
                        
                        if axis == 'X':
                            # Reverses direction on horizontal collision
                            if self.velocity.x > 0:
                                self.position.x = tile_rect[0] - PLAYER_SIZE
                            elif self.velocity.x < 0:
                                self.position.x = tile_rect[0] + TILE_SIZE
                            #self.velocity.x *= -1 # Reverse direction

                        elif axis == 'Y':
                            if self.velocity.y > 0.0: # Falling (Hitting Ground)
                                self.position.y = tile_rect[1] - PLAYER_SIZE
                                self.grounded = True 
                                self.velocity.y = 0.0 

                            elif self.velocity.y < 0.0: # Jumping (Hitting Ceiling)
                                self.position.y = tile_rect[1] + TILE_SIZE
                                self.velocity.y = 0.0 
                            
                        enemy_rect = self.get_rect() # Update rect after resolution

    def draw(self):
        draw_texture_pro(
            self.player_texture,
            self.player_frame,
            Rectangle(self.position.x , self.position.y, PLAYER_SIZE , PLAYER_SIZE),
            Vector2(0, 0), 0.0, WHITE,
        )
        draw_rectangle_lines(int(self.position.x), int(self.position.y), PLAYER_SIZE, PLAYER_SIZE, RED)