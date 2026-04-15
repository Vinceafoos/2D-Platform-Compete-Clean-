# --- Game Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40          # Size of one tile in pixels
GRAVITY = 1800.0        # Downward acceleration (pixels/s/s)
JUMP_VELOCITY = -600.0  # Initial upward velocity on jump
STOMP_BOUNCE = JUMP_VELOCITY * 0.6 # Reduced jump velocity for bounce
PLAYER_SPEED = 300.0    # Player horizontal movement speed
ENEMY_SPEED = 100.0     # Enemy horizontal movement speed
PLAYER_WIDTH = TILE_SIZE * 0.8
PLAYER_HEIGHT = TILE_SIZE * 0.9
BULLET_SPEED = 600

# --- Tilemap Definitions ---
TILE_AIR = 0
TILE_SOLID = 1
TILE_COIN = 2 
TILE_ENEMY = 3 

SPRITE_FRAME_WIDTH = 460
SPRITE_FRAME_HEIGHT = 600