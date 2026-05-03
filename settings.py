# --- Game Constants ---
from pathlib import Path
import csv

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40          # Size of one tile in pixels
GRAVITY = 1800.0        # Downward acceleration (pixels/s/s)
JUMP_VELOCITY = -800.0  # Initial upward velocity on jump
STOMP_BOUNCE = JUMP_VELOCITY * 0.6 # Reduced jump velocity for bounce
PLAYER_SPEED = 300.0    # Player horizontal movement speed
ENEMY_SPEED = 100.0     # Enemy horizontal movement speed
PLAYER_WIDTH = TILE_SIZE*.8
PLAYER_HEIGHT = TILE_SIZE*.9
RESTING_VELOCTY = 18

MOVE_SPEED = 200
SPRITE_SHEET_TILE_WIDTH = 168
SPRITE_SHEET_TILE_HEIGHT = 190
PLAYER_SIZE = 40
PLAYER_BOUNDING_BOX_WIDTH = 30
PLAYER_BOUNDING_BOX_HEIGHT = 40
PLAYER_HITBOX_X_OFFSET = 5   
PLAYER_HITBOX_Y_OFFSET = 2   
PLAYER_HITBOX_WIDTH = 20     
PLAYER_HITBOX_HEIGHT = 36    
SPIKE_TIP_HEIGHT = 12      

THIS_DIR = Path(__file__).resolve().parent
SHEET = str(THIS_DIR/"assets/wada_spritesheet.png")
BLOOD_SPRITE = str(THIS_DIR/"assets/blood_bag.png")
WEIGHT_SPRITE = str(THIS_DIR/"assets/weight_sheet.png")
TRACK_GROUND = str(THIS_DIR/"assets/track.png")
SAND_GROUND = str(THIS_DIR/"assets/sand.png")
STONE_GROUND = str(THIS_DIR/"assets/stone.png")
DIRT_GROUND = str(THIS_DIR/"assets/dirt.png")
SPIKES = str(THIS_DIR/"assets/spikes.png")
JAVELIN_SPRITE = str(THIS_DIR/"assets/javelin.png")
SPLASH = str(THIS_DIR/"assets/splash.png")
LEVEL_COMPLETE = str(THIS_DIR/"assets/level_complete.png")
BACKGROUND = str(THIS_DIR/"assets/complete_clean_background.png")
CALCULATING = str(THIS_DIR/"assets/calculating.png")
ESCAPED = str(THIS_DIR/"assets/escaped.png")
CAUGHT = str(THIS_DIR/"assets/caught.png")
DEFEAT = str(THIS_DIR/"assets/defeat.png")
FLAG = str(THIS_DIR/"assets/flag.png")
INSTRUCTIONS = str(THIS_DIR/"assets/instructions.png")
GAME_MUSIC = str(THIS_DIR/"assets/game_music.mp3")
WEIGHT_SOUND = str(THIS_DIR/"assets/weight_sound.mp3")
BLOOD_SOUND = str(THIS_DIR/"assets/blood_pickup.mp3")





WEIGHT_SHEET_TILE_WIDTH = 40
WEIGHT_SHEET_TILE_HEIGHT = 138



# --- Tilemap Definitions ---
TILE_AIR = 0
TILE_SOLID = 1
TILE_TRACK = 10
TILE_STONE = 11
TILE_SAND = 12
TILE_DIRT = 13
TILE_WEIGHT = 2
TILE_ENEMY = 3
TILE_SPIKE = 14
TILE_BLOOD = 6
TILE_WIN = 7
TILE_THROWER = 21
TILE_FLAG = 15


def load_level_from_csv(filename):
    level = []
    with open(filename, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            level.append([int(cell) for cell in row])
    return level

LEVEL1 = load_level_from_csv (str(THIS_DIR/"levels/cc_level1.csv"))
LEVEL2 = load_level_from_csv(str(THIS_DIR/"levels/cc_level2.csv"))
LEVEL3 = load_level_from_csv(str(THIS_DIR/"levels/cc_level3.csv"))


TILE_ROWS = len(LEVEL1)
TILE_COLS = len(LEVEL1[0])

LEVELS = [LEVEL1, LEVEL2, LEVEL3]


# --- World Dimensions ---
WORLD_WIDTH = TILE_COLS * TILE_SIZE
WORLD_HEIGHT = TILE_ROWS * TILE_SIZE