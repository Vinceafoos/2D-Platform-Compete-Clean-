from raylib import *
from game import *
from settings import * 

if __name__ == '__main__':  

  init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Compete Clean")
  init_audio_device() 
  set_target_fps(120)
  music = load_music_stream(GAME_MUSIC)
  play_music_stream(music)
  current_game = Game()

  while not window_should_close():
    update_music_stream(music)


    current_game.update()

    begin_drawing()
    clear_background(BLACK)
    draw_rectangle_gradient_v(0,   0, SCREEN_WIDTH, 240, Color(10,  20,  70,  255), Color(60, 110, 180, 255))
    draw_rectangle_gradient_v(0, 240, SCREEN_WIDTH, 360, Color(60, 110, 180, 255), Color(120, 145, 165, 255))
    if current_game.game_state == GameStates.GAME:
      current_game.draw_clouds()
      current_game.draw_plane()
      current_game.draw_hud()
    else:
      current_game.draw_screens()
    begin_mode_2d(current_game.camera)

    current_game.draw()
    end_mode_2d()

    end_drawing()

unload_music_stream(music)
close_audio_device()
current_game.shutdown()
close_window()