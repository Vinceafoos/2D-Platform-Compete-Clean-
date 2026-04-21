from raylib import *
from game import *
from settings import * 

if __name__ == '__main__':  

  init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Compete Clean")
  init_audio_device() 
  set_target_fps(120)
  current_game = Game()
  #game_level = current_game.parse_level(LEVEL1)

  while not window_should_close():

    current_game.update()
    begin_mode_2d(current_game.camera)

    begin_drawing() 
    clear_background(SKYBLUE) 
    current_game.draw_level(LEVEL1)

    current_game.draw()
    end_mode_2d()

    end_drawing()

close_window()