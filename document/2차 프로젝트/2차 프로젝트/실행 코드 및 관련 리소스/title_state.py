import game_framework
import stage1
from pico2d import *

name = "TitleState"
image = None

def enter():
    global image
    open_canvas(900, 700)
    image = load_image('UI/gameTitle.png')

def exit():
    global image
    del(image)
    close_canvas()

def update():
    pass


def draw():
    global image
    clear_canvas()
    image.draw(450, 350)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.push_state(stage1)


def pause(): pass
def resume(): pass