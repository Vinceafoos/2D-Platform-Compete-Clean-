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

THIS_DIR = Path(__file__).resolve().parent
SHEET = str(THIS_DIR/"wada_spritesheet.png")
BLOOD_SPRITE = str(THIS_DIR/"blood_bag.png")
WEIGHT_SPRITE = str(THIS_DIR/"weight_sheet.png")
TRACK_GROUND = str(THIS_DIR/"track.png")
SAND_GROUND = str(THIS_DIR/"sand.png")
STONE_GROUND = str(THIS_DIR/"stone.png")
DIRT_GROUND = str(THIS_DIR/"dirt.png")
JAVELIN_SPRITE = str(THIS_DIR/"javelin.png")
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
TILE_SPIKE = 4
TILE_BLOOD = 6
TILE_WIN = 7


def load_level_from_csv(filename):
    level = []
    with open(filename, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            level.append([int(cell) for cell in row])
    return level


LEVEL1 = load_level_from_csv("cc_level1.csv")
LEVEL2 = load_level_from_csv("cc_level2.csv")
LEVEL3 = load_level_from_csv("cc_level3.csv")


TILE_ROWS = len(LEVEL1)
TILE_COLS = len(LEVEL1[0])

LEVELS = [LEVEL1, LEVEL2, LEVEL3]


# --- World Dimensions ---
WORLD_WIDTH = TILE_COLS * TILE_SIZE
WORLD_HEIGHT = TILE_ROWS * TILE_SIZE