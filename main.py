from raylib import *
from game import *
from settings import * 

if __name__ == '__main__':  

  init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Compete Clean")
  set_target_fps(120)
  current_game = Game()
  #game_level = current_game.parse_level(LEVEL1)
  current_game.startup(LEVEL1)

  while not window_should_close():

    current_game.update()

    begin_drawing()
    clear_background(SKYBLUE)
    begin_mode_2d(current_game.camera)

    current_game.draw(LEVEL1)
    end_mode_2d()

    end_drawing()

close_window()