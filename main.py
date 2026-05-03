from raylib import *
from game import *
from settings import * 

if __name__ == '__main__':  

  init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Compete Clean")
  set_target_fps(120)
  current_game = Game()

  while not window_should_close():

    current_game.update()

    begin_drawing()
    clear_background(SKYBLUE)
    if current_game.game_state == GameStates.GAME:
      current_game.draw_hud()
    else:
      current_game.draw_screens()
    begin_mode_2d(current_game.camera)

    current_game.draw()
    end_mode_2d()

    end_drawing()

close_window()